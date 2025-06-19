from Npp import editor
import re


# Wim Gielis
# Jun. 2025
#
# TM1NoHierarchyNotation script (Alt-q):
#       - For TM1 rules and feeders syntax, we remove the hierarchy notation
#       - only the dim:elem notation remains


# Start an undo action for a single undo step
editor.beginUndoAction()

# Get selected text
selected_text = editor.getSelText()

# Regex to match [ ... ]
pattern = re.compile(r'\[(.*?)\]', re.DOTALL)

def clean_part(part):
    """Remove outer single quotes, strip spaces, lowercase"""
    part = part.strip()
    if part.startswith("'") and part.endswith("'") and len(part) >= 2:
        part = part[1:-1]
    return part.strip().lower()

def process_element(element):
    """Check one comma-separated element"""
    parts = element.split(':')
    if len(parts) == 3:
        first = clean_part(parts[0])
        second = clean_part(parts[1])
        if first == second:
            return ':'.join(parts[1:])  # Remove first + colon
    return element

def replacer(match):
    content = match.group(1)
    # Split by commas, keeping any surrounding spaces
    elements = re.split(r'\s*,\s*', content)
    processed = [process_element(el) for el in elements]
    # Join back with ', ' to preserve typical style
    new_content = ', '.join(processed)
    return f'[{new_content}]'

# Apply substitution
result = pattern.sub(replacer, selected_text)

# Replace selection with processed text
editor.replaceSel(result)

# End the undo action
editor.endUndoAction()