import os
import verify_location
import verify_markdown
import verify_folder_names


def main():
    location = os.environ["INPUT_LOCATION"]
    changes = os.environ["INPUT_CHANGES"]
    structure = os.environ["INPUT_STRUCTURE"]

    # Verifies that changes are in the correct directory
    location_tuple = verify_location.main(location, changes)
    # Verifies the markdown file contents
    result_structure = verify_markdown.main(location_tuple[0]+"README.md",
                                            structure)
    # Verifies the folder names
    verify_folder_names.main(result_structure, location_tuple[1])

    print("Everything is correct")


if __name__ == "__main__":
    main()
