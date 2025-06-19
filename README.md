Many useful scripts for usage in Notepad++. Setup first is needed to have PythonScript in Notepad++
After that, it becomes really powerful.

Wim Gielis
HY1 2025


- MergeLines.py (alt-m):
Select lines and choose a separator. I could not find the same functionality in Notepad++ but maybe I overlooked. The separator is stored in an ini file.

- SplitText.py (alt-e):
The inverse operation of MergeLines. A custom separator can be derived and if not found, chosen. The separator is stored in an ini file.

- DeleteText.py (alt-d):
Select text, press Alt-d and in the whole file it will be removed. Much faster than Replace with an empty string and making sure the checkbox with regex/normal/extended is right, etc.

- DuplicateTab.py (alt-t):
Duplicate the text in the current tab as a new tab, immediately to the right and enable the same language syntax (if any)

- DeleteTab (alt-del):
Delete the tab (the file if it was already saved) or close without changes (it not yet saved).

- BulletText (alt-b):
Add bullets to the selected lines (- ... so a hyphen and a space in front)

- SaveTab (alt-x):
Tab to space, trim trailing space, then save the file (if needed, write to disk), reload the file

- SaveAllTabs.py (alt-s):
A loop through all open tabs. If unsaved, the code saves the tab if already saved earlier. If not yet saved, it is writting in a hardcoded folder on the hard drive.

- IndentText.py (alt-i):
The selected text is indented. We add 4 spaces to the beginning of every non-empty line. (Empty lines are unaffected)

- UnindentText.py (alt-shift-i):
The selected text is unindented. We remove 4 spaces from the beginning of every non-empty line.

- IndentTIAndRules.py (alt-F11):
The selected text is changed from multiples of 3 spaces to multiples of 4 spaces (customizable). Lines that deviate can be flagged. Target is probably TI processes and rules files.

- SelectLastCharacter (alt-F12):
For the selected text, select each time after the last character (not the EOL character). Adding text to lines with variable lenghts becomes easy.

- CleanUpSpaces.py (alt-p):
The selected text is trimmed for the trailing whitespace. Then we convert leading tabs to 4 spaces. Lastly, multiples of 3 spaces are converted to the same multiple of 4 spaces.

- SearchTextDeleteLine.py (alt-l):
Search a text (literal or regex) and all lines in the file where the search string occurs, will be removed. The selected text is presented as the choice of search string. Very useful in data text files or log files.

- SearchTextKeepLine.py (alt-l):
Search a text (literal or regex) and all lines in the file where the search string occurs, will be kept. The selected text is presented as the choice of search string. Very useful in data text files or log files.

- SearchTextInFolderKeepOrDeleteFiles:
Search a string in text files of a folder. Delete the matching files (keep the others), or keep (and delete the others).

- OpenProcess (alt-g):
Open the TI process whose base file name is under the cursor.

- DeleteNP++Hits (alt-w):
After copying search results to a new file, we remove the number of hits and file extensions from the end of each line.

- ConvertTextNumbersToNumbers (alt-n):
The selection is a tabular format. Provide a field separator, column(s) to convert to numbers and locales.

- RectangularEdits.py (alt-r):
Insert text or a series of numbers (with a pattern) onto the rectangular selection

- TM1NoElementsWithCarets (Alt-z):
In view MDX, we remove in the member syntax with ^ characters anything in front of the real element name.

- TM1NoHierarchyNotation (Alt-f):
In rules and feeders, we remove the hierarchy notation for the element references in the main hierarchy.

- TreatEmeilText.py (alt-a):
Probably only useful to me :-) To format emails from Gmail. Also, also extra text to emails from Neil
