from os import environ, getcwd
from os.path import join

# Config file path
CONFIG_FILE_PATH = environ.get("CONFIG_FILE_PATH", "")
if not CONFIG_FILE_PATH:
    # Default value
    CONFIG_FILE_PATH = join(getcwd(), "config", "config.json")

# Output directory
OUTPUT_DIR = environ.get("OUTPUT_DIR", "")
if not OUTPUT_DIR:
    # Default value
    OUTPUT_DIR = join(getcwd(), "output")
