6 useful scripts for usage in Notepad++. Setup first is needed to have PythonScript in Notepad++
After that, it becomes really powerful.

Wim Gielis
Q1 2025


DeleteText.py: select text, press Alt-d and in the whole file it will be removed. Much faster than Replace with an empty string and making sure the checkbox with regex/normal/extended is right, etc.

MergeLines.py: select lines and choose a separator. I could not find the same functionality in Notepad++ but maybe I overlooked.

UnmergeText.py: the inverse operation or MergeLines. A customer separator can be derived and if not found, chosen.

SaveAllTabs.py: a loop through all open tabs. If unsaved, the code saves the tab if already saved earlier. If not yet saved, it is writting in a hardcoded folder on the hard drive.

DuplicateTab: duplicate the text in the current tab as a new tab, immediately to the right and enable the same language syntax (if any)

AddArrows.py: probably only useful to me :-) Serves a specific purpose of adding ==> text in the empty lines between paragraphes of text copied from an email.
