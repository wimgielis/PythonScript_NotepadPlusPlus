from Npp import notepad, editor


# Wim Gielis
# Mar. 2025
#
# RectangularEdits script (Alt-t):
#       - Test whether the user has a rectangular selection
#       - Ask for the input of:
#         * either an initial numeric value (int or float), a step value and repeat value. Step value can be negative.
#         * either a string value (but this is not useful as you could just type the value... maybe I extend it later though)
#       - Apply the series on the selection
#       - When making the rectangular selection, start from the top or from the bottom
#         * This will determine where the initial value will be written


def convert_to_number(s):
    try:
        # First try to convert to int
        return int(s)
    except ValueError:
        # If it fails, try to convert to float
        try:
            return float(s)
        except ValueError:
            # If both conversions fail, return the original string
            return s

# Constants from Scintilla API
SC_SEL_STREAM = 0
SC_SEL_RECTANGLE = 1
SC_SEL_LINES = 2
SC_SEL_THIN = 3

# Check if the selection is rectangular
if editor.getSelectionMode() != SC_SEL_RECTANGLE:
    notepad.messageBox("Please make a rectangular selection.", "Error", 0)
else:
    # Get number of rows in selection
    num_rows = editor.getSelections()

    # Get the start position of the first selection
    start_pos = editor.getSelectionNStart(0)
    end_pos = editor.getSelectionNEnd(0)

    # Calculate width in characters
    col_width = end_pos - start_pos

    # Ask user for initial number and step value, or text, using Notepad++ built-in prompt dialog
    is_number = False
    initial_value = notepad.prompt("Enter the initial or text:", "Input", "1")
    initial_value = convert_to_number(initial_value)
    if isinstance( initial_value, (int, float)):
        is_number = True
        initial_value = convert_to_number(initial_value)
        step_value = notepad.prompt("Enter the step value (negative for decreasing):", "Input", "1")
        step_value = convert_to_number(step_value)
        repeat = int(notepad.prompt("Enter the repeat value:", "Input", "1"))


    # Generate the sequence of values, including repeats, up to the number of rows needed
    if is_number:
        sequence = [initial_value + (i // repeat) * step_value for i in range(num_rows)]
    else:
        sequence = [initial_value for i in range(num_rows)]


    # Start modifying text
    editor.beginUndoAction()

    # Insert numbers in the selection
    for index, value in enumerate(sequence):

        if is_number:
            number_str = str(value).replace('.', ',').rjust(col_width)  # Right-align text
        else:
            number_str = value

        editor.setTargetRange(editor.getSelectionNStart(index), editor.getSelectionNEnd(index))
        editor.replaceTarget(number_str)

    editor.endUndoAction()