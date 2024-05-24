from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List


class SanityFailLevel(Enum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


class SanityStatus(Enum):
    FAIL = auto()
    PASSED = auto()
    RESOLVED = auto()


class Sanity(ABC):
    NICE_NAME: str = ""
    FAIL_LEVEL: SanityFailLevel = None
    DEFAULT_CHECK: bool = True

    def __init__(self) -> None:
        self._sanity_status: SanityStatus = None

    @classmethod
    def validate(cls) -> bool:
        return all(
            [
                cls.NICE_NAME,
                cls.FAIL_LEVEL
            ]
        )

    @abstractmethod
    def check(self) -> List[str]:
        """Method to check the integrity of an element."""

    def fix(self) -> None:
        """Method to resolve a wrong check."""

    @property
    def has_fix(self) -> bool:
        return self.__class__.fix != Sanity.fix

    @property
    def sanity_status(self) -> SanityStatus:
        return self._sanity_status
    
    @sanity_status.setter
    def sanity_status(self, status: SanityStatus) -> None:
        self._sanity_status = status


import random


class CheckVersionUpdater(Sanity):
    FAIL_LEVEL = SanityFailLevel.INFO

    def check(self) -> List[str]:
        if random.choice([True, False]):
            print("Check Version Updater is good")
        else:
            return ["HEIN", "OUI", "NON"]


class CheckAnotherThing(Sanity):
    def check(self) -> List[str]:
        if random.choice([True, False]):
            print("Oui Oui Oui")
        else:
            return ["HEIN", "OUI", "NON"]
    def fix(self) -> None:
        print("Hola !")


if __name__ == "__main__":
    print(CheckVersionUpdater().validate())
    sanity_01 = CheckVersionUpdater()
    result = sanity_01.check()
    print(result)
