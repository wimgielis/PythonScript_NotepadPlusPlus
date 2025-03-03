10 useful scripts for usage in Notepad++. Setup first is needed to have PythonScript in Notepad++
After that, it becomes really powerful.

Wim Gielis
Q1 2025


- MergeLines.py (alt-m):
Select lines and choose a separator. I could not find the same functionality in Notepad++ but maybe I overlooked. The separator is stored in an ini file.

- SplitText.py (alt-e):
The inverse operation of MergeLines. A custom separator can be derived and if not found, chosen. The separator is stored in an ini file.

- DeleteText.py (alt-d):
Select text, press Alt-d and in the whole file it will be removed. Much faster than Replace with an empty string and making sure the checkbox with regex/normal/extended is right, etc.

- DuplicateTab.py (alt-t):
Duplicate the text in the current tab as a new tab, immediately to the right and enable the same language syntax (if any)

- SaveAllTabs.py (alt-s):
A loop through all open tabs. If unsaved, the code saves the tab if already saved earlier. If not yet saved, it is writting in a hardcoded folder on the hard drive.

- IndentText.py (alt-i):
The selected text is indented. We add 4 spaces to the beginning of every non-empty line. (Empty lines are unaffected)

- UnindentText.py (alt-shift-i):
The selected text is unindented. We remove 4 spaces from the beginning of every non-empty line.

- CleanUpSpaces.py (alt-p):
The selected text is trimmed for the trailing whitespace. Then we convert leading tabs to 4 spaces. Lastly, multiples of 3 spaces are converted to the same multiple of 4 spaces.

- SearchTextDeleteLine.py (alt-l):
Search a text (literal or regex) and all lines in the file where the search string occurs, will be removed. The selected text is presented as the choice of search string. Very useful in data text files or log files.

- SearchTextKeepLine.py (alt-l):
Search a text (literal or regex) and all lines in the file where the search string occurs, will be kept. The selected text is presented as the choice of search string. Very useful in data text files or log files.

- AddArrows.py (alt-a):
Probably only useful to me :-) Serves a specific purpose of adding ==> text in the empty lines between paragraphes of text copied from an email.
