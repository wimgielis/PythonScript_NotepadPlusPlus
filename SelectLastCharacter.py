from Npp import editor


# Wim Gielis
# Mar. 2025
#
# SelectLastCharacter script (Alt-b):
#       - For the selected text, select each time after the last character (not the EOL character)
#       - This is useful because a rectangular selection would leave extra whitespace after the last character on the line.


# Get the current selection range
sel_start = editor.getSelectionStart()
sel_end = editor.getSelectionEnd()

# Get the starting and ending line numbers of the selection
start_line = editor.lineFromPosition(sel_start)
end_line = editor.lineFromPosition(sel_end)

# Create an empty list to store selection ranges
selection_ranges = []

# Iterate through selected lines only
for line_num in range(start_line, end_line + 1):
    # Get line content
    line_text = editor.getLine(line_num)

    # Strip newline characters and check if line is not empty
    stripped_text = line_text.rstrip("\r\n")
    if stripped_text:
        # Find the last character index in the line
        start_pos = end_pos = editor.positionFromLine(line_num) + len(stripped_text)

        # Only select if within the original selection range
        if sel_start <= start_pos <= sel_end:
            selection_ranges.append((start_pos, end_pos))

# Make the multiple selections
if selection_ranges:
    # Clear any existing selection
    editor.setSelectionMode(0)  # Normal selection mode

    # Set initial selection
    first_start, first_end = selection_ranges[0]
    editor.setSelection(first_end, first_start)

    # Add additional selections
    for start, end in selection_ranges[1:]:
        editor.addSelection(end, start)

    editor.setSelectionMode(0)