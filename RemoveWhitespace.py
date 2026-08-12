from Npp import *
import re


# Wim Gielis
# Aug. 2026
#
# RemoveWhitespace script (Ctrl-<):
#       - From the end of the line, put a space, remove all whitespace until the following non-whitespace encountered
#       - This could span several linse possibly.
#       - This is useful for cleaning up code and texts.
#


editor.beginUndoAction()

try:
    # Current line
    line = editor.lineFromPosition(editor.getCurrentPos())

    # End of the current line, before its line ending
    start = editor.getLineEndPosition(line)

    # Get everything from here to the end of the document
    remaining = editor.getTextRange(start, editor.getLength())

    # Find the first non-whitespace character
    match = re.search(r'\s*(\S)', remaining)

    if match:
        # Replace ALL whitespace between the current line
        # and the first non-whitespace character with ONE space.
        #
        # Example:
        #     "\r\n   \r\n      W"
        # becomes:
        #     " W"
        target_start = start
        target_end = start + match.end()

        editor.setTargetRange(target_start, target_end)
        editor.replaceTarget(" " + match.group(1))

    else:
        # Nothing but whitespace remains.
        # Just put one space at the end of the current line.
        editor.insertText(start, " ")

finally:
    editor.endUndoAction()