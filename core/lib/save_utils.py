from argparse import ArgumentParser, Namespace
from os import listdir, makedirs
from os.path import exists
from shutil import copytree
from typing import Optional

from models.enums import ActionEnum, OsEnum


def get_padding() -> str:
    """Uniform log padding.

    Returns:
        str: Log padding.
    """
    return " " * 5


def get_parsed_args() -> Namespace:
    """Get parsed arguments of the command.

    Returns:
        Namespace: Parsed args.
    """
    parser = ArgumentParser(description="Game saves management program")

    # Main action
    parser.add_argument(
        "action",
        choices=[e.value for e in ActionEnum],
        nargs="?",  # Optional
        help="Action to execute",
    )

    # Optional arg, adding a save index
    parser.add_argument(
        "value",
        type=int,
        nargs="?",  # Optional
        default=None,
        help="Save index to use with the action, if any.",
    )

    # Arg group to add OS name
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--windows", action="store_true", help="Windows OS")
    group.add_argument("-l", "--linux", action="store_true", help="Linux OS")
    group.add_argument("-m", "--macos", action="store_true", help="MacOS OS")

    # Parsing args
    return parser.parse_args()


def get_os_value(args: Namespace) -> Optional[OsEnum]:
    """Get OS value based on given args.

    Args:
        args (Namespace): Arguments.

    Returns:
        Optional[OsEnum]: OS value.
    """
    if args.windows:
        return OsEnum.WINDOWS
    elif args.linux:
        return OsEnum.LINUX
    elif args.macos:
        return OsEnum.MACOS
    elif not any([args.windows, args.linux, args.macos]):
        print("❌ Error: You must provide the current OS using the proper argument.")
        return None


def copy_directory(src: str, dest: str):
    """Copy recursively a directory.

    Args:
        src (str): Source path.
        dest (str): Destination path.
    """
    if not exists(src):
        print(f"❌ Error - Source directory '{src}' does not exist. Check config file.")
        return

    if not exists(dest):
        makedirs(dest)

    try:
        copytree(src, dest, dirs_exist_ok=True)
        print(
            f"✅ Files copied from \n{get_padding() + src} to \n{get_padding() + dest}"
        )
    except Exception as e:
        print(f"❌ Error during copy: {e}")


def confirm_action(action: ActionEnum, save_tag: str, destination: str) -> bool:
    """Asks for overwriting if destination already exists and non empty.

    Args:
        action (ActionEnum): Current action (logging purposes).
        save_tag (str): Current save (logging purposes).
        destination (str): Destination path.

    Returns:
        bool: True if data will be overwritten, else False.
    """
    if exists(destination) and listdir(destination):
        response = input(
            f"⚠️ '{destination}' already contains files.\n"
            + get_padding()
            + f"Are you sure you want to {action.value} '{save_tag}'? (y/n): "
        )
        return response.strip().lower() == "y"

    # Default to True if no destination or empty folder
    return True
