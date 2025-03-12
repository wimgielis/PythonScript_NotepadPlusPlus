from Npp import notepad, editor
import re


# Wim Gielis
# Mar. 2025
#
# TM1NoElementsWithCarets script (Alt-z):
#       - We search for strings with caret (^) in it. It should only be inside square brackets.
#       - in addition, the square brackets must follow 1 or 2 square bracketed text
#       - Then we remove anything inside the square brackets in front of (and including) the last caret.


# Start an undo action for a single undo step
editor.beginUndoAction()

# Get the current position of the caret to avoid losing position after replacement
caret_position = editor.getCurrentPos()

# Do we still have carets ?
caret_count = len(re.findall(r'\^', editor.getText()))
if caret_count == 0:
    notepad.messageBox(f"No carets were found.", "Caret Count", 0)
else:

    # Remove texts
    editor.rereplace(r"(\[.*\]\.\[.*\]\.)\[[^\]]*\^([^\]]+)\]", r"\1[\2]")
    editor.rereplace(r"(\[.*\]\.)\[[^\]]*\^([^\]]+)\]", r"\1[\2]")

    # Move caret back to its original position
    editor.gotoPos(caret_position)

    # End the undo action
    editor.endUndoAction()

    # Do we still have carets ?
    caret_count = len(re.findall(r'\^', editor.getText()))
    if caret_count == 1:
        notepad.messageBox(f"There is still 1 caret in the text.", "Caret Count", 0)
    elif caret_count > 1:
        notepad.messageBox(f"There are still {caret_count} carets in the text.", "Caret Count", 0)