from Npp import notepad, editor


# Wim Gielis
# Oct. 2025
#
# ReplaceWithTemplate script (Alt-Shift-t):
#       - The entire file is converted, line by line, following a template
#       - Easy to insert text in front and/or at the end
#       - Source: https://isc.sans.edu/diary/31240


def Substitute(contents, lineNumber, totalLines=None):
    contents = str(contents).rstrip('\n\r')
    if contents != '':
        editor.replaceLine(lineNumber, template.replace(token, contents))

def forEachSelectedLine(callback):
    start_line = editor.lineFromPosition(editor.getSelectionStart())
    end_line   = editor.lineFromPosition(editor.getSelectionEnd())
    for line_num in range(start_line, end_line + 1):
        line_text = editor.getLine(line_num)
        callback(line_text, line_num)


# # token = notepad.prompt('Provide a token', 'Substitute token', '#' )
# token = '#'
# template = notepad.prompt('Provide a template', 'Substitute template', '#')
# if token != None and template != None:
    # editor.forEachLine(Substitute)


# token = notepad.prompt('Provide a token', 'Substitute token', '#' )
token = '#'
template = notepad.prompt('Provide a template', 'Substitute template', '#')
if token != None and template != None:
    forEachSelectedLine(Substitute)