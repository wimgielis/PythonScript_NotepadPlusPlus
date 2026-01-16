from Npp import editor
import re


# Wim Gielis
# Jan. 2026
#
# IncreaseNumbersInSelection script (Ctrl-Alt-<):
#       - For the currently selected lines, identify all positive numbers with regex
#       - Increase each number with 1 and overwrite the selection


def increment_numbers(text):
    delta = 0

    def repl(match):
        nonlocal delta
        original = match.group()
        new = str(int(original) + 1)
        delta += len(new) - len(original)
        return new

    new_text = re.sub(r'\d+', repl, text)
    return new_text, delta


sel_count = editor.getSelections()

# Process selections from last to first (prevents offset corruption)
for i in reversed(range(sel_count)):
    start = editor.getSelectionNStart(i)
    end   = editor.getSelectionNEnd(i)

    if start == end:
        continue

    original_text = editor.getTextRange(start, end)
    new_text, delta = increment_numbers(original_text)

    editor.setTargetStart(start)
    editor.setTargetEnd(end)
    editor.replaceTarget(new_text)

    # Restore selection with adjusted length
    editor.setSelectionNStart(i, start)
    editor.setSelectionNEnd(i, end + delta)