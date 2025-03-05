class SampleFileGenerationError(Exception):
    def __init__(self):
        super().__init__(
            "Unable to run the script that generates the comparison file."
        )