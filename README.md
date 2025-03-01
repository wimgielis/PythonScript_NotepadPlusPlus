6 useful scripts for usage in Notepad++. Setup first is needed to have PythonScript in Notepad++
After that, it becomes really powerful.

Wim Gielis
Q1 2025


MergeLines.py (Alt-m):
select lines and choose a separator. I could not find the same functionality in Notepad++ but maybe I overlooked.

UnmergeText.py (Alt-e):
the inverse operation or MergeLines. A customer separator can be derived and if not found, chosen.

DeleteText.py (Alt-d):
select text, press Alt-d and in the whole file it will be removed. Much faster than Replace with an empty string and making sure the checkbox with regex/normal/extended is right, etc.

DuplicateTab.py (Alt-t):
Duplicate the text in the current tab as a new tab, immediately to the right and enable the same language syntax (if any)

SaveAllTabs.py (Alt-s):
a loop through all open tabs. If unsaved, the code saves the tab if already saved earlier. If not yet saved, it is writting in a hardcoded folder on the hard drive.

IndentCode.py (Alt-i):
The selected text is indented. We add 4 spaces to the beginning of every non-empty line. (Empty lines are unaffected)

UnindentCode.py (Alt-Shift-i):
The selected text is unindented. We remove 4 spaces from the beginning of every non-empty line.

CleanUpSpaces.py (Alt-p):
The selected text is trimmed for the trailing whitespace. Then we convert leading tabs to 4 spaces. Lastly, multiples of 3 spaces are converted to the same multiple of 4 spaces.

AddArrows.py (Alt-a):
Probably only useful to me :-) Serves a specific purpose of adding ==> text in the empty lines between paragraphes of text copied from an email.
