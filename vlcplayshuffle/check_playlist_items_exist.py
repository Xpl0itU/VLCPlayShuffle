from typing import Iterable, Dict
import os


def check_playlist_items_exist(track_paths: Iterable[str]) -> Dict[str, bool]:
    final_dict = {}
    for track_path in track_paths:
        final_dict[track_path] = os.path.exists(track_path)
    return final_dict
