import os
import json


PATH_TO_INPUT = "./data"
PATH_TO_OUTPUT = "./schema"


def extract_schema(json_obj: dict) -> dict:
    """
    takes a json_obj in for of a python dictionary and returns its schema
    """

    schema = {}

    for key in json_obj:

        if key != "attributes":

            sub_schema = {
                "tag": "",
                "description": "",
                "required": False
            }

            obj_type = type(json_obj[key])

            if obj_type == dict:
                # if its a nexted object we call this fuction recursivey
                s = extract_schema(json_obj[key])
                sub_schema["properties"] = s
                sub_schema["type"] = "object"
                pass

            elif obj_type == str:
                sub_schema["type"] = "string"
                pass

            elif obj_type == int:
                sub_schema["type"] = "integer"
                pass

            elif obj_type == list:
                if len(json_obj[key]) > 0 and type(json_obj[key][0]) == str:
                    sub_schema["type"] = "enum"
                else:
                    sub_schema["type"] = "array"

            elif obj_type == bool:
                sub_schema["type"] = "bool"
                pass

            schema[key] = sub_schema

    return schema


def dump_schema_output(schema: dict, path: str) -> None:
    """
    dumps the schema into an output json file
    """
    with open(path, "w") as file:
        json.dump(schema, file)


def snif_schema(input_dir: str, output_dir: str) -> None:
    """
    reads the json data from `input_dir` snifs its schema 
    and stores the result in `output_dir` directory
    """

    files = os.scandir(input_dir)
    for file in files:
        # ensure that its a json files
        if file.is_file and ".json" in file.path:
            path = file.path.replace("\\", "/")

            with open(path, "r") as file:
                json_obj = json.load(file).get("message")

                schema = extract_schema(json_obj)

                output_file_name = path.split("/")[-1].replace("data", "schema")
                output_path = os.path.join(output_dir, output_file_name)
                dump_schema_output(schema, output_path)


if __name__ == "__main__":
    snif_schema(PATH_TO_INPUT, PATH_TO_OUTPUT)
