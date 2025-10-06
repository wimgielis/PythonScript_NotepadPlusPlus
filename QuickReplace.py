from Npp import notepad, editor


# Wim Gielis
# Sep. 2025
#
# QuickReplace script (Alt-v):
#       - The selected text is replaced
#       - If not text is selected then the user is asked to enter the text
#       - Enter the replacement too
#       - Regular expression replace is not supported


# Use selection as default "find", or empty if nothing selected
sel_text = editor.getSelText()
find_text = sel_text if sel_text else ""

do_continue = True

# Ask for text to find
if not find_text:
    find_text = notepad.prompt("Enter text to find:", "Simple Replace", find_text)

if not find_text:
    notepad.messageBox("No find text entered. Aborted.", "Simple Replace")
    do_continue = False

if do_continue:
    # Ask for replacement text
    replace_text = notepad.prompt(f"Replace '{find_text}' with:", "Simple Replace", find_text)
    if replace_text is None:
        notepad.messageBox("Aborted.", "Simple Replace")
        do_continue = False

if do_continue:
    # Replace in the whole document
    text = editor.getText()
    text_new = text.replace(find_text, replace_text)

    if text != text_new:
        editor.setText(text_new)


# If case-insensitive:
# import re
# from Npp import editor, notepad

# # ... (keep your prompt code as before)

# # Replace in the whole document, case-insensitive
# pattern = re.compile(re.escape(find_text), re.IGNORECASE)
# text = editor.getText()
# text_new, count = pattern.subn(replace_text, text)  # subn returns (new_text, number_of_replacements)

# if count > 0:
    # editor.setText(text_new)
    # notepad.messageBox(f"Replaced {count} occurrence(s) of '{find_text}' (case-insensitive).", "Simple Replace")
# else:
    # notepad.messageBox(f"No occurrences of '{find_text}' found.", "Simple Replace")