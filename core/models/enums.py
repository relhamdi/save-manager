from enum import Enum

# Actions available on the game saves
class ActionEnum(Enum):
    PUSH = "push"
    PULL = "pull"

# Supported OS
class OsEnum(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
