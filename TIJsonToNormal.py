from Npp import notepad, editor
import json


LINE_BREAK = "\n"
TAB_SPACES = " " * 4
SECTION_SEPARATOR = LINE_BREAK * 3  # space between different parts in the output
REMOVE_GENERATED_STATEMENTS = True
REMOVE_BEDROCK_HEADER = True


GENERATED_STATEMENTS_BEGIN = "#****Begin: Generated Statements***"
GENERATED_STATEMENTS_END = "#****End: Generated Statements****"
BEDROCK_HEADER_00 = "#" * 97 + " "
BEDROCK_HEADER_01 = "##~~Join the bedrock TM1 community on GitHub https://github.com/cubewise-code/bedrock Ver 4.0 ~~##"
BEDROCK_HEADER_02 = "##~~Join the bedrock TM1 community on GitHub https://github.com/cubewise-code/bedrock-5 Ver 5.0~~##"


# Wim Gielis
# Dec. 2025
#
# TIJsonToNormal script (Ctr-Alt-j):
#       - Reads the entire current tab and parses it as JSON
#       - Extracts these properties: Parameters, Variables, PrologProcedure, MetadataProcedure, DataProcedure, EpilogProcedure
#       - Clears the current tab and outputs the 4 property values


def normalize_code_text(text: str) -> str:
    """
    Normalizes formatting of already-decoded JSON strings.
    """
    if not does_tab_contain_real_code(text):
        text = "# No code in this tab"
    else:

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        if LINE_BREAK != "\n":
            text = text.replace("\n", LINE_BREAK)

        # Tabs to spaces
        text = text.replace("\t", TAB_SPACES)

        # Remove unwanted code
        if REMOVE_GENERATED_STATEMENTS:
            text = text.replace(GENERATED_STATEMENTS_BEGIN + LINE_BREAK, "")
            text = text.replace(GENERATED_STATEMENTS_END + LINE_BREAK, "")

        if REMOVE_BEDROCK_HEADER:
            text = text.replace(BEDROCK_HEADER_00 + LINE_BREAK + BEDROCK_HEADER_01 + LINE_BREAK + BEDROCK_HEADER_00 + LINE_BREAK, "")
            text = text.replace(BEDROCK_HEADER_00 + LINE_BREAK + BEDROCK_HEADER_02 + LINE_BREAK + BEDROCK_HEADER_00 + LINE_BREAK, "")

    return text

def maybe_double_decode(text: str) -> str:
    """
    Decodes text if it looks like JSON-escaped content.
    """
    if "\\n" in text or "\\t" in text:
        try:
            return json.loads(f'"{text}"')
        except Exception:
            pass
    return text

def does_tab_contain_real_code(text: str) -> bool:

    _LINES_TO_IGNORE = [
        GENERATED_STATEMENTS_BEGIN,
        GENERATED_STATEMENTS_END,
        BEDROCK_HEADER_00,
        BEDROCK_HEADER_01,
        BEDROCK_HEADER_02,
    ]

    for line in text.splitlines():
        if line.strip():
            if line.strip() not in _LINES_TO_IGNORE:
                return True

    return False

def format_parameters(items) -> str:
    """
    Formats TM1 Parameters array into readable plain text.
    """

    lines = []
    if not items:
        lines.append("# No parameters for this process")
    else:
        max_parameter_name_length = max((len(i.get("Name", "")) for i in items), default=0)

        for i in items:
            name = i.get("Name", "")
            prompt = i.get("Prompt", "")
            value = i.get("Value", "")
            ptype = i.get("Type", "")

            # Align equals sign for readability
            lines.append(f"[{ptype:<7}] {name:<{max_parameter_name_length + 1}}= {str(value)}    # {prompt}")

    return LINE_BREAK.join(lines)

def format_variables(items) -> str:
    """
    Formats TM1 Variables array into readable plain text.
    """

    lines = []
    if not items:
        lines.append("# No variables for this process")
    else:
        max_position_length = max((len(str(i.get("Position", ""))) for i in items), default=0)

        for i in items:
            name = i.get("Name", "")
            ptype = i.get("Type", "")
            position = i.get("Position", "")

            # Align equals sign for readability
            lines.append(f"[{ptype:<7}] {position:<{max_position_length + 1}}= {name}")

    return LINE_BREAK.join(lines)

def get_header_text(tab_name: str) -> str:
    header  = "#" * 3 + "  "
    header += tab_name.upper()
    header += "  " + "#" * 3
    header += LINE_BREAK * 2
    return header

def main_code() -> bool:

    # Read current document
    raw_text = editor.getText()

    try:
        data = json.loads(raw_text)
    except Exception as e:
        notepad.messageBox(
            "The current document is not valid JSON:\n\n{}".format(e),
            "JSON Error"
        )
        raise

    # Extract procedure values
    _PROCESS_PROPERTIES = [
        "Parameters",
        "Variables",
        "PrologProcedure",
        "MetadataProcedure",
        "DataProcedure",
        "EpilogProcedure"
    ]

    output_blocks = []
    for prop in _PROCESS_PROPERTIES:
        value = None
        if prop.endswith("Procedure"):
            value = data.get(prop, "")
            value = maybe_double_decode(value)
            value = normalize_code_text(value)
        elif prop == 'Parameters':
            value = format_parameters(items=data.get(prop, []))
        elif prop == 'Variables':
            value = format_variables(items=data.get(prop, []))

        if value:
            value = get_header_text(tab_name=prop.replace("Procedure", "")) + value
            output_blocks.append(value)


    # Replace document contents
    editor.beginUndoAction()
    editor.setText(SECTION_SEPARATOR.join(output_blocks))
    editor.endUndoAction()

    # Activate the TM1 language instead of the default JSON
    try:
        notepad.runMenuCommand("Language", "TM1")
    except Exception:
        notepad.messageBox(
            "The TM1 language cannot be activated",
            "Language Error"
        )
        raise

    return True


b = main_code()