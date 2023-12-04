from typing import Iterable, Dict, Optional
import os
import glob
from urllib.parse import unquote
from typing_extensions import Annotated
import typer
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


def get_xspf_file_in_current_dir() -> Optional[str]:
    """
    Gets the first XSPF file found in the current directory.

    Returns:
        List[str]: A list of files ending in .xspf in the current directory.
    """
    xspf_files = glob.glob("*.xspf")
    return xspf_files[0] if xspf_files else None


def shuffle_and_play(
    xspf_path: Annotated[
        str, typer.Argument(default_factory=get_xspf_file_in_current_dir)
    ]
):
    if not xspf_path:
        print("Error: no XSPF files found!")
        print("Usage: main.py XSPF_PATH")
        return
    if not vlcplayshuffle.play_in_vlc.check_vlc_in_path():
        print("Error: vlc binary not in path!")
        return
    shuffled_playlist = vlcplayshuffle.randomize_xspf.randomize_xspf_file(xspf_path)
    if not shuffled_playlist:
        print("Error: couldn't parse xspf file!")
        return

    tracklist_paths = []
    for i, (track_name, track_location) in enumerate(shuffled_playlist):
        decoded_file_location = file_uri_decode(track_location)
        tracklist_paths.append(decoded_file_location)
        print(f"{i}. {track_name} ({decoded_file_location})")

    playlist_items_existence = check_playlist_items_exist(tracklist_paths)
    if not all(playlist_items_existence.values()):
        for track_path, exists in playlist_items_existence.items():
            if not exists:
                print(f"Not found: {track_path}")
        print("Error: some items in the tracklist haven't been found")
        return

    vlcplayshuffle.play_in_vlc.spawn_vlc(tracklist_paths)


if __name__ == "__main__":
    typer.run(shuffle_and_play)
