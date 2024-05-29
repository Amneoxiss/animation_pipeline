from dataclasses import dataclass, field
from .sanity_check import Sanity, SanityStatus
from typing import Tuple, List

@dataclass
class SanityResult:
    result: List[str] = field(default_factory=list)
    status: SanityStatus = None
    sanity_name: str = ""


class SanityRunner:
    def __init__(self) -> None:
        pass

    def run(self, sanity: Sanity) -> SanityResult:
        sanity_result = SanityResult
        _result: List[str] = []
        try:
            sanity_result.result = sanity.check()
        except Exception as err:
            _status = SanityStatus.EXECUTION_FAIL
            _result = ["Execution Failed."]

        if _result:
            sanity_result.status = SanityStatus.FAIL
        sanity_result.result = _result 

        
    def run_and_fix(self, sanity: Sanity) -> SanityResult:
        result: List[str] = []
        try:
            result = sanity.check()
        except Exception as err:
            sanity.status = SanityStatus.EXECUTION_FAIL
            result = ["Execution failed"]
        if not result:
            sanity.status = SanityStatus.FAIL
        elif result and sanity.has_fix:
            sanity.fix()
        else:
            return result, SanityStatus.FAIL
