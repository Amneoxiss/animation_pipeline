from abc import ABC, abstractmethod

class ProcedureUI(ABC):
    @abstractmethod
    def show_end_success_message(procedure_name: str) -> None:
        """"""

    @abstractmethod
    def show_end_fail_message(procedure_name: str, message: str) -> None:
        """"""
