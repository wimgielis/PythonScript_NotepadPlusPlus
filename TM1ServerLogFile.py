from Npp import editor, notepad
from datetime import datetime, timedelta


# Wim Gielis
# Mar. 2025
#
# TM1ServerLogFile script (Alt-......):
#       - The TM1 server log file, with a predefined format, can be queried/manipulated
#       - The goal is to make quick selections like today's log or this hour's logs


console.write('I NEED THE PANDAS MODULE !!!')
console.write('DE CHAT WERD GEARCHIVEERD !!')


# Define column index (0-based)
TIMESTAMP_COLUMN = 3  # 4th column
COLUMN_SEPARATOR = "   "
TIME_FORMAT_TIMESTAMP = "%Y-%m-%d %H:%M:%S.%f"
TIME_FORMAT_DATE = "%Y-%m-%d"


def find_match_line(current_timestamp_selection, total_lines: int, direction: str = "top-down") -> int:
    """
    Find the first or last occurrence of a given date in the specified column.

    Args:
        current_timestamp_selection (date): The date to match.
        total_lines (int): The total number of lines in the document.
        direction (str): "top-down" to find the first match, "bottom-up" to find the last match.

    Returns:
        int: The line number of the first/last match, or -1 if no match is found.
    """
    console.write('\n' + str(total_lines))
    line_range = range(total_lines) if direction == "top-down" else range(total_lines - 1, -1, -1)

    for i in line_range:
        if i < 0 or i >= total_lines:  # Prevent out-of-bounds error
            console.write(f"Skipping invalid line index: {i}\n")
            continue  # Skip and move on
        line_text = editor.getLine(i).strip()
        cols = line_text.split(COLUMN_SEPARATOR)

        if len(cols) > TIMESTAMP_COLUMN:
            try:
                entry_date = datetime.strptime(cols[TIMESTAMP_COLUMN], TIME_FORMAT_TIMESTAMP).date()
                if entry_date == current_timestamp_selection:
                    return i
            except ValueError:
                continue  # Ignore invalid date formats

    return -1  # No match found


# Get the current line number and text
current_line_number = editor.lineFromPosition(editor.getCurrentPos())
current_line_text = editor.getLine(current_line_number).strip()
current_line_columns = current_line_text.split(COLUMN_SEPARATOR)

do_continue = True
if len(current_line_columns) > TIMESTAMP_COLUMN:
    # Extract the date from the selected line (assuming format "YYYY-MM-DD")
    current_timestamp_str = current_line_columns[TIMESTAMP_COLUMN]
    try:
        current_timestamp_selection = datetime.strptime(current_timestamp_str, TIME_FORMAT_TIMESTAMP).date()
        selection_before = current_timestamp_selection - timedelta(days=1)
        console.write(str(selection_before))
    except ValueError:
        notepad.messageBox("Error: Invalid date format in selected line.")
        do_continue = False

if do_continue:
    total_lines = editor.getLineCount()

    # Step 1: Find the logs matching the time selection
    last_match = find_match_line(current_timestamp_selection, total_lines, "bottom-up")
    first_match = find_match_line(selection_before, last_match, "bottom-up")

    # Step 2: Extract matching lines
    if first_match != -1 and last_match != -1 and first_match <= last_match:
        filtered_lines = [editor.getLine(i).strip() for i in range(first_match, last_match + 1)]
        notepad.messageBox(str(first_match))
        notepad.messageBox(str(last_match))
        # notepad.messageBox("\n".join(filtered_lines))  # Print in the PythonScript console

        # Optional: Replace document content with filtered lines
        # editor.setText("\n".join(filtered_lines))
    else:
        notepad.messageBox("No matching lines found.")

else:
    notepad.messageBox("Error: The selected line does not contain enough columns.")