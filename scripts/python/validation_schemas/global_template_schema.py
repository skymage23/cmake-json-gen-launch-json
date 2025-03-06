#For explanations on what these properties do and on their respective values,
#see https://code.visualstudio.com/docs/cpp/launch-json-reference
global_template_validation_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://json-schemas.gen-launch-json.nugent-dev.net",
    "$vocabulary": {
        "https://json-schema.org/draft/2020-12/vocab/core": True,
        "https://json-schema.org/draft/2020-12/vocab/applicator": True,
        "https://json-schema.org/draft/2020-12/vocab/unevaluated": True,
        "https://json-schema.org/draft/2020-12/vocab/validation": True,
        "https://json-schema.org/draft/2020-12/vocab/meta-data": True,
        "https://json-schema.org/draft/2020-12/vocab/format-annotation": True,
        "https://json-schema.org/draft/2020-12/vocab/content": True
    },
    "title": "global_template_validation_schema",
    "type": "object",
    "properties": {
        #This property isn't in the VSCode spec.  This is unique to this app, and is used
        #to help determine whether or not the configuration afterwards described
        #applies to the CMake target being processed.
        "languages": {
            "comment": "Identify which language this configuration applies.",
            "type": "array",
            "minItems": 1,
            "item": {
                "type": "string"
            } #end item
        }, #end languages
        "externalConsole": {
            "type": "boolean",
            "default": True 
        }, 
        "logging": {
            "enum": [
                "exceptions",
                "moduleLoad",
                "programOutput",
                "engineLogging",
                "trace",
                "traceRespose"
            ]
        },
        "visualizerFile": {
            "type": "string",
            "default": None
        },
        "showDisplayString": {
            "type": "boolean",
            "default": False
        },
        "args": {
            "type": "array",
            "item": {
                "type": "string"
            }
        }, 
        "cwd": {
            "type": "string",
            "default": None
        },
        "environment": {
            "type": "array"
        },
        "coreDumpPath": {
            "type": "string",
            "default": None
        }, 
        "miDebuggerServerAddress": {
            "type": "string",
            "default": None
        },
        "debugServerPath": {
            "type": "string",
            "default": None
        },
        "debugServerArgs": {
            "type": "string",
            "default": None
        },
        "serverStarted": {
            "type": "string",
            "default": None
        },
        "filterStdout": {
            "type": "boolean",
            "default": True
        },
        "filterStderr": {
            "type": "boolean",
            "default": False
        },
        "serverLaunchTimeout": {
            "$ref": "https://json-schema.org/draft/2020-12/vocab/validation/$defs/nonNegativeIntegerDefault0",
            "maximum": 10000
        },
    }, #end global_template_validation_schema.properties
    "required": [
        "languages"
    ]
}#end global_template_validation_schema