from abc import ABC, abstractmethod

class UI(ABC):
    @abstractmethod
    def show_end_success_message(procedure_name: str) -> None:
        """"""

    @abstractmethod
    def show_end_fail_message(procedure_name: str, message) -> None:
        """"""

    @abstractmethod
    def show_check_fail_message(procedure_name: str, message: str) -> None:
        """"""

    @abstractmethod
    def show_execute_fail_message(procedure_name: str, message: str) -> None:
        """"""

    @abstractmethod
    def show_revert_fail_message(procedure_name: str, message: str) -> None:
        """"""