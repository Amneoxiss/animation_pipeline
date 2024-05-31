from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List


class SanityFailLevel(Enum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


class Sanity(ABC):
    NICE_NAME: str = ""
    FAIL_LEVEL: SanityFailLevel = None
    DEFAULT_CHECK: bool = True
    DEPENDENCY: List[Sanity] = []

    @classmethod
    def validate(cls) -> bool:
        """
        Method to check that the minimum informations required to run properly the sanity exists.
        The two constants NICE_NAME and FAIL LEVEL needs to be filled.
        """
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

        for sanity in self.DEPENDENCY:
            result = sanity.run()
            if result:
                result = [f"Sanity '{sanity.NICE_NAME}' has failed. Can't perform current check."]
                break
        
        if not result:
            result = self.check()

        return result
