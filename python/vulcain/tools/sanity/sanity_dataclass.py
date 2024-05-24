from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Iterable


class FailLevel(Enum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


@dataclass
class SanityInfos:
    sanity_name: str
    fail_level: FailLevel

    @property
    def sanity_nice_name(self):
        return self.sanity_name.replace("_", " ").title()


collectorFn = Callable[[], Iterable]


class SanityCheck(ABC):

    def __init__(self, sanity_infos: SanityInfos, collector: collectorFn):
        self.sanity_infos = sanity_infos
        self.collector = collector
        self.failed_listing: list[str] = []

    @abstractmethod
    def check() -> list[str]:
        pass

    @abstractmethod
    def resolve() -> None:
        pass


class Sanifier():

    def __init__(self, sanity_listing: list = None):
        self.sanity_listing = sanity_listing

    def add_sanity(self, sanity: SanityCheck):
        self.sanity_listing.append(sanity)

    def remove_sanity(self, sanity_name: str):
        sanity = self.get_sanity_from_name(sanity_name)
        self.sanity_listing.pop(sanity)

    def get_sanity_from_name(self, sanity_name):
        for sanity in self.sanity_listing:
            if sanity.sanity_infos.sanity_nice_name != sanity_name:
                continue

            return sanity


#### IMPLEMENTATION


class CheckSomething(SanityCheck):
    def check(self):
        print("CHECKING SOMETHING.")
        print(self.collector())
        self.sanity_infos.fail_level = FailLevel.WARNING

    def resolve(self):
        print("RESOLVING SOMETHING.")


def get_dag():
    return {"key": "value"}


def sanity_assetbase(sanifier: Sanifier) -> Sanifier:
    # Add check assetbase
    check_something_infos = SanityInfos(fail_level=FailLevel.ERROR, sanity_name="some_random_check")
    check_something = CheckSomething(check_something_infos, collector=get_dag)
    sanifier.add_sanity(check_something)

    return sanifier


def belfort_sanity_assetbase(sanifier: Sanifier) -> Sanifier:
    sanifier.remove_sanity("some_random_check")


def main():
    un_sanity_complet = sanity_assetbase(Sanifier())
    un_sanity_spécifique_au_projet = belfort_sanity_assetbase(un_sanity_complet)

    # UNE FACTORY ?


if __name__ == "__main__":
    main()