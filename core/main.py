from json import load as json_load
from os.path import exists, expanduser, expandvars, join

from lib.save_utils import confirm_action, copy_directory, get_os_value, get_parsed_args
from models.entities import SaveListModel
from models.enums import ActionEnum

from config import CONFIG_FILE_PATH, OUTPUT_DIR

# Check if config file exists
if not exists(CONFIG_FILE_PATH):
    print(f"❌ Error - Config.json does not exist at '{CONFIG_FILE_PATH}'.")
    exit()

# Load config
try:
    with open(CONFIG_FILE_PATH, "r") as f:
        data = json_load(f)
        savedata = SaveListModel(**data)
except Exception as e:
    print(f"❌ Error: {e}")
    exit()
else:
    unique_tags_list = sorted({save.tag for save in savedata.saves})

# Min/Max constants for save's index in list
MIN_VALUE = 0
MAX_VALUE = len(savedata.saves) - 1


def main():
    # Get parsed args
    args = get_parsed_args()

    # If no action, list all save tags
    if args.action is None:
        if not savedata.saves:
            print("No saves found.")

        print("-- Game saves available --")
        for index, tag in enumerate(unique_tags_list):
            print(f"{index} - {tag}")
        return

    # Get action
    action = ActionEnum(args.action)
    # print(f"🔹 Action: {action.value}")

    # Get targeted tag, if applicable
    targeted_tag = None
    if args.value is not None:
        if MIN_VALUE <= args.value <= MAX_VALUE:
            targeted_tag = unique_tags_list[args.value]
            # print(f"🔢 Save index: {args.value}")
            # print(f"🏷 Chosen tag: {targeted_tag}")
        else:
            print("❌ Error: Bad index chosen.")
            return

    # Get OS
    os_value = get_os_value(args)
    if os_value is None:
        return
    # print(f"🖥 Targeted OS: {os_value}")

    # Get targeted save objects
    targeted_saves = savedata.saves
    if targeted_tag is not None:
        # Filter save list if one tag required
        targeted_saves = [save for save in savedata.saves if save.tag == targeted_tag]

    for save in targeted_saves:
        # Get local and distant paths
        local_path = getattr(save.paths, os_value.value, None)
        if not local_path:
            print(f"⚠️ No '{os_value.value}' path was defined for tag '{save.tag}'.")
            continue
        distant_path = join(OUTPUT_DIR, save.tag)
        if save.subdir is not None:
            # Add sub-directory if any
            distant_path = join(distant_path, save.subdir)

        # Resolve eventual path variables
        local_path = expandvars(expanduser(local_path))

        print(f"🚀 Processing {action.value} for tag: {save.tag}")
        if action == ActionEnum.PUSH:
            # 'Push' files from local machine to distant repo
            source_path = local_path
            destination_path = distant_path
        elif action == ActionEnum.PULL:
            # 'Pull' files from distant repo to local machine
            source_path = distant_path
            destination_path = local_path

        if not confirm_action(action, save.tag, destination_path):
            print(f"❌ Action {action.value} canceled for tag '{save.tag}'.")
            continue
        copy_directory(source_path, destination_path)


if __name__ == "__main__":
    main()
