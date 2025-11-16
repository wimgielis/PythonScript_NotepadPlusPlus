from Npp import editor, notepad, MESSAGEBOXFLAGS
import re
import os


# Wim Gielis
# Nov. 2025
#
# ReplaceGibberishWithTM1rules script (no shortcut, launch from the menu):
#       - Lines for code 565 are replaced with something fixed like TM1rules


TARGET_DIR = r"D:\OneDrive - Aexis Belgium NV\Wim\TM1\TI processes"

# Regex: line beginning with 565,"..." and we capture the gibberish part in the middle
PATTERN = re.compile(r'^565,"([^"]*)"$', re.IGNORECASE)

# Function to find matching files
def find_matching_files():
    matching_files = []

    for root, _, files in os.walk(TARGET_DIR):
        for file in files:

            # Process only my own TI processes
            if file.lower().endswith(".pro"):
                if not file.startswith("}bedrock"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        lines = f.readlines()

                        line_num = 0
                        for line in lines:
                            line_num += 1

                            if line_num <= 10:
                                match = pattern.match(line.rstrip("\r\n"))
                                if match:
                                    inside = match.group(1)
                                    if inside != "TM1rules":
                                        matching_files.append(file_path)

    return matching_files


files_to_keep = find_matching_files()
if not files_to_keep:
    notepad.messageBox( "No gibberish found in the TM1 data directory.", "No hits", MESSAGEBOXFLAGS.OK )
else:
    change_count = 0
    for file_to_change in files_to_keep:

        with open(file_to_change, "r") as f:
            lines = f.readlines()

        modified = False
        new_lines = []
        line_num = 0

        for line in lines:
            line_num += 1

            if line_num <= max_lines:
                m = pattern.match(line.rstrip("\r\n"))
                if m:
                    inside = m.group(1)

                    if inside != "TM1rules":
                        # Build the new line, preserving EOL
                        eol = line[len(line.rstrip("\r\n")):]
                        line = '565,"TM1rules"' + eol
                        modified = True
                        change_count += 1

            new_lines.append(line)

        # Only rewrite if needed
        if modified:
            with open(file_to_change, "w") as f:
                f.writelines(new_lines)

    # Final result
    notepad.messageBox( "Number of processes changed: " + str(change_count) + '\r\n\r\n' + '\r\n'.join([s.replace(TARGET_DIR + "\\", " -  ").replace(".pro", "") for s in files_to_keep]), "Number of hits", MESSAGEBOXFLAGS.OK )