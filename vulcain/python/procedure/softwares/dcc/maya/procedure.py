import sys
import traceback

from vulcain.python.procedure.shared.vulcain_arg import VArg
from vulcain.python.pipeline_exceptions import ArgumentMissing
import vulcain.python.logger as log


logger = log.Logger(name="Maya Procedure")

class MayaProcedure():
    required_param = {}
    optional_patam = {}

    def __init__(self, **kwargs):
        self.execution_from_ddc = True  # TODO: Find a way to known if were in a shell or in a dcc

    def execute(self, **kwargs):

        if not kwargs:
            kwargs = self.parse_arguments()
            logger.debug(kwargs)
        else:
            logger.debug(kwargs)

        for key, value in kwargs.items():
            if key == "varg":
                kwargs["varg"] == VArg(value)

        if not self.execution_from_ddc:
            import maya.standalone
            maya.standalone.initialize(name="Python")

        # CHECK PROCEDURE
        check_before_procedure_fail = False
        try:
            self.check_before_procedure(**kwargs)
        except Exception as err:
            traceback.print_exc()
            logger.error(err)
            check_before_procedure_fail = True

        if check_before_procedure_fail:
            try:
                self.revert_check_procedure(**kwargs)
                self.end_execute(check_fail=True, check_revert_fail=False)
            except Exception as err:
                self.end_execute(check_fail=True, check_revert_fail=True)

            return

        # PROCEDURE
        procedure_fail = False
        try:
            self.procedure(**kwargs)
        except Exception as err:
            traceback.print_exc()
            logger.error(err)
            procedure_fail = True

        if procedure_fail:
            try:
                self.revert_procedure(**kwargs)
                self.end_execute(fail=True, revert_fail=False)
            except Exception as err:
                self.end_execute(fail=True, revert_fail=True)
        else:
            self.end_execute()

        if not self.execution_from_ddc:
            maya.standalone.uninitialize()

    def check_before_procedure(self, **kwargs):
        logger.debug("There is no check procedure implemented.")

    def revert_check_procedure(self, **kwargs):
        logger.debug("There is no revert check procedure implemented.")

    def procedure(self, **kwargs):
        raise NotImplementedError()

    def revert_procedure(self, **kwargs):
        logger.debug("There is no revert procedure implemented.")

    def end_execute(fail=False, revert_fail=False):
        logger.info("END PROCEDURE")

    def parse_arguments(self):
        keyword_args = {}
        args = sys.argv

        i = 1  # Start at index 1 to skip the script name (index 0)
        while i < len(args):
            arg = args[i]
            if arg.startswith('--'):
                # Found a keyword argument
                key = arg[2:]
                if i + 1 < len(args):
                    # Check if the next argument is the value
                    value = args[i + 1]
                    keyword_args[key] = value
                    i += 1  # Skip the value
                else:
                    # No value provided, treat it as a flag
                    keyword_args[key] = True
            i += 1
        if not keyword_args:
            raise ArgumentMissing()
        return keyword_args


if __name__ == "__main__":
    procedure = MayaProcedure()
    procedure.execute()