# VLCPlayShuffle

Takes an XSPF file in the current directory, shuffles all the items in it and plays it in VLC.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)

## Setup

1. Clone the repository.
2. Navigate to the project directory.
3. (Optional) Run `pip install -U -r requirements.test.txt` to install testing dependencies.

## Usage

Currently, it scans the current directory for XSPF files and plays the first one that's been found, no fancy CLI arguments yet.

Please ensure that you have the `vlc` binary in your PATH, otherwise it will fail to run.
```bash
python main.py
```

## Testing

1. Ensure you have installed all the dependencies in the `requirements.test.txt` file.
2. Run the following commands in the same order as below.
```bash
coverage run
coverage report
```

## License

This program is distributed under the GPLv3 License. For more information, see the [LICENSE](LICENSE) file.
