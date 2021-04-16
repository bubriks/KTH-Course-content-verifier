# File content checker

This action is intended for use only by the KTH DevOps course repository. It checks if changes have taken place in correct location and that markdown file structure is currect. In case of any violation it is expected to fail the build. 

## Usage

The verification of the markdown file contents is done using JSON schema, with possible usage of three value types: dictionary, list, and string.

- Dictionary- All contents within the dictionary must be satisfied.
- List- At least one of the list elements must match (takes the first match).
- String- Regex value used for line content verification.

## Advice

Functionality of the following actions is incorporated in repository:
- https://github.com/bubriks/string-verifier
- https://github.com/bubriks/file-content-checker

when possible it is advisible to use them instead of this action.

### Example usage for the Devops course

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

	- id: changed-files
      name: Get changed files
      uses: jitterbit/get-changed-files@v1

    - name: Verify submission details
      uses: bubriks/KTH-Course-content-verifier@master
      with:
        location: ^contributions/(.+)/(.+)/
		changes: ${{ steps.changed-files.outputs.all }}
        structure: >
          {
            "title": [
              "^# presentation:.*$",
              "^# essay:.*$",
              "^# demo:.*$",
              "^# open-source:.*$",
              "^# executable tutorial:.*$",
              "^# course automation:.*$",
              "^# feedback:.*$"
            ],
            "member": {
              "title": "^## members$",
              "memberOne": [
                {
                  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$",
                  "gitHub": "^github: https://github.com/[a-z]+$"
                },
                {
                  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$"
                }
              ],
              "memberTwo": [
                {
                  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$",
                  "gitHub": "^github: https://github.com/[a-z]+$"
                },
                {
                  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$"
                },
                {}
              ],
              "memberThree": [
                {
                  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$",
                  "gitHub": "^github: https://github.com/[a-z]+$"
                },
                {
                  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$"
                },
                {}
              ]
            },
            "proposal": "^## proposal$"
          }
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `path`  | Path to the file to be verified.    |
| `structure` | Expected file content structure (JSON string).    |
| `strip` _(optional)_  | Remove spaces at the beginning and the end of the line read from the file path.    |
| `empty` _(optional)_  | Use empty lines for comparison.    |
| `lower` _(optional)_  | Text from file to lowercase.    |
