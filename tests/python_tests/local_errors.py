import initializer
initializer.initialize()

import os_utilities

class SampleFileGenerationError(Exception):
    def __init__(self):
        str_list = ["Unable to run the script that generates the comparison file."]
        if os_utilities.is_windows():
            str_list.append("This could be because you are blocked from running PowerShell files.")
            str_list.append("To fix this, you will have to loosen your Execution Policy.")
            str_list.append("Out of respect for your InfoSec department, we will not detail")
            str_list.append("how to do so here.")
        super().__init__(
            "\n".join(str_list)
        )