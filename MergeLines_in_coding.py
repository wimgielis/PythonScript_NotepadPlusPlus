import re


# Wim Gielis
# Aug. 2026
#
# MergeLines_in_coding script (Alt-Shift-m):
#       - The selected lines are merged with a space, except line 1 + 2, and last but one line + last line
#       - Typical use case is in coding, to merge multiple lines into 1 longer line
#
# Rules:
#   1. First line + second line: no separator
#   2. Middle lines: one space between them
#   3. Last-but-one + last line: no separator
#   4. Remove a trailing comma before a closing ), ] or }
#   5. Works with LF, CRLF, or CR line endings
#   6. The selection is replaced in-place
#   7. The whole operation is one Ctrl+Z undo step


selected = editor.getSelText()
if selected:
    # Split on any of the three possible line-ending styles.
    lines = re.split(r'\r\n|\r|\n', selected)

    # Remove indentation and whitespace around each line.
    lines = [line.strip() for line in lines]

    # Remove empty lines at the beginning/end of the selection.
    while lines and not lines[0]:
        lines.pop(0)

    while lines and not lines[-1]:
        lines.pop()

    if lines:
        # If the final line is a closing bracket,
        # remove the trailing comma from the preceding line.
        if len(lines) >= 2 and lines[-1] in (')', ']', '}'):
            lines[-2] = re.sub(r',\s*$', '', lines[-2])

        if len(lines) == 1:
            result = lines[0]

        elif len(lines) == 2:
            # First/second and last-but-one/last are the same join.
            result = lines[0] + lines[1]

        else:
            # First + second: no space
            result = lines[0] + lines[1]

            # Middle joins: one space
            for i in range(1, len(lines) - 2):
                result += ' ' + lines[i + 1]

            # Last-but-one + last: no space
            result += lines[-1]

        # One undo operation for the entire replacement.
        editor.beginUndoAction()
        try:
            editor.replaceSel(result)
        finally:
            editor.endUndoAction()