import sys
import re
import json
from itertools import permutations

def get_category_folder(json_structure):
    m = re.search("^# (.+):.*$", json_structure["title"])
    if m:
        return m.group(1).replace(" ", "-")
    sys.exit("Category folder found no match")

def get_member_last_name_list(json_structure):
    member_last_names = []

    for member_key in ["memberOne", "memberTwo", "memberThree"]:
        name_email = json_structure["member"][member_key].get("nameAndEmail")
        if name_email is not None:
             m = re.search("([a-z]+) \(.+\)$", name_email)
             if m:
                 last_name = m.group(1)
                 member_last_names.append(last_name)

    return member_last_names

def main(structure, folder_names):
    json_structure = json.loads(structure)
    
    expected_category_folder = get_category_folder(json_structure)
    if(folder_names[0] != expected_category_folder):
        sys.exit("Category folder doesnt match markdown file contents\n" +
                 "Expected: " + expected_category_folder)
    
    member_last_names = get_member_last_name_list(json_structure)
    perms = ['-'.join(p) for p in permutations(member_last_names)]
    if(folder_names[1] not in perms):
        sys.exit("Member names not represented in folder name\n" +
                 "Expected variations: " + str(perms))