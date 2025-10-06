from Npp import notepad, editor

NUMBER_OF_INDENT_SPACES = 4


# Wim Gielis
# Mar. 2025
#
# CleanUpSpaces script (Alt-p):
#       - The selected text is investigated
#       - First, we trim the trailing whitespace
#       - Then we convert leading tabs to 4 spaces
#       - Lastly, multiples of 3 spaces are converted to the same multiple of 4 spaces


# Get the start and end positions of the current selection
sel_start = editor.getSelectionStart()
sel_end = editor.getSelectionEnd()

# Extend the selection to the start of the first selected line
line_start = editor.lineFromPosition(sel_start)
sel_start = editor.positionFromLine(line_start)

# Extend the selection to the end of the last selected line
line_end = editor.lineFromPosition(sel_end)
sel_end = editor.getLineEndPosition(line_end)

# Set the new selection range
editor.setSelection(sel_end, sel_start)


# Get the selected lines of text
selected_text = editor.getSelText()

# Split into lines and process
lines = selected_text.splitlines()
new_lines = []
found_multiples = set()

for line in lines:

    line = line.rstrip()
    line = line.replace(t,   * NUMBER_OF_INDENT_SPACES)

    new_line = line
    multiple = 30
    if line:
        while multiple >= 1:
            if len(line) - len(line.lstrip()) == multiple * 3:
                if (multiple * 3) % 4 != 0 or (multiple - 1) in found_multiples:
                    new_line = ' ' * (multiple * NUMBER_OF_INDENT_SPACES) + line.lstrip()
                    found_multiples.add(multiple)
                    break
            multiple -= 1
    new_lines.append(new_line)

if new_lines:
    # Join the processed lines back together
    new_text = '\r\n'.join(new_lines)

    # Replace the content in the editor
    editor.replaceSel(new_text)