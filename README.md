# Save Manager

This repo aims to help keep track of a game's save files across multiple computers.

The program will centralize all the saves of the given games in one place to ease their management, and can also copy those save to their original directories.

## Dependencies

- Python 3.10 (untested on other versions)
- Pydantic (for data models)

Dependencies management is done using `pipenv`, you can create the same virtual environment using the following commands in the root directory:
```sh
pip install pipenv      # If needed
pipenv shell
pipenv install -d
```

## Config

### 1. Config file

To make it work, you must provide a config file with the game saves you want to track.
Example (also in `config/config.base.json`):
```json
{
    "saves": [
        {
            "tag": "",
            "subdir": null,
            "paths": {
                "windows": "",
                "linux": "",
                "macos": ""
            }
        }
    ]
}
```
Properties explanation:
- `saves`: The root of the config file. All games will be in this list.
- `tag`: Defines a game. You can have multiple games with the same tag, if you have multiple instances of a game for example.
- `subdir`, optional: Add a sub-directory within the game's folder, helpful to differentiate tags.
- `paths`: Paths to the save directories of the game on `windows`, `linux` or `macos`.

This config file will be checked using *Pydantic* models to ensure its format.

> Note: While defining your game's paths, you can use system variables to anonymise or shorten them (%UserProfile% for Windows, and ~ for Linux/MacOS for the main ones).

### 2. .env file

You can configure the config file's and the output directory's locations using a `.env` file.
For that, just copy and rename the `.env.default` file to `.env` and fill in the **CONFIG_FILE_PATH** and **OUTPUT_DIR** variables.

> Note 1: Only tested using `pipenv`.

> Note 2: Default values are provided in `core/config.py`, locating the files in this folder.

## Usage

### 1. Script

To start the script, you need to run the `core/main.py` yourself, or using the pipenv script **main** (with the command `pipenv run main`).

Then, you will need to provide arguments for the script to run properly.
Usage: `... main.py [-h] [-w | -l | -m] [{push,pull}] [value]`

- *No arguments*: Lists all games configured in the config file, with an index number for each of them.
- **-h**: Displays the documentation.
- **-w/-l/-m**: Specifies the targeted OS, respectively for Windows, Linux and MacOS.
- **push/pull**: Main action ; **push** will copy from the computer to the output location, and **pull** will copy from the output location to the computer.
- **value**: You can specify one of the index numbers obtained when using the script with no arguments to only activate it for one tag or group of tags.

> Note: If a destination (output or computer) already exists, you will be asked if you want to overwrite the files with the new ones.

### 2. Versioning

Once obtained, you can move your output directory to another device and run the script with the opposite action to keep your progress synchronized.
To do that, you can use Github's versioning feature to save those files in a repository.

Tested method:
1. Create and clone a new Git repository on your computer.
2. Create your `config.json` and your `output` directory at the root of the repository.
3. Fill in the `config.json` (you can use the `config/config.base.json` as a base).
4. (Optional) Create a new directory and open a terminal there (`mkdir modules` && `cd modules`).
5. Create the git submodule with `git submodule add -b main https://github.com/relhamdi/save-manager.git`.
6. Move to the created module (`cd save-manager`).
7. Copy and rename the `.env.default` as `.env` and fill in the paths to the `config.json` and `output` directory.
8. Open a terminal and create the virtual environment:
```sh
pipenv shell
pipenv install -d
```
9. Use the program as you like (always within the `save-manager` directory).
10. Add, commit and push your files to your distant repository.

If you already did those steps and want to clone this project elsewhere, don't forget to initialize the submodule after cloning:
```sh
git submodule init
git submodule update
```

> Note: You can still pull updates when in the `save-manager` directory, if available.

## TODO

- Test on MacOS and Linux
- Allows multiple tags to be used at once
- Automatic detection of the OS
- Option to overwrite (or not) automatically
- Better logging process (?)
- Remove all files before copying to have an exact file sync (?)
