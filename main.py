import tempfile
import vlcplayshuffle
import xml.etree.ElementTree as ET


def save_xsfp_to_temp_dir(
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
    vlcplayshuffle.parse_xspf.save_xspf(xspf, temp_xspf)
    return temp_xspf


def shuffle_and_play(xspf_path: str):
    if not vlcplayshuffle.play_in_vlc.check_vlc_in_path():
        print("Error: vlc binary not in path!")
        return
    xspf = vlcplayshuffle.randomize_xspf.randomize_xspf(xspf_path)
    if not xspf:
        print("Error: couldn't parse xspf file!")
        return
    tracklist_element = xspf.getroot().find(vlcplayshuffle.constants.TRACKLIST_TAG)
    for i, (track_name, track_location) in enumerate(
        vlcplayshuffle.parse_xspf.get_xspf_tracklist_title_location(tracklist_element)
    ):
        print(f"{i}. {track_name} ({track_location})")
    temp_xspf = save_xsfp_to_temp_dir(xspf)
    vlcplayshuffle.play_in_vlc.spawn_vlc([temp_xspf.name])


if __name__ == "__main__":
    shuffle_and_play("music.xspf")
