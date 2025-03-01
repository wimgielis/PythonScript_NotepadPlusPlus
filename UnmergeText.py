from Npp import notepad, editor


# Wim Gielis
# Mar. 2025
#
# UnmergeText script (Alt-e):
#       - The selected text is unmerged with a chosen separator
#       - For the separator, we first inspect the selected text. If not good candidate is found, the user should enter a separator.


# Get the selection start position
selection_start = editor.getSelectionStart()

# Get the selected lines of text
selected_text = editor.getSelText()

# If there is no selection, do nothing
if not selected_text.strip():
    notepad.messageBox("Please select the text to unmerge!", "Unmerge Text", 0)
else:

    # Define the separator you want between merged lines
    separator = next((sep for sep in ['\t',', ', ',', '|', '+ ', '+'] if selected_text.count(sep) > 2), '')
    separator = notepad.prompt("Please enter the separator (1 is comma, 2 is pipe, 3 is plus sign)", "Separator", separator)

    if not separator is None:
        # the user did not cancel the prompt

        # if separator:
            # # the user provided a separator

        if separator == '1':
            separator = ', '
        elif separator == '2':
            separator = '|'
        elif separator == '3':
            separator = ' + '

        # Unmerge the selected text based on user's choice
        if separator in selected_text:
            unmerged_text = selected_text.split(separator)
            unmerged = 1
        elif separator.strip() in selected_text:
            unmerged_text = selected_text.split(separator.strip())
            unmerged = 1
        else:
            unmerged = 0

        if unmerged == 1:
            # Replace the selected text with the merged version
            editor.replaceSel('\n'.join(unmerged_text))

            # Move the cursor back to the start of the original selection
            editor.setSelection(selection_start, selection_start)