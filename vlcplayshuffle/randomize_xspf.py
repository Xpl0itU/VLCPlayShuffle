from typing import Optional, List, Tuple
import random
import xml.etree.ElementTree as ET

from vlcplayshuffle.parse_xspf import parse_xspf, get_xspf_track_title_location
from vlcplayshuffle.constants import TRACKLIST_TAG


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
    return randomized_tracklist


def randomize_xspf_file(xspf_path: str) -> Optional[List[Tuple[str, str]]]:
    """
    Takes a path to a XSPF file as an input, shuffles the tracklist and returns a list of tuples with the name and path of the playlist files.

    Args:
        xspf_path (str): The path to the XSPF file.

    Returns:
        List[Tuple[str, str]]: An optional list of tuples with the name and path of the playlist files.
    """
    assert isinstance(xspf_path, str), "xspf_path must be a string"

    xspf = parse_xspf(xspf_path)
    assert (
        isinstance(xspf, ET.ElementTree) or xspf is None
    ), "parse_xspf should return either None or an ElementTree"

    if not xspf:
        return None
    root = xspf.getroot()
    tracklist_element = root.find(TRACKLIST_TAG)
    assert tracklist_element is not None, "root should have a TRACKLIST_TAG element"

    return [
        get_xspf_track_title_location(track)
        for track in randomize_xspf_tracks(tracklist_element)
    ]
