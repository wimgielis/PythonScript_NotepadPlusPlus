from Npp import editor, notepad
import re


# Wim Gielis
# Mar. 2025
#
# SearchTextDeleteLine script (Alt-l):
#       - The text in a prompt is searched in the entire file
#       - The default string in the pattern is the selected text (if any) when the script is launched.
#       - All lines where the text occurs, are removed.
#       - A regex pattern is allowed: in the prompt, start the string with re& (add it in front)


PREFIX_REGEX = 're&'


selected_text = editor.getSelText()

if selected_text:
    if '\t' in selected_text:
        selected_text = f"{PREFIX_REGEX}{selected_text.replace('\t', r'\t')}"

# Prompt user for the search text (supports regex)
search_text = notepad.prompt("Enter the literal or regex or extended search pattern:", "Delete Lines Containing Text", selected_text)

# If user cancels or enters nothing, exit
if not search_text:
    exit()

# Literal or regex search ?
search_regex = search_text.startswith(PREFIX_REGEX)

# Get the entire text of the document
editor.beginUndoAction()
try:
    text = editor.getText()
    lines = text.splitlines(keepends=True)
    if search_regex:
        # Remove matching lines based on a regex pattern
        # Compile the regex pattern for efficiency
        search_text = search_text[len(PREFIX_REGEX):]
        pattern = re.compile(search_text)
        new_text = ''.join(line for line in lines if not pattern.search(line))
    else:
        # Remove matching lines based on a literal pattern
        new_text = ''.join(line for line in lines if search_text not in line)
    editor.setText(new_text)
finally:
    editor.endUndoAction()