from Npp import editor
import re


# Wim Gielis
# Sep. 2026
#
# RemoveTextWithTags script (Ctrl-...):
#       - Delete the complete element containing the caret, or whose opening/closing tag is selected.
#       - HTML and XML supported
#       - The line is also deleted if only whitespace remains after the initial delete operation.
#
# Examples:
#
#   <div>Some text</div>
#       ^ caret in either tag -> deletes the whole div
#
#   <div>
#       <span>Hello</span>
#   </div>
#       ^ caret in span tag -> deletes only the span
#
# Handles:
#   - Nested tags
#   - Attributes containing > characters
#   - HTML and XML
#   - Comments
#   - CDATA
#   - Processing instructions
#   - Self-closing tags
#
# HTML tag names are matched case-insensitively.
# XML tag names are effectively matched case-insensitively too.
# If strict XML case sensitivity is required, see the note below.

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# HTML void elements have no closing tag.
# If the caret is inside one of these, the tag itself is deleted.
HTML_VOID_TAGS = set(["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"])

# ----------------------------------------------------------------------
# Find all tags in the document
# ----------------------------------------------------------------------
def find_tags(text):
    """
    Return a list of tag records.

    Each record is:
        {
            "start":  start position,
            "end":    end position (exclusive),
            "name":    tag name,
            "type":    "open", "close", "self"
        }

    Comments, CDATA, declarations and processing instructions are skipped.
    """

    tags = []

    length = len(text)
    i = 0

    while i < length:

        # --------------------------------------------------------------
        # HTML/XML comment
        # --------------------------------------------------------------
        if text.startswith("<!--", i):
            end = text.find("-->", i + 4)

            if end == -1:
                break

            i = end + 3
            continue

        # --------------------------------------------------------------
        # CDATA
        # --------------------------------------------------------------
        if text.startswith("<![CDATA[", i):
            end = text.find("]]>", i + 9)

            if end == -1:
                break

            i = end + 3
            continue

        # --------------------------------------------------------------
        # Processing instruction
        # <?xml ... ?>
        # --------------------------------------------------------------
        if text.startswith("<?", i):
            end = text.find("?>", i + 2)

            if end == -1:
                break

            i = end + 2
            continue

        # --------------------------------------------------------------
        # DOCTYPE / declarations
        # <!DOCTYPE ...>
        # --------------------------------------------------------------
        if text.startswith("<!", i):
            end = find_tag_end(text, i)

            if end == -1:
                break

            i = end + 1
            continue

        # --------------------------------------------------------------
        # Normal tag
        # --------------------------------------------------------------
        if text[i] == "<":

            # Closing tag
            if i + 1 < length and text[i + 1] == "/":
                match = re.match(r'<\s*/\s*([A-Za-z_][\w:.-]*)', text[i:])

                if match:
                    name = match.group(1)

                    end = find_tag_end(text, i)

                    if end != -1:
                        tags.append({
                            "start": i,
                            "end": end + 1,
                            "name": name.lower(),
                            "type": "close"
                        })

                        i = end + 1
                        continue

            # Opening tag
            else:
                match = re.match(r'<\s*([A-Za-z_][\w:.-]*)', text[i:])

                if match:
                    name = match.group(1)
                    end = find_tag_end(text, i)

                    if end != -1:

                        tag_text = text[i:end + 1]

                        # Determine whether it is explicitly self-closing.
                        # Ignore whitespace before >.
                        self_closing = bool(re.search(r'/\s*>$', tag_text))

                        # HTML void elements are also effectively
                        # self-closing.
                        if name.lower() in HTML_VOID_TAGS:
                            self_closing = True

                        tags.append({
                            "start": i,
                            "end": end + 1,
                            "name": name.lower(),
                            "type": "self" if self_closing else "open"
                        })

                        i = end + 1
                        continue

        i += 1

    return tags

# ----------------------------------------------------------------------
# Find the end of a tag while respecting quoted attributes
# ----------------------------------------------------------------------

def find_tag_end(text, start):
    """
    Find the '>' ending a tag.

    A '>' inside a quoted attribute does not terminate the tag.

    Example:
        <div title="a > b">

    The correct ending is the second '>'.
    """

    quote = None
    i = start + 1
    length = len(text)

    while i < length:
        ch = text[i]

        if quote:
            if ch == quote:
                quote = None

        else:
            if ch == '"' or ch == "'":
                quote = ch

            elif ch == ">":
                return i

        i += 1

    return -1

# ----------------------------------------------------------------------
# Match opening and closing tags
# ----------------------------------------------------------------------
def build_pairs(tags):
    """
    Match opening and closing tags using a stack.

    Returns:
        open_to_close
        close_to_open

    where the values are tag indexes.
    """

    open_to_close = {}
    close_to_open = {}

    stack = []

    for index, tag in enumerate(tags):

        if tag["type"] == "open":
            stack.append(index)

        elif tag["type"] == "self":
            # No matching closing tag.
            pass

        elif tag["type"] == "close":

            # Search backwards for the most recent matching opening tag.
            match_index = -1

            for j in range(len(stack) - 1, -1, -1):
                candidate = stack[j]

                if tags[candidate]["name"] == tag["name"]:
                    match_index = candidate
                    break

            if match_index != -1:

                # Remove the matched opening tag and anything above it.
                #
                # Normally everything above it should already have
                # matched. This also makes the routine reasonably
                # tolerant of malformed HTML.
                stack = stack[:match_index]

                open_to_close[match_index] = index
                close_to_open[index] = match_index

    return open_to_close, close_to_open

# ----------------------------------------------------------------------
# Determine which tag the caret/selection is inside
# ----------------------------------------------------------------------
def find_selected_or_current_tag(tags, selection_start, selection_end):
    """
    Find the tag containing the caret or selection.

    A tag is considered selected if:

        selection_start >= tag.start
        selection_end   <= tag.end

    We also accept overlap, which makes the script more forgiving.
    """

    # First preference: a tag completely containing the selection.
    candidates = []

    for index, tag in enumerate(tags):

        if selection_start >= tag["start"] and \
           selection_end <= tag["end"]:

            candidates.append(index)

    if candidates:
        # Normally only one tag can contain another because tags
        # themselves cannot be nested.
        return candidates[-1]


    # If the selection/caret overlaps the tag, use that too.
    for index, tag in enumerate(tags):

        if selection_start < tag["end"] and \
           selection_end > tag["start"]:

            return index

    return None

# ----------------------------------------------------------------------
# Main operation
# ----------------------------------------------------------------------
def delete_current_element():

    text = editor.getText()

    if not text:
        return

    selection_start = editor.getSelectionStart()
    selection_end = editor.getSelectionEnd()

    tags = find_tags(text)

    if not tags:
        notepad.messageBox("No HTML/XML tag was found at the cursor.", "Delete Element")
        return

    # --------------------------------------------------------------
    # Identify the tag under the cursor/selection
    # --------------------------------------------------------------
    tag_index = find_selected_or_current_tag(
        tags,
        selection_start,
        selection_end
    )

    if tag_index is None:

        notepad.messageBox("The cursor or selection is not inside an HTML/XML tag.", "Delete Element")
        return

    open_to_close, close_to_open = build_pairs(tags)
    tag = tags[tag_index]

    # --------------------------------------------------------------
    # Opening tag
    # --------------------------------------------------------------
    if tag["type"] == "open":

        if tag_index in open_to_close:

            close_index = open_to_close[tag_index]

            start = tags[tag_index]["start"]
            end = tags[close_index]["end"]

        else:
            # Unmatched opening tag.
            #
            # Rather than deleting arbitrary document contents, delete
            # only the tag itself.
            start = tag["start"]
            end = tag["end"]

    # --------------------------------------------------------------
    # Closing tag
    # --------------------------------------------------------------

    elif tag["type"] == "close":

        if tag_index in close_to_open:

            open_index = close_to_open[tag_index]

            start = tags[open_index]["start"]
            end = tag["end"]

        else:
            # Unmatched closing tag.
            start = tag["start"]
            end = tag["end"]

    # --------------------------------------------------------------
    # Self-closing tag / HTML void element
    # --------------------------------------------------------------

    else:

        start = tag["start"]
        end = tag["end"]

    # --------------------------------------------------------------
    # Delete the complete range
    # --------------------------------------------------------------

    editor.beginUndoAction()

    try:
        editor.setSelection(start, end)
        editor.replaceSel("")

        # ----------------------------------------------------------
        # If the resulting line contains only spaces/tabs, 
        # delete the entire line as well.
        # ----------------------------------------------------------

        # Get the position of the caret after the deletion.
        pos = editor.getCurrentPos()

        line = editor.lineFromPosition(pos)

        line_start = editor.positionFromLine(line)
        line_end = editor.getLineEndPosition(line)

        # Get the remaining contents of the line.
        remaining = editor.getTextRange(line_start, line_end)

        # Only spaces and tabs are considered whitespace here.
        if remaining.strip(" \t") == "":

            # Select the entire line including its line ending.
            editor.setSelection(line_start, editor.getLineEndPosition(line))

            # Include the line ending if there is one.
            if line < editor.getLineCount() - 1:
                editor.gotoLine(line)
                editor.home()
                editor.lineDelete()

            else:
                # Last line: just remove its remaining whitespace.
                editor.replaceSel("")

    finally:
        editor.endUndoAction()

# ----------------------------------------------------------------------
# Run it
# ----------------------------------------------------------------------
delete_current_element()