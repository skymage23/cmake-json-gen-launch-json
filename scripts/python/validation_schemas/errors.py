class SchemaFileMissingError(Exception):
    def __init__(self, file):
        super().__init__("Import JSON schema file \"{}\" is missing. You will need to revert to a previous commit.".format(file))