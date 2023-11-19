import shutil
import subprocess
from typing import Iterable


def check_vlc_in_path(vlc_binary: str = "vlc") -> bool:
    """
    Check if VLC media player is installed and available in the system's PATH.

    Args:
        vlc_binary (str, optional): The path or name of the VLC media player binary. Default is "vlc".

    Returns:
        bool: True if VLC media player is available, False otherwise.
    """
    return bool(shutil.which(vlc_binary))


def spawn_vlc(args: Iterable[str], vlc_binary: str = "vlc") -> None:
    """
    Spawn a new instance of VLC media player with the provided arguments.

    Args:
        args (Iterable[str]): An iterable of arguments to be passed to VLC media player.
        vlc_binary (str, optional): The path or name of the VLC media player binary. Default is "vlc".
    """
    subprocess.call([vlc_binary, *args])
