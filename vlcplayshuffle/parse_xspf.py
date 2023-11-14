from typing import List, Tuple
import xml.etree.ElementTree as ET

from vlcplayshuffle.constants import (
    TRACK_TAG,
    TITLE_TAG,
    LOCATION_TAG,
    DEFAULT_NAMESPACES,
)


def parse_xspf(
    xspf_path: str, namespaces: List[Tuple[str, str]] = DEFAULT_NAMESPACES
) -> ET.ElementTree | None:
    """
    Parse an XSPF file and return the parsed XML as an ElementTree object.

    Args:
        xspf_path (str): The path to the XSPF file that needs to be parsed.
        namespaces (list of tuples, optional): A list of namespace prefixes and URIs that will be registered before parsing the XML file. Defaults to DEFAULT_NAMESPACES.

    Returns:
        ElementTree: The parsed XML as an ElementTree object if parsing is successful, else None.
    """
    for prefix, uri in namespaces:
        ET.register_namespace(prefix, uri)
    xspf = None
    try:
        xspf = ET.parse(xspf_path)
    except (ET.ParseError, FileNotFoundError, IsADirectoryError):
        return None
    return xspf


def replace_element_children(
    element_to_replace: ET.Element, new_element_children: ET.Element
):
    """
    Replaces the children of an XML element with new elements.
    NOTE: It will only replace the children, not the parent tag itself.

    Args:
        element_to_replace (ElementTree): The parent element of the children to replace.
        new_element_children (ET.Element): The parent element that contains the new children.
    """
    if element_to_replace and new_element_children:
        element_to_replace.clear()
        element_to_replace.extend(new_element_children)


def save_xspf(xspf: ET.ElementTree, path: str):
    """
    Saves a XSPF file at the specified path.

    Args:
        xspf (ElementTree): The parent element of the file to save.
        path (str): The path where the XSPF file will be saved.
    """
    xspf.write(path, encoding="utf-8", xml_declaration=True)


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
    track_titles = []
    for track in tracklist.findall(TRACK_TAG):
        title_element = track.find(TITLE_TAG)
        title = (
            title_element.text if title_element is not None else "Title not available"
        )
        location_element = track.find(LOCATION_TAG)
        location = (
            location_element.text
            if location_element is not None
            else "Location not available"
        )
        track_titles.append((title, location))
    return track_titles
