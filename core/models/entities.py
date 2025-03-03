from typing import List, Optional

from pydantic import BaseModel, Field

# Class with different paths to the given ressource, depending of the OS
class OsPathModel(BaseModel):
    windows: str
    linux: str
    macos: str

# Base game save representation
class SaveModel(BaseModel):
    # Tag is used instead of name because multiple SaveModel could have the same tag.
    # It is the case when wanting to manage two or more save directories for a unique game.
    # Thus, all of then will be grouped under the same tag
    tag: str
    # Subdir allows to split different saves with the same tag in different sub-directories.
    subdir: Optional[str] = None
    paths: OsPathModel

# List of game saves
class SaveListModel(BaseModel):
    saves: List[SaveModel] = Field(default_factory=list)
