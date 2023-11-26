from typing import Optional
import random
import xml.etree.ElementTree as ET

from vlcplayshuffle import parse_xspf
from vlcplayshuffle.constants import EXTENSION_TAG, ID_TAG, TRACKLIST_TAG


def randomize_xspf_tracks(tracklist: ET.Element) -> ET.Element:
    """
    Randomizes the tracklist by shuffling the elements.

    Args:
        tracklist (ET.Element): The tracklist to be randomized.

    Returns:
        ET.Element: The randomized tracklist.
    """
    assert isinstance(tracklist, ET.Element), "tracklist must be an Element"

    randomized_tracklist = tracklist[:]
    random.shuffle(randomized_tracklist)
    for i, child in enumerate(randomized_tracklist):
        extension_element = child.find(EXTENSION_TAG)
        assert (
            extension_element is not None
        ), "Each child should have an EXTENSION_TAG element"
        id_element = extension_element.find(ID_TAG)
        assert (
            id_element is not None
        ), "Each EXTENSION_TAG element should have an ID_TAG element"
        id_element.text = str(i)
    return randomized_tracklist


def randomize_xspf_file(xspf_path: str) -> Optional[ET.ElementTree]:
    """
    Takes a path to a XSPF file as an input, shuffles the tracklist and returns the modified XSPF ElementTree.

    Args:
        xspf_path (str): The path to the XSPF file.

    Returns:
        ET.ElementTree: The modified XSPF ElementTree with the tracklist shuffled.
    """
    assert isinstance(xspf_path, str), "xspf_path must be a string"

    xspf = parse_xspf.parse_xspf(xspf_path)
    assert (
        isinstance(xspf, ET.ElementTree) or xspf is None
    ), "parse_xspf should return either None or an ElementTree"

    if not xspf:
        return None
    root = xspf.getroot()
    tracklist_element = root.find(TRACKLIST_TAG)
    assert tracklist_element is not None, "root should have a TRACKLIST_TAG element"

    parse_xspf.replace_element_children(
        tracklist_element, randomize_xspf_tracks(tracklist_element)
    )
    return xspf
