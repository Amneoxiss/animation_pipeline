from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List


class SanityFailLevel(Enum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


class SanityStatus(Enum):
    CHECK_FAIL = auto()
    EXECUTION_FAIL = auto()
    PASSED = auto()
    RESOLVED = auto()


class Sanity(ABC):
    NICE_NAME: str = ""
    FAIL_LEVEL: SanityFailLevel = None
    DEFAULT_CHECK: bool = True
    DEPENDENCY: List[Sanity] = []

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

    def run(self) -> List[str]:
        result: List[str] = []
        
        if self.DEPENDENCY:
            for each in self.DEPENDENCY:
                result = each.run()
                if result :
                    break
        
        if not result:
            result = self.check()

        return result


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
