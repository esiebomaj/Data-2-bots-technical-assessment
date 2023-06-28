import os
import sys
import json
import pprint


def extract_schema(json_obj):
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
                sub_schema["type"] = s
                pass

            elif obj_type == str:
                sub_schema["type"] = "string"
                pass

            elif obj_type == int:
                sub_schema["type"] = "integer"
                pass

            elif obj_type == list:
                sub_schema["type"] = "list"
                pass

            elif obj_type == bool:
                sub_schema["type"] = "boolean"
                pass

            schema[key] = sub_schema

    return schema


def dump_schema_output(schema, path):
    with open(path, "w") as file:
        json.dump(schema, file)


def main():
    files = os.scandir("./data")
    for file in files:
        # ensure that its a json files
        if file.is_file and ".json" in file.path:
            path = file.path.replace("\\", "/")

            with open(path, "r") as file:
                json_obj = json.load(file)["message"]
                schema = extract_schema(json_obj)
                output_path = path.replace("data", "schema")
                dump_schema_output(schema, output_path)


if __name__ == "__main__":
    main()
