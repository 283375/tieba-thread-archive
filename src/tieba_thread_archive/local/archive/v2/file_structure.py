from typing import Dict, List, Union

from .models import *

AV2File_ThreadInfoJson = AV2ThreadInfo.ArchivePart

AV2File_PostsJson = AV2Posts.ArchivePart

AV2File_UsersJson = Dict[Union[int, str], AV2User.ArchivePart]

AV2File_PortraitsJson = List[AV2TiebaAsset]

AV2File_AssetsJson = List[AV2TiebaAsset]
