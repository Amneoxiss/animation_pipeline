from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from .sanity_check import Sanity, SanityFailLevel


class SanityStatus(Enum):
    CHECK_FAIL = auto()
    EXECUTION_FAIL = auto()
    PASSED = auto()
    RESOLVED = auto()


@dataclass
class SanityResult:
    result: List[str] = field(default_factory=list)
    status: SanityStatus = None
    sanity_name: str = ""


def get_sanity_result(sanity: Sanity) -> SanityResult:
    sanity_result = SanityResult
    sanity_result.sanity_name = sanity.NICE_NAME

    try:
        _result = sanity.run()
        if _result:
            sanity_result.result = _result
            sanity_result.status = SanityStatus.CHECK_FAIL
        else:
            sanity_result.status = SanityStatus.PASSED

    except Exception as err:
        sanity_result.result = [f"Execution Failed :\n{str(err)}"]
        sanity_result.status = SanityStatus.EXECUTION_FAIL

    return sanity_result


def run_and_fix_sanity(sanity: Sanity) -> SanityResult:
    sanity_result = get_sanity_result(sanity)

    if sanity_result.status == SanityStatus.PASSED or sanity_result.status == SanityStatus.EXECUTION_FAIL:
        return sanity_result

    if sanity_result.status == SanityStatus.CHECK_FAIL and sanity.FAIL_LEVEL == SanityFailLevel.WARNING:
        try:
            sanity.fix()
            sanity_result.result = sanity.run()
        except Exception as err:
            sanity_result.result = [f"Execution Failed :\`n{str(err)}"]
            sanity_result.status = SanityStatus.EXECUTION_FAIL

    if not sanity_result.result:
        sanity_result.status = SanityStatus.RESOLVED
    
    return sanity_result
