from Npp import editor, notepad
import re


# Wim Gielis
# Feb. 2025
#
# DeleteText script (Alt-d):
#       - The selected text is deleted in the whole file
#       - If no text is selected then input is asked from the user. Using this input, a regular expressions way of deleting can be asked:
#         * if the input is re...... and it starts with 're&' then the regex following the 1 is deleted everywhere
#         * all other input is treated as literal text
#       - This script works faster for the regular deletes (literal text),
#         but also for regex, it is faster and has the added benefit that the regex checkbox is not activated in the Find/Replace dialog window.
#       - The script allows for multi-selections, in which case it will be a literal delete of each selected text.
#       - For bigger files (above 1 MB), regex replacements through Notepad++ can be slower. In that case, we use the re module from Python.
#       - Options for delete_mode when single selection delete is done:
#         * delete_mode = -1 ==> no delete
#         * delete_mode =  0 ==> a literal delete
#         * delete_mode =  1 ==> a regex delete
#       - Options for delete_mode when multi-selections delete is done:
#         * delete_mode =  0 ==> a literal delete
#       - Documentation and links:
#         * https://community.notepad-plus-plus.org/topic/26620/search-and-replace-with-pythonscript-compared-to-built-in
#         * https://npppythonscript.sourceforge.net/docs/latest/scintilla.html


PREFIX_REGEX = 're&'


def delete_text(text_pattern: str, delete_mode: int) -> None:

    # delete_mode = 0 ==> literal delete so a literal replace is needed
    # delete_mode = 1 ==> regex delete so a regex replace is needed

    if editor.getLength() < 1_000_000:

        # Start an undo action for a single undo step
        editor.beginUndoAction()

        # Get the current position of the caret to avoid losing position after replacement
        caret_position = editor.getCurrentPos()

        if delete_mode == 0:
            editor.replace(text_pattern, "")

        elif delete_mode == 1:
            editor.rereplace(text_pattern, "")

        # Move caret back to its original position
        editor.gotoPos(caret_position)

        # End the undo action
        editor.endUndoAction()

    else:
        # print("File size too big and switching to the Python re module: " + str(editor.getLength))
        full_text = editor.getText()

        if delete_mode == 0:
            editor.setText(full_text.replace(text_pattern, ""))
            # the code below is much slower (physically selects all instances and hits Del on the keyboard)
            # 42090 = Ignore Case & Whole Word, in the file: C:\Program Files\Notepad++\localization\english.xml
            # advantage could be an easy way to delete let's say the word 'the' but as a full word, instead of deleting 'the' in 'atheism'
            # caret_position = editor.getCurrentPos()
            # notepad.menuCommand(42090)
            # editor.clear()
            # editor.gotoPos(caret_position)

        elif delete_mode == 1:
            editor.setText(re.sub(text_pattern, "", full_text))

# Get the selected area(s) and the selected text(s)
num_selections = editor.getSelections()
if num_selections == 1:
    delete_mode = 0
    selected_text = editor.getSelText()

    # Ensure there is some selected text (or we go for a regex delete)
    if not selected_text:
        # Ask the user for input
        selected_text = notepad.prompt("Please enter the text to be deleted from the active file\n(suffix 1 for a regex delete, otherwise a literal delete)", "User input", "")

        if selected_text is None:
            # the user canceled the prompt
            delete_mode = -1
        elif not selected_text:
            # the user entered nothing
            delete_mode = -1
        elif selected_text.startswith(PREFIX_REGEX):
            # prefix 1 means a regex delete
            delete_mode = 1
            selected_text = selected_text[len(PREFIX_REGEX):]
        else:
            # default case is a literal delete
            delete_mode = 0

    if delete_mode > -1:
        delete_text(selected_text, delete_mode)

else:
    selected_texts = []

    # Multiple selections are done
    for i in range(num_selections):

        # Get each time the selected text
        start = editor.getSelectionNStart(i)
        end = editor.getSelectionNEnd(i)
        if end > start:
            selected_text = editor.getTextRange(start, end)
            if selected_text:
                selected_texts.append(selected_text)

    for selected_text in selected_texts:
        delete_text(selected_text, 0)

    # if we want to process in 1 go (as regex in that case, but optionally, escaped for special characters):
    # if selected_texts:
        # delete_text('|'.join(selected_texts), 1)
        # delete_text('|'.join(re.escape(item) for item in selected_texts), 1)