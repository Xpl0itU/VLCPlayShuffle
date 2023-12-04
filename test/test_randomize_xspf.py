import xml.etree.ElementTree as ET
import os.path
import pytest
from vlcplayshuffle.constants import TRACKLIST_TAG, EXTENSION_TAG, ID_TAG
from vlcplayshuffle.randomize_xspf import randomize_xspf_tracks, randomize_xspf_file


# Returns a shuffled tracklist element with the same number of children as the input tracklist element
@pytest.mark.xspf_randomization
def test_returns_shuffled_tracklist_with_same_number_of_children():
    xspf_path = os.path.join("test", "data", "test.xspf")
    xspf = ET.parse(xspf_path)
    tracklist_element = xspf.find(TRACKLIST_TAG)
    shuffled_tracklist = randomize_xspf_tracks(tracklist_element)
    assert len(shuffled_tracklist) == len(tracklist_element)


# The order of the children in the shuffled tracklist element is different from the order of the children in the input tracklist element
@pytest.mark.xspf_randomization
def test_shuffled_tracklist_has_different_order_from_input_tracklist():
    xspf_path = os.path.join("test", "data", "test.xspf")
    xspf = ET.parse(xspf_path)
    tracklist_element = xspf.find(TRACKLIST_TAG)
    shuffled_tracklist = randomize_xspf_tracks(tracklist_element)
    assert shuffled_tracklist != list(tracklist_element)


# The text of the ID tag in each child element of the shuffled tracklist element is a unique integer between 0 and the number of children in the shuffled tracklist element minus 1
@pytest.mark.xspf_randomization
def test_id_tags_in_shuffled_tracklist_are_unique_integers():
    xspf_path = os.path.join("test", "data", "test.xspf")
    xspf = ET.parse(xspf_path)
    tracklist_element = xspf.find(TRACKLIST_TAG)
    shuffled_tracklist = randomize_xspf_tracks(tracklist_element)
    id_tags = [
        int(child.find(EXTENSION_TAG).find(ID_TAG).text) for child in shuffled_tracklist
    ]
    assert len(set(id_tags)) == len(shuffled_tracklist)
    assert all(0 <= id_tag < len(shuffled_tracklist) for id_tag in id_tags)


# Returns an empty tracklist element when the input tracklist element is empty
@pytest.mark.xspf_randomization
def test_returns_empty_tracklist_when_input_tracklist_is_empty():
    tracklist_element = ET.Element(TRACKLIST_TAG)
    shuffled_tracklist = randomize_xspf_tracks(tracklist_element)
    assert len(shuffled_tracklist) == 0


# Returns a list of tuples when given a valid path to an XSPF file
@pytest.mark.xspf_randomization
def test_valid_path_returns_list_of_tuples():
    xspf_path = os.path.join("test", "data", "test.xspf")
    shuffled_list = randomize_xspf_file(xspf_path)
    assert isinstance(shuffled_list, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in shuffled_list)


# Returns None when given an empty path to an XSPF file
@pytest.mark.xspf_randomization
def test_empty_path_returns_none():
    xspf_path = ""
    modified_xspf = randomize_xspf_file(xspf_path)
    assert modified_xspf is None


# Returns None when given a path to a non-existent XSPF file
@pytest.mark.xspf_randomization
def test_nonexistent_path_returns_none():
    xspf_path = os.path.join("test", "data", "nonexistent.xspf")
    modified_xspf = randomize_xspf_file(xspf_path)
    assert modified_xspf is None


# Returns None when given a path to a file that is not an XSPF file
@pytest.mark.xspf_randomization
def test_non_xspf_file_returns_none():
    xspf_path = os.path.join("test", "data", "not_xspf.txt")
    modified_xspf = randomize_xspf_file(xspf_path)
    assert modified_xspf is None
