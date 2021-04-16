import sys
import re


def main(location, changes):
    groups = None
    match = None
    for i in changes.split(" "):
        match = re.match(location, i)
        if match:
            if groups is None:
                groups = match.groups()
            elif groups != match.groups():
                sys.exit("Groups dont match" +
                         "\nGroup 1: " + str(groups) +
                         "\nGroup 2: " + str(match.groups()))
        else:
            sys.exit("String doesnt match the pattern" +
                     "\nString: " + i)
    return (match.group(0), match.groups())