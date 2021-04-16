import sys
import json
import re


def get_lines_from_file(path):
    file = open(path, 'r')
    lines = file.readlines()
    lines = [s.strip() for s in lines]
    lines = list(filter(None, lines))
    lines = [s.lower() for s in lines]
    return lines


def verify_lines(json_input, lines):
    if isinstance(json_input, list):
        for json_value in json_input:
            response = verify_lines(json_value, lines)
            if response is not None:
                return response
        return None
    elif isinstance(json_input, dict):
        test_lines = lines.copy()
        for json_value in json_input:
            response = verify_lines(json_input[json_value], test_lines)
            if response is None:
                return None
            json_input[json_value] = response
        lines.clear()
        lines.extend(test_lines)
        return json_input
    elif isinstance(json_input, str):
        if len(lines) > 0 and re.search(json_input, lines[0]):
            return lines.pop(0)
        else:
            return None
    else:
        sys.exit(f"incorrect data type for: {json_input}")
        return None


def main(path, structure):
    structure = r"" + structure.replace("\\", "\\\\")
    json_structure = json.loads(structure)

    lines = get_lines_from_file(path)
    json_output = verify_lines(json_structure, lines)
    if json_output is not None:
        result = json.dumps(json_output)
        return result
    else:
        sys.exit("Contents don't match the provided structure")
