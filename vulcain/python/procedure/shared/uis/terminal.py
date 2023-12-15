from vulcain.python.procedure.shared.uis.procedure_ui import ProcedureUI

class TerminalUI(ProcedureUI):
    def show_end_success_message(procedure_name: str) -> None:
        print(f"End of {procedure_name}")

    def show_end_fail_message(procedure_name: str, message: str) -> None:
        print(f"Error while executing '{procedure_name}'\n'{message}'")