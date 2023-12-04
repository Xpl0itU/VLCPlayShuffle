from typing import Iterable, Tuple, Optional
import xml.etree.ElementTree as ET

from vlcplayshuffle.constants import (
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


def get_xspf_track_title_location(track: ET.Element) -> Tuple[str, str]:
    """
    This function takes an XML tracklist as input and returns a list of tuples containing the title and location of each track in the tracklist.

    Args:
        tracklist (ET.Element): An XML element representing the tracklist.

    Returns:
        Tuple[str, str]: A tuple containing the title and location of the track.
    """
    assert isinstance(track, ET.Element), "track must be an Element"

    title_element = track.find(TITLE_TAG)
    title = title_element.text if title_element is not None else TITLE_NOT_AVAILABLE
    location_element = track.find(LOCATION_TAG)
    location = (
        location_element.text
        if location_element is not None
        else LOCATION_NOT_AVAILABLE
    )
    track_title = title, location

    assert (
        isinstance(track_title, tuple) and len(track_title) == 2
    ), "track_title should be a tuple of length 2"
    return track_title
