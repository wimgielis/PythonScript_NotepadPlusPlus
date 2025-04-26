from Npp import editor


# Wim Gielis
# Apr. 2025
#
# TreatEmailText script (Alt-a):
#       - Select all the text in the selected file, it is coming from a copy/paste of email messages
#       - Remove unnecessary text like the signature and the timestamp of sending the email

#       - Also, if wanted:
#         * delete all lines that contain the word Wim.
#         * for every line that is ONLY a space character and nothing else, in front we add an arrow
#         * the cursor is put after the first arrow, for quick editing.


# Get the editor object
editor.beginUndoAction()



clean_up_emails = notepad.prompt("Do you want to clean up the email text ? (YN)", "Clean up email text", "Y")

if clean_up_emails == 'Y':
    
    try:

        # Select all text
        editor.selectAll()
        all_text = editor.getText()

        # Split into lines and process
        lines = all_text.splitlines()
        new_lines = []

        for line in lines:
            # Skip certain lines
            if line == 'Best regards / Beste groeten,':
                continue
            if line == 'Wim Gielis':
                continue
            if line.startswith('IBM Champion 20'):
                continue
            if line.startswith('MS Excel MVP 20'):
                continue
            if line == 'https://www.wimgielis.com':
                continue
            if 'Wim Gielis <wim.gielis@gmail.com>' in line:
                continue
            if 'minuten geleden' in line:
                continue
            if 'uur geleden' in line:
                continue
            if line.strip() == '':
                continue
            if line.strip() == 'Inbox':
                continue
            if line == '------':
                continue

            if line == 'aan mij':
                line = ''

            new_lines.append(line)
            new_text = '\r\n'.join(new_lines)
            editor.setText(new_text)

    finally:
        editor.endUndoAction()



add_arrows = notepad.prompt("Do you want to add arrows to the text ? (YN)", "Add arrows", "N")

if add_arrows == 'Y':

    try:
        # Select all text
        editor.selectAll()
        all_text = editor.getText()

        # Split into lines and process
        lines = all_text.splitlines()
        new_lines = []

        for line in lines:
            # Skip certain lines
            # if 'Wim' in line:
            #     continue
            if line == 'Neil':
                continue

            # A line with only a space gets an arrow
            # But only when there is already text (the greeting is ignored and does not need an arrow)
            elif line == ' ':
                if new_lines:
                    new_lines.append('==> ')
            elif line.strip() == '':
                if new_lines:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # Add an extra arrow, unless the last line contains the word 'hopefully'
        if not (new_lines and any(keyword in lines[-1].strip().lower() for keyword in ['hopefully', 'neil'])):
            new_lines = new_lines + ['', '==> ']

        # A greeting
        new_lines = ["Hi Neil,", "", "I hope you're good.", ""] + new_lines

        # Replace text
        new_lines = [l.replace(".  ", ". ") for l in new_lines]
        new_lines = [l.replace("?  ", "? ") for l in new_lines]
        new_lines = [l.replace("!  ", "! ") for l in new_lines]

        # Join the processed lines back together
        new_text = '\r\n'.join(new_lines)

        # Replace the content in the editor
        editor.setText(new_text)

        # Find the position of the first arrow and move the cursor there
        arrow_pos = new_text.find('==> ')
        if arrow_pos != -1:
            editor.gotoPos(arrow_pos + 6)
        else:
            editor.gotoPos(0)

    finally:
        editor.endUndoAction()