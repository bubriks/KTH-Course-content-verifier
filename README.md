# File content checker

This action is intended for use only by the KTH DevOps course repository. It checks if changes have taken place in the correct location and that the markdown file structure is correct. In case of any violation, it is expected to fail the build. 

## Advice

The functionality of the following actions is incorporated in this repository:
- https://github.com/bubriks/string-verifier
- https://github.com/bubriks/file-content-checker

When possible it is advisable to use them instead of this action, as it is unlikely that this solution is suitable for needs outside of this course.

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
| `location`  | Changes must follow this path.    |
| `structure` | Expected file content structure (JSON string).    |
| `changes` | Location of files that have been changed    |

### Explaning the inputs

#### location

This is a regex string that verifies that changes have taken place in the correct location.

when the string looks like this: ^contributions/.+/(.+)/

the following locations would be accepted
```
contributions/any/any/test1
contributions/some/any/test2...
```
But it would fail the build in the scenario if changes would look like this
```
contributions/any/any/test1
contributions/some/some/test2...
```
Notice, that it is acceptable to have any value for directory directly under contributions, but the following directory must be the same for all changes. This is the case due to the comparison of groups, with "(.+)" symbolizing group, while ".+" allows any variety of input.

#### changes

Changes is a simple space-separated list of changed files. For this example, it utilizes "jitterbit/get-changed-files@v1" Github action.

#### structure

The structure is JSON object that contains regex expressions. The verification of the markdown file contents is done using this JSON schema, with possible usage of three value types: dictionary, list, and string.

- Dictionary- All contents within the dictionary must be satisfied.
- List- At least one of the list elements must match (takes the first match).
- String- Regex value used for line content verification.

This means, that for example only one of the following must match (the first to match is picked).

```
"title": [
  "^# presentation:.*$",
  "^# essay:.*$",
  "^# demo:.*$",
  "^# open-source:.*$",
  "^# executable tutorial:.*$",
  "^# course automation:.*$",
  "^# feedback:.*$"
]
```

While here all entries must be sattisfied for saccesfull completions.

```
{
  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$",
  "gitHub": "^github: https://github.com/[a-z]+$"
}
```

Notice, that these types could be contained within each other and the same rules would appply.

```
"memberOne": [
	{
	  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$",
	  "gitHub": "^github: https://github.com/[a-z]+$"
	},
	{
	  "nameAndEmail": "^[a-z]+( [a-z]+)* [a-z]+ \([a-z]+@kth.se\)$"
	},
	{}
  ],
```

In this case, it could be that 2nd element in the list is the first to be fully satisfied, then it'll be returned, while even though the last element also satisfies the needs it's ignored due to being a lower priority.

### Important to know

The structure JSON "title" is used for category folder name verification. This action extracts information from this field using this regex expression "^# (.+):.*$", meaning that in case of the following regex matching "^# course automation:.*$", the string extracted would be "course automation" and to make it valid for directory name all spaces are replaced with "-". The final result looking like this: "course-automation".

For member folder names the following field value will be used "nameAndEmail" for ["memberOne", "memberTwo", "memberThree"] within the "member" (exactly as shown in the example). The extract last names regex is used ("([a-z]+) \(.+\)$"). The various permutations of last names separated by "-" are compared against the user directory name and in case of no match exception would be thrown.    