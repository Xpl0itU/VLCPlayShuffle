import os.path
import xml.etree.ElementTree as ET
from vlcplayshuffle.constants import TRACKLIST_TAG
from vlcplayshuffle.parse_xspf import parse_xspf, get_xspf_tracklist_title_location
import pytest


# The function successfully parses a valid xspf file.
@pytest.mark.xspf_parsing
def test_valid_xspf_file():
    xspf_path = os.path.join("test", "data", "test.xspf")
    result = parse_xspf(xspf_path)
    assert isinstance(result, ET.ElementTree)


# The function returns None if the xspf file is not valid XML.
@pytest.mark.xspf_parsing
def test_invalid_xml_file():
    xspf_path = os.path.join("test", "data", "invalid_xml.xspf")
    result = parse_xspf(xspf_path)
    assert result is None


# The function returns None if the xspf file is empty.
@pytest.mark.xspf_parsing
def test_empty_xspf_file():
    xspf_path = os.path.join("test", "data", "empty.xspf")
    result = parse_xspf(xspf_path)
    assert result is None


# The function returns None if the xspf file does not exist.
@pytest.mark.xspf_parsing
def test_non_existing_xspf_file():
    xspf_path = os.path.join("test", "data", "nonexistent.xspf")
    result = parse_xspf(xspf_path)
    assert result is None


# Returns a list of tuples containing the title and location of each track in the tracklist
@pytest.mark.xspf_parsing
def test_returns_list_of_tuples_with_title_and_location():
    tracklist = ET.parse(os.path.join("test", "data", "test.xspf")).getroot()

    result = get_xspf_tracklist_title_location(tracklist)

    assert isinstance(result, list)
    assert all(isinstance(item, tuple) for item in result)
    assert all(len(item) == 2 for item in result)
    assert all(isinstance(item[0], str) for item in result)
    assert all(isinstance(item[1], str) for item in result)


# Returns an empty list if the input tracklist is None
@pytest.mark.xspf_parsing
def test_returns_empty_list_if_tracklist_is_none():
    tracklist = None

    result = get_xspf_tracklist_title_location(tracklist)

    assert result == []


# Returns an empty list if the input tracklist has no TRACK_TAG elements
@pytest.mark.xspf_parsing
def test_returns_empty_list_if_tracklist_has_no_track_elements():
    tracklist = ET.Element(TRACKLIST_TAG)

    result = get_xspf_tracklist_title_location(tracklist)

    assert result == []
