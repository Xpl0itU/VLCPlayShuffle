from typing import List, Iterable, Dict
import os
import tempfile
import glob
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import vlcplayshuffle


def file_uri_decode(uri: str) -> str:
    """
    Decodes a file URI by removing the "file://" prefix and percent-encoding from the remaining string.

    Args:
        uri (str): The file URI to be decoded.

    Returns:
        str: The decoded file URI.
    """
    return unquote(uri.partition("file://")[2])


def check_playlist_items_exist(track_paths: Iterable[str]) -> Dict[str, bool]:
    """
    Checks if the paths passed as argument exist.

    Args:
        track_paths (Iterable[str]): An iterable of paths to check their existence.

    Returns:
        Dict[str, bool]: A dict with the path as a key and if it exists as a value.
    """
    final_dict = {}
    for track_path in track_paths:
        final_dict[track_path] = os.path.exists(track_path)
    return final_dict


def get_xspf_files_in_current_dir() -> List[str]:
    """
    Gets a list of XSPF files in the current directory.

    Returns:
        List[str]: A list of files ending in .xspf in the current directory.
    """
    return glob.glob("*.xspf")


def save_xspf_to_temp_dir(
    xspf: ET.ElementTree,
) -> tempfile._TemporaryFileWrapper:
    """
    Saves an XML ElementTree object to a temporary file with a .xspf extension.

    Args:
        xspf (xml.etree.ElementTree.ElementTree): The XML ElementTree object to be saved as a temporary file.

    Returns:
        tempfile._TemporaryFileWrapper: A wrapper object for the temporary file that contains the saved XML ElementTree.
    """
    temp_xspf = tempfile.NamedTemporaryFile(suffix=".xspf")
    vlcplayshuffle.parse_xspf.save_xspf(xspf, temp_xspf.name)
    return temp_xspf


def shuffle_and_play(xspf_path: str):
    if not vlcplayshuffle.play_in_vlc.check_vlc_in_path():
        print("Error: vlc binary not in path!")
        return
    xspf = vlcplayshuffle.randomize_xspf.randomize_xspf_file(xspf_path)
    if not xspf:
        print("Error: couldn't parse xspf file!")
        return
    tracklist_element = xspf.getroot().find(vlcplayshuffle.constants.TRACKLIST_TAG)
    tracklist = vlcplayshuffle.parse_xspf.get_xspf_tracklist_title_location(
        tracklist_element
    )
    for i, (track_name, track_location) in enumerate(tracklist):
        print(f"{i}. {track_name} ({file_uri_decode(track_location)})")
    tracklist_paths = [file_uri_decode(track_info[1]) for track_info in tracklist]
    playlist_items_existence = check_playlist_items_exist(tracklist_paths)
    if not all(playlist_items_existence.values()):
        for track_path, exists in playlist_items_existence.items():
            if not exists:
                print(f"Not found: {track_path}")
        print("Error: some items in the tracklist haven't been found")
        return

    temp_xspf = save_xspf_to_temp_dir(xspf)
    vlcplayshuffle.play_in_vlc.spawn_vlc([temp_xspf.name])


if __name__ == "__main__":
    import sys

    xspf_files = get_xspf_files_in_current_dir()
    if not xspf_files:
        print("Error: no XSPF files found in the current directory")
        sys.exit(1)
    print(f"Found {len(xspf_files)} XSPF files in the current directory")
    print(f"Playing {xspf_files[0]}")
    shuffle_and_play(xspf_files[0])
