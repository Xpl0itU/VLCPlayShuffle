from typing import Iterable, Dict
import os


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
