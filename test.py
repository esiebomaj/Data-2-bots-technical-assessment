import json
import unittest
from main import snif_schema
import os


class TestSnifSchema(unittest.TestCase):

    def doCleanups(self) -> None:
        # we clean up by deleting the test scema file that was created
        os.remove("./test_data/schema/schema.json")
        return super().doCleanups()

    def test_snif_schema(self):
        """
        test the sniffer function
        :return:
        """

        expected_schema_path = "./test_data/schema/expected_schema.json"
        output_path = "./test_data/schema/schema.json"
        input_data_path = "./test_data/data"
        output_dir_path = "./test_data/schema"

        snif_schema(input_data_path, output_dir_path)

        # test that an output schema was indeed created
        self.assertEqual(os.path.exists(output_path), True)

        with open(expected_schema_path) as file:
            expected_schema = json.load(file)

        with open(output_path) as file:
            result_schema = json.load(file)

        # test that the output that was created matches the expected results
        self.assertEqual(expected_schema, result_schema)
