from Npp import editor, notepad
import re


# Wim Gielis
# Mar. 2025
#
# SearchTextKeepLine script (Alt-k):
#       - The text in a prompt is searched in the entire file
#       - The default string in the pattern is the selected text (if any) when the script is launched.
#       - All lines where the text occurs, are kept. The other lines are removed.
#       - A regex pattern is allowed: in the prompt, start the string with re& (add it in front)
#       - When lines are deleted, the header row is preserved.


PREFIX_REGEX = 're&'


def get_separator(line):
    # Common separators: comma, semicolon, tab, pipe
    separators = ['\t', ';', ',', '|', '#']
    separator_counts = {sep: line.count(sep) for sep in separators}
    # Return the separator with the highest count
    return max(separator_counts, key=separator_counts.get)

def detect_data_type(value):
    # if re.match(r"^\d+$", value):
    if re.match(r"^-?(\d+ ?)+\d+-?$", value):
        return 'int'
    elif re.match(r"^-?(\d+[., ]?)+\d+-?$", value):
        return 'float'
    elif re.match(r"^(3[01]|2\d|1\d|0\d|\d)([ -\/]?)(0[1-9]|[1-9]|1[0-2]|[a-zA-Z]{3})([ -\/]?)(\d{4})$", value):
        # dd/mm(m)/yyyy   nothing or dash instead of forward slash also allowed
        return 'date'
    elif re.match(r"^(0[1-9]|[1-9]|1[0-2]|[a-zA-Z]{3})([ -\/]?)(3[01]|2\d|1\d|0\d|\d)([ -\/]?)(\d{4})$", value):
        # mm(m)/dd/yyyy   nothing or dash instead of forward slash also allowed
        return 'date'
    elif re.match(r"^(\d{4})([ -\/]?)(0[1-9]|[1-9]|1[0-2]|[a-zA-Z]{3})([ -\/]?)(3[01]|2\d|1\d|0\d|\d)$", value):
        # yyyy/mm(m)/dd   nothing or dash instead of forward slash also allowed
        return 'date'
    elif value == "":
        return 'empty'
    else:
        return 'str'

def detect_header_row(lines) -> bool:
    separator = get_separator(lines[0])
    potential_header_count = 0
    previous_data_types = None

    for line in lines:
        fields = line.strip().split(separator)
        data_types = [detect_data_type(field.strip()) for field in fields]

        if previous_data_types is None:
            previous_data_types = data_types
        else:
            # If current line's data types differ significantly from previous line's data types
            return previous_data_types != data_types


selected_text = editor.getSelText()

if selected_text:
    if '\t' in selected_text:
        selected_text = f"{PREFIX_REGEX}{selected_text.replace('\t', r'\t')}"

# Prompt user for the search text (supports regex)
search_text = notepad.prompt("Enter the literal or regex or extended search pattern:", "Keep Lines Containing Text", selected_text)

# If user cancels or enters nothing, do nothing
if search_text:

    # Literal or regex search ?
    search_regex = search_text.startswith(PREFIX_REGEX)

    # Get the entire text of the document
    editor.beginUndoAction()
    try:
        text = editor.getText()
        lines = text.splitlines(keepends=True)
        if lines:
            # Do we have a header row ?
            # If yes, retain it and process 1 line less
            header_row_exists = detect_header_row(lines)
            if header_row_exists:
                new_text = lines[0]
                lines = lines[1:]
            else:
                new_text = ''

            if search_regex:
                # Remove matching lines based on a regex pattern
                # Compile the regex pattern for efficiency
                search_text = search_text[len(PREFIX_REGEX):]
                pattern = re.compile(search_text)
                new_text += ''.join(line for line in lines if pattern.search(line))
            else:
                # Remove matching lines based on a literal pattern
                new_text += ''.join(line for line in lines if search_text in line)

            editor.setText(new_text)

    finally:
        editor.endUndoAction()