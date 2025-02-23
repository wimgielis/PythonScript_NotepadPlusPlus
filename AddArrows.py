from Npp import editor


# Wim Gielis
# Feb. 2025
#
# AddArrows script (Alt-a):
#       - Select all the text in the selected file
#       - First we delete all lines that contain the word Wim.
#       - For every line that is ONLY a space character and nothing else, in front we add an arrow
#       - The cursor is put after the first arrow, for quick editing.


# Get the editor object
editor.beginUndoAction()
try:
    # Select all text
    editor.selectAll()
    text = editor.getText()

    # Split into lines and process
    lines = text.splitlines()
    new_lines = []

    for line in lines:
        # Skip lines containing 'Wim'
        if 'Wim' in line:
            continue
        # A line with only a space gets an arrow
        # But only when there is already text (the greeting is ignored and does not need an arrow)
        elif line == ' ':
            if new_lines:
                new_lines.append('==> ')
        elif line.strip() == '':
            if new_lines:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Add an extra arrow, unless the last line contains the word 'hopefully'
    if not (new_lines and 'hopefully' in new_lines[-1].strip().lower()):
        new_lines = new_lines + ['', '==> ']

    # A greeting
    new_lines = ["Hi Neil,", "", "I hope you're good.", ""] + new_lines

    # Join the processed lines back together
    new_text = '\r\n'.join(new_lines)

    # Replace the content in the editor
    editor.setText(new_text)

    # Find the position of the first arrow and move the cursor there
    arrow_pos = new_text.find('==> ')
    if arrow_pos != -1:
        editor.gotoPos(arrow_pos + 6)
    else:
        editor.gotoPos(0)
finally:
    editor.endUndoAction()