import random
import xml.etree.ElementTree as ET

from vlcplayshuffle import parse_xspf
from vlcplayshuffle.constants import EXTENSION_TAG, ID_TAG, TRACKLIST_TAG


def randomize_xspf_tracks(
    tracklist: ET.Element, seed: int | float | str | bytes | bytearray | None = None
) -> ET.Element:
    """
    Randomizes the tracklist by shuffling the elements.

    Args:
        tracklist (ET.Element): The tracklist to be randomized.
        seed (int | float | str | bytes | bytearray | None, optional): The seed value for randomization. Defaults to None.

    Returns:
        ET.Element: The randomized tracklist.
    """
    if seed:
        random.seed(seed)
    randomized_tracklist = tracklist[:]
    random.shuffle(randomized_tracklist)
    for i, child in enumerate(randomized_tracklist):
        child.find(EXTENSION_TAG).find(ID_TAG).text = str(i)
    return randomized_tracklist


def randomize_xspf(xspf_path: str) -> ET.ElementTree:
    """
    Takes a path to a XSPF file as an input, shuffles the tracklist and returns the modified XSPF ElementTree.

    Args:
        xspf_path (str): The path to the XSPF file.

    Returns:
        ET.ElementTree: The modified XSPF ElementTree with the tracklist shuffled.
    """
    xspf = parse_xspf.parse_xspf(xspf_path)
    if not xspf:
        return None
    root = xspf.getroot()
    tracklist_element = root.find(TRACKLIST_TAG)
    parse_xspf.replace_element_children(
        tracklist_element, randomize_xspf_tracks(tracklist_element)
    )
    return xspf
