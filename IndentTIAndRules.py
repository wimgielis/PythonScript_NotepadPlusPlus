from Npp import editor, notepad
import re


NUMBER_OF_INDENT_SPACES_EX_ANTE = 3
NUMBER_OF_INDENT_SPACES_EX_POST = 4
MAX_NUMBER_OF_INDENT_LEVELS = 50


# Wim Gielis
# Apr. 2025
#
# IndentTIAndRules script (Alt-F11):
#       - The selected text is changed for indentation: 3 spaces in the beginning of a line becomes 4 spaces
#       - First we also delete the trailing spaces and we convert tabs to spaces (in the beginning of the line)
#       - The code will also check if lines have spacing but not a multiple of the expected (ex ante) number of spaces


if NUMBER_OF_INDENT_SPACES_EX_ANTE == NUMBER_OF_INDENT_SPACES_EX_POST:
    notepad.messageBox( f"{NUMBER_OF_INDENT_SPACES_EX_ANTE} is equal to {NUMBER_OF_INDENT_SPACES_EX_POST} and this makes no sense.", "", MESSAGEBOXFLAGS.OK )
else:

    # Define the range object based on the condition
    if NUMBER_OF_INDENT_SPACES_EX_ANTE < NUMBER_OF_INDENT_SPACES_EX_POST:
        # Loop backwards
        range_of_multiples = range(MAX_NUMBER_OF_INDENT_LEVELS, 0, -1)
    else:
        # Loop forwards
        range_of_multiples = range(1, MAX_NUMBER_OF_INDENT_LEVELS + 1)


    # Get selected range
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    start_line_number = editor.lineFromPosition(start)

    # Get selected text and split into lines
    selected_text = editor.getTextRange(start, end)
    lines = selected_text.splitlines()

    new_lines = []
    lines_without_correct_spacing = []
    inside_example_call = False

    for idx, line in enumerate(lines):
        actual_line_number = start_line_number + idx

        # Remove trailing spaces
        line = line.rstrip()

        if line.strip() != "":
            # Replace tabs with spaces but only at the beginning of the line
            match = re.match(r'^([ \t]*)(.*)', line)
            if match:
                # Replace each tab in the leading whitespace with spaces
                line = match.group(1).replace('\t', " " * NUMBER_OF_INDENT_SPACES_EX_POST) + match.group(2)

            if not inside_example_call:
                if line == 'If( 1 = 0 );':
                    if lines[idx + 1].startswith('ExecuteProcess('):
                        inside_example_call = True

            if not inside_example_call:
                # Do we have spaces that is not a correct multiple ? Then flag this line in the console window
                match = re.match(r'^( *)(\S.*)?$', line)
                if match:
                    leading_spaces = match.group(1)
                    space_count = len(leading_spaces)
                    if space_count % NUMBER_OF_INDENT_SPACES_EX_ANTE != 0:
                        lines_without_correct_spacing.append(f"{len(lines_without_correct_spacing) + 1}. Line {actual_line_number + 1} has {space_count} leading spaces: {line}")

                # Replace the indentation
                for i in range_of_multiples:
                    line = re.sub(r"^ {" + str(i * NUMBER_OF_INDENT_SPACES_EX_ANTE) + r"}(?=\S)", " " * i * NUMBER_OF_INDENT_SPACES_EX_POST, line)

            if inside_example_call:
                if line == 'EndIf;':
                    if lines[idx - 1] == ');':
                        inside_example_call = False

        new_lines.append(line)

if lines_without_correct_spacing:
    console.write('\r\n'.join(lines_without_correct_spacing))
    if new_lines:
        apply_changes = notepad.prompt(f"{len(lines_without_correct_spacing):,} line(s) without correct multiple of spaces were identified. Do you want to apply changes to {len(new_lines):,} line(s) anyway ?   Yes or No", "User input", "No")
        if apply_changes:
            if apply_changes.strip().lower() == "y":
                # Replace the content in the editor
                editor.beginUndoAction()
                editor.replaceSel('\r\n'.join(new_lines))
                editor.endUndoAction()
                editor.setCurrentPos(start + 2)
                editor.gotoPos(start + 2)
                console.write(f"\r\nReady, changes made to {len(new_lines):,} line(s).")

else:
    notepad.messageBox("Good, no lines with incorrect multiple of spaces found.")
    if new_lines:
        # Replace the content in the editor
        editor.beginUndoAction()
        editor.replaceSel('\r\n'.join(new_lines))
        editor.endUndoAction()
        editor.setCurrentPos(start + 2)
        editor.gotoPos(start + 2)
        console.write(f"\r\nReady, changes made to {len(new_lines):,} line(s).")
    else:
        console.write("\r\nNo changes made.")