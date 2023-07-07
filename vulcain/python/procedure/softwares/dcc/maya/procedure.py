import sys
from vulcain.python.pipeline_exceptions import ArgumentMissing

class MayaProcedure():
    def __init__(self, gui=False, **kwargs):
        if not kwargs:
            kwargs = self.parse_arguments()
            print(kwargs)
        else:
            print(kwargs)

    def execute(self):
        procedure_fail = False
        try:
            self.procedure()
        except Exception as err:
            print(err)
            procedure_fail = True

        if procedure_fail:
            try:
                self.revert_procedure()
                self.end_execute(fail=True, revert_fail=False)
            except:
                self.end_execute(fail=True, revert_fail=True)
        else:
            self.end_execute()

    def procedure(self):
        pass

    def revert_procedure(self):
        pass

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
            raise ArgumentMissing
        return keyword_args

    def end_execute(fail=False, revert_fail=False):
        pass


if __name__ == "__main__":
    procedure = MayaProcedure()
    procedure.execute()