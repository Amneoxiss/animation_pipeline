from enum import Enum

class VulcainEntity(Enum):
    ASSET = "asset"
    SETDRESS = "setdress"
    EPISODE = "episode"
    SEQUENCE = "sequence"
    SHOT = "shot"
    TASK = "task"
    VERSION = "version"


class VulcainPath():
    def __init__(self, param):
        self.param = param
        self.entity = self.param.split("~")[1]

    def is_asset(self):
        return self.param.split("~")[0] == "assets"

    def get_vulcain_path_entity(self):
        entity = self.path.split("/")[0]
        if entity == VulcainEntity.ASSET:
            pass
        elif entity == VulcainEntity.SETDRESS:
            pass
        elif entity == VulcainEntity.EPISODE:
            pass
        elif entity == VulcainEntity.SEQUENCE:
            pass
        elif entity == VulcainEntity.SHOT:
            pass
        else:
            raise ValueError()

    def is_asset_task(self):
        return len(self.entity.split("/")) >= 3

    def is_asset_version(self):
        return len(self.entity.split("/")) >= 4

    def get_entity_type(self):
        if self.is_asset():
            return self.entity.split("/")[0] 
        return None

    def get_entity_name(self):
        if self.is_asset():
            return self.entity.split("/")[1]
        return None

    def get_entity_task(self):
        if self.is_asset() and self.is_asset_task():
            return self.entity.split("/")[2]
        return None

    def get_entity_version(self):
        if self.is_asset() and self.is_asset_version():
            return self.entity.split("/")[3]
        return None
