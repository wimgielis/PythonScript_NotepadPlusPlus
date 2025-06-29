from Npp import editor, notepad
import re


# Wim Gielis
# Jun. 2025
#
# TM1Tools script (Alt-f):
#       There are 4 tools, which one you want is asked in the prompt
#       * if you choose "empty lines" (or "1") in the prompt
#       - We remove all lines that are completely empty. This is to correct MDX editor issues where additional whitespace is added time and time again.
#       * if you choose "caret" (or "2") in the prompt
#       - We search for strings with a caret character (^) in it. It should only be inside square brackets.
#       - In addition, the square brackets must follow 1 or 2 square bracketed text
#       - Then we remove anything inside the square brackets in front of (and including) the last caret.
#       * if you choose "remove" (or "3") or "add" (or "4") in the prompt
#       - For TM1 rules and feeders syntax, we either add or remove the hierarchy notation
#       - only the dim:elem notation remains when removing text
#       - the full dim:hier:elem notation is used when adding text


# Start an undo action for a single undo step
editor.beginUndoAction()

# Get selected text
selected_text = editor.getSelText()

# Ask user for action: remove or add text
action = notepad.prompt("Which option? 1/empty lines = Remove empty lines. 2/caret = remove the text left of carets. 3/remove = remove hierarchy notation inside brackets. 4/add = add hier notation.", "Option", "empty lines")

def clean_part(part, strip_quotes: bool = True, in_lower_case: bool = True):
    """Remove outer single quotes, strip spaces, lowercase"""
    part = part.strip(" \t")
    if strip_quotes:
        part = part.strip("'\"")
    if in_lower_case:
        return part.lower()
    else:
        return part

def process_element(element):
    """Check one comma-separated element"""
    parts = element.split(':')
    if len(parts) == 3:
        first = clean_part(parts[0])
        second = clean_part(parts[1])
        if first == second:
            return ':'.join(parts[1:])  # Remove first + colon
    return element

def replacer_remove(match):
    content = match.group(1)
    # Split by commas, keeping any surrounding spaces
    elements = re.split(r'\s*,\s*', content)
    processed = [process_element(el) for el in elements]
    # Join back with ', ' to preserve typical style
    new_content = ', '.join(processed)
    return f'[{new_content}]'

def replacer_add(match):
    content = match.group(1)
    # Split by commas, keeping any surrounding spaces
    elements = re.split(r'\s*,\s*', content)
    new_elements = []

    for element in elements:
        parts = element.split(':')
        if len(parts) == 2:
            first = clean_part(parts[0], in_lower_case=False)
            # Add the first part back after the opening square bracket
            new_elements.append(f"'{first}':" + element)
        else:
            # If no colon, keep as is
            new_elements.append(element)
    
    # Join the elements back with commas
    new_content = ', '.join(new_elements)
    return f'[{new_content}]'

# Apply the chosen action (remove or add)
if not action:
    notepad.messageBox("Ok good, no action needed", "Information", 0)

elif action == "1" or action.upper() == "EMPTY LINES":
    editor.rereplace(r"^\s*\r?\n", r"")

elif action == "2" or action.upper() == "CARET":
    
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

        # Do we still have carets ?
        caret_count = len(re.findall(r'\^', editor.getText()))
        if caret_count == 1:
            notepad.messageBox(f"There is still 1 caret in the text.", "Caret Count", 0)
        elif caret_count > 1:
            notepad.messageBox(f"There are still {caret_count} carets in the text.", "Caret Count", 0)

elif action == "3" or action.upper() == "REMOVE":

    pattern = re.compile(r'\[(.*?)\]', re.DOTALL)
    result = pattern.sub(replacer_remove, selected_text)
    # Replace selection with processed text
    editor.replaceSel(result)

elif action == "4" or action.upper() == "ADD":

    pattern = re.compile(r'\[(.*?)\]', re.DOTALL)
    result = pattern.sub(replacer_add, selected_text)
    # Replace selection with processed text
    editor.replaceSel(result)

else:
    notepad.messageBox("Invalid action. Please type '1/2/3/4' or 'empty lines/caret/remove/add'.", "Error", 0)

# Copy all text to the Windows clipboard
editor.copyText(editor.getText())

# End the undo action
editor.endUndoAction()