from typing import Iterable, List, Tuple, Optional
import xml.etree.ElementTree as ET

from vlcplayshuffle.constants import (
    TRACK_TAG,
    TITLE_TAG,
    LOCATION_TAG,
    DEFAULT_XSPF_VLC_NAMESPACES,
    TITLE_NOT_AVAILABLE,
    LOCATION_NOT_AVAILABLE,
)


def parse_xspf(
    xspf_path: str, namespaces: Iterable[Tuple[str, str]] = DEFAULT_XSPF_VLC_NAMESPACES
) -> Optional[ET.ElementTree]:
    """
    Parse an XSPF file and return the parsed XML as an ElementTree object.

    Args:
        xspf_path (str): The path to the XSPF file that needs to be parsed.
        namespaces (Iterable[Tuple[str, str]], optional): A list of namespace prefixes and URIs that will be registered before parsing the XML file. Defaults to DEFAULT_XSPF_VLC_NAMESPACES.

    Returns:
        ET.ElementTree: The parsed XML as an ElementTree object if parsing is successful, else None.
    """
    assert isinstance(xspf_path, str), "xspf_path must be a string"
    assert isinstance(namespaces, Iterable), "namespaces must be an iterable"

    for prefix, uri in namespaces:
        ET.register_namespace(prefix, uri)
    xspf = None
    try:
        xspf = ET.parse(xspf_path)
    except (ET.ParseError, FileNotFoundError, IsADirectoryError):
        return None

    assert xspf is not None, "xspf should not be None after successful parsing"
    return xspf


def replace_element_children(
    element_to_replace: ET.Element, new_element_children: Iterable[ET.Element]
) -> None:
    """
    Replaces the children of an XML element with new elements.
    NOTE: It will only replace the children, not the parent tag itself.

    Args:
        element_to_replace (ET.Element): The parent element of the children to replace.
        new_element_children (ET.Element): The parent element that contains the new children.
    """
    if not element_to_replace or not new_element_children:
        return

    assert isinstance(
        element_to_replace, ET.Element
    ), "element_to_replace must be an Element"
    assert isinstance(
        new_element_children, Iterable
    ), "new_element_children must be an Iterable"

    if element_to_replace and new_element_children:
        element_to_replace.clear()
        element_to_replace.extend(new_element_children)
        assert len(element_to_replace) == len(
            new_element_children
        ), "The element_to_replace should have the same number of children as new_element_children"


def save_xspf(xspf: ET.ElementTree, path: str) -> None:
    """
    Saves a XSPF file at the specified path.

    Args:
        xspf (ET.ElementTree): The parent element of the file to save.
        path (str): The path where the XSPF file will be saved.
    """
    assert isinstance(xspf, ET.ElementTree), "xspf must be an ElementTree"
    assert isinstance(path, str), "path must be a string"

    try:
        xspf.write(path, encoding="utf-8", xml_declaration=True)
    except (PermissionError, IsADirectoryError) as e:
        print(f"Error saving XSPF file: {e}")


def get_xspf_tracklist_title_location(tracklist: ET.Element) -> List[Tuple[str, str]]:
    """
    This function takes an XML tracklist as input and returns a list of tuples containing the title and location of each track in the tracklist.

    Args:
        tracklist (ET.Element): An XML element representing the tracklist.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing the title and location of each track in the tracklist.
    """
    if not tracklist:
        return []

    assert isinstance(tracklist, ET.Element), "tracklist must be an Element"

    track_titles = []
    for track in tracklist.findall(TRACK_TAG):
        title_element = track.find(TITLE_TAG)
        title = title_element.text if title_element is not None else TITLE_NOT_AVAILABLE
        location_element = track.find(LOCATION_TAG)
        location = (
            location_element.text
            if location_element is not None
            else LOCATION_NOT_AVAILABLE
        )
        track_titles.append((title, location))

    assert all(
        isinstance(track_title, tuple) and len(track_title) == 2
        for track_title in track_titles
    ), "Each item in the result should be a tuple of length 2"
    return track_titles
