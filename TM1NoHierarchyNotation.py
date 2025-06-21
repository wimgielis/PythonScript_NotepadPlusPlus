from Npp import editor
import re


# Wim Gielis
# Jun. 2025
#
# TM1NoHierarchyNotation script (Alt-f):
#       - For TM1 rules and feeders syntax, we either add or remove the hierarchy notation
#       - only the dim:elem notation remains when removing text
#       - the full dim:hier:elem notation is used when adding text


# Start an undo action for a single undo step
editor.beginUndoAction()

# Get selected text
selected_text = editor.getSelText()

# Ask user for action: remove or add text
action = notepad.prompt("Do you want to remove text or add text inside the brackets? Type 'remove' or 'add':", "Remove or Add", "remove")

# Regex to match [ ... ]
pattern = re.compile(r'\[(.*?)\]', re.DOTALL)

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
if action.upper() == "REMOVE":
    result = pattern.sub(replacer_remove, selected_text)
elif action.upper() == "ADD":
    result = pattern.sub(replacer_add, selected_text)
else:
    editor.messageBox("Invalid action. Please type 'remove' or 'add'.", "Error", 0)

# Replace selection with processed text
editor.replaceSel(result)

# End the undo action
editor.endUndoAction()