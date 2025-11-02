from Npp import editor, notepad
import re


# Wim Gielis
# Nov. 2025
#
# SumNumbers script (Alt-$):
#       - The selected text contains numbers (or text and numbers)
#       - We display the sum of all numbers extracted from the selection
#       - The selection can be multiple non-contiguous areas or even a rectangular (columnar) selection
#       - We want to show numbers as in Dutch notation
#       - When the selected numbers contain separators for decimals and/or thousands then the user needs to confirm these for correct parsing


WANTED_DECIMAL_SEP = ','
WANTED_THOUSAND_SEP = '.'


# --- Utilities ----------------------------------------------------------------
def ask_user(prompt: str, default: str) -> str:
    """Ask user for input"""
    user_input = notepad.prompt(f"{prompt}", "Separator", default)
    return user_input.strip() if user_input.strip() else default

def show_message(title: str, text: str) -> None:
    """Show message box with title and text"""
    notepad.messageBox(text, "Result")

def parse_core_number(core_text: str, decimal: str, thousand: str):
    """Given core_text (digits and possibly separators), parse to float using decimal/thousand characters."""
    t = core_text
    if thousand:
        # remove all thousand separators (they may appear multiple times)
        t = t.replace(thousand, '')
    # replace decimal sep with dot for Python float
    if decimal and decimal != '.':
        t = t.replace(decimal, '.')
    # Edge-case: if result still contains both '.' and ',' (user may have inverted choices) try a fallback:
    t = t.strip()
    # final sanity: remove stray spaces
    t = re.sub(r'\s+', '', t)
    return float(t)

def remap_us_format(s, user_thousand, user_decimal):
    # If user wants no thousand separator (empty), remove ',' from us formatted
    if user_thousand == '':
        s = s.replace(',', '')
        # Now replace decimal point:
        if user_decimal != '.':
            s = s.replace('.', user_decimal)
        return s
    # else do a safe replace with placeholder
    placeholder = '<<<TH>>>'
    s = s.replace(',', placeholder)  # US thousands -> placeholder
    s = s.replace('.', user_decimal)  # US decimal -> user decimal
    s = s.replace(placeholder, user_thousand)  # placeholder -> user thousand
    return s

# --- Patterns & vars ----------------------------------------------------------

# Regex to find possible numbers:
# optional leading minus, at least one digit, optional digits/dots/commas, optional trailing minus.
num_pattern = re.compile(r'-?\d[\d\.,]*-?')

# currency tokens to detect around matches
currency_tokens = ['EUR', 'USD', '€', '$']

console.clear()

# Collect all texts from selections (normal + rectangular)
sel_count = editor.getSelections()
all_texts = []

# Detect rectangular selection: editor.getRectangularSelection() returns list for rect
# We'll attempt to handle both normal and rectangular selections as in prior scripts.
rect_handled = False
for i in range(sel_count):
    start = editor.getSelectionNStart(i)
    end = editor.getSelectionNEnd(i)
    # If there's a rectangular selection active, handle it once
    try:
        rect_lines = editor.getRectangularSelection()
    except Exception:
        rect_lines = None

    # If we have rectangular lines and they're non-empty, use them (handle once)
    if rect_lines and not rect_handled:
        # rect_lines is a list of strings representing the selected columns on each line
        for line in rect_lines:
            if line is not None:
                all_texts.append(line)
        rect_handled = True
        # if rectangular selection is active, normal selection parts may not be needed
        # continue to next selection (rect handled)
        continue

    # else normal selection
    txt = editor.getTextRange(start, end)
    if txt:
        all_texts.append(txt)

# If nothing selected, inform user and exit
if not all_texts:
    show_message("Sum Selected Numbers", "No selection found. Please select text (normal or column/rectangular) and run again.")
else:

    # --- Extract numbers, detect separators and currencies -----------------------

    found_numbers = []  # list of dicts: {raw:..., cleaned:..., sign:..., currencies:set()}
    detected_currency_tokens = set()
    need_ask_separators = False

    for text in all_texts:
        # Search for number-like substrings in the text
        for m in num_pattern.finditer(text):
            token = m.group(0)
            if not token:
                continue

            # Check for currency tokens immediately around the match (a few characters)
            span_start, span_end = m.start(), m.end()
            nearby = ''
            # get up to 4 chars before and after match if available
            try:
                before = text[max(0, span_start-4):span_start]
                after  = text[span_end:span_end+4]
                nearby = before + after
            except Exception:
                nearby = ''

            token_currencies = set()
            # detect tokens like EUR or USD (letters) or € or $
            for cur in currency_tokens:
                pattern_cur = re.escape(cur)
                if re.search(pattern_cur, nearby, flags=re.IGNORECASE):
                    token_currencies.add(cur)
                    detected_currency_tokens.add(cur)

            # Determine sign: leading minus or trailing minus => negative
            negative = False
            if token.startswith('-') and token.endswith('-'):
                # both sides: treat as negative (rare)
                negative = True
                token_core = token.strip('-')
            elif token.startswith('-'):
                negative = True
                token_core = token[1:]
            elif token.endswith('-'):
                negative = True
                token_core = token[:-1]
            else:
                token_core = token

            # Skip tokens that don't have any digits after stripping (safety)
            if not re.search(r'\d', token_core):
                continue

            # If the token_core contains '.' or ',', then we'll possibly need to ask separators
            if ('.' in token_core) or (',' in token_core):
                need_ask_separators = True

            # store raw and cleaned core
            found_numbers.append({
                'raw': token,
                'core': token_core,
                'negative': negative,
                'currencies': token_currencies
            })

    # If no numbers found, inform user
    if not found_numbers:
        show_message("Sum Selected Numbers", "No numeric tokens found in selection.")
    else:

        # --- Ask separators (only once and only if needed ------------------------------------

        data_decimal_sep = "."
        data_thousand_sep = ","
        if need_ask_separators:
            # Ask user once for decimal and thousand separators (defaults shown)
            data_decimal_sep = ask_user("Enter the observed decimal separator", WANTED_DECIMAL_SEP)
            data_thousand_sep = ask_user("Enter the observed thousand separator", WANTED_THOUSAND_SEP)

        # If user chose same char for both separators, warn and revert thousand to empty
        if data_decimal_sep == data_thousand_sep:
            # It's ambiguous to have both equal; treat thousand as empty (no thousands)
            data_thousand_sep = ''
            try:
                # console.show()
                console.write("Decimal and thousand separator were identical; thousand separator ignored.\n")
            except Exception:
                pass

        total = 0.0
        parse_errors = []

        for item in found_numbers:
            core = item['core']
            sign = -1.0 if item['negative'] else 1.0
            try:
                value = parse_core_number(core, data_decimal_sep, data_thousand_sep)
                total += sign * value
            except Exception as ex:
                parse_errors.append((item['raw'], str(ex)))

        # --- Format output using user's separators -----------------------------------

        # Format total with 2 decimals using US-style grouping (',' thousands, '.' decimal),
        # then remap to user-chosen separators.
        us_formatted = "{:,.2f}".format(total)  # e.g. "1,234.56"
        # Remap separators: us_formatted has ',' as thousand, '.' as decimal.
        # We want thousand_sep and decimal_sep as provided by user.
        final_formatted = remap_us_format(us_formatted, WANTED_THOUSAND_SEP, WANTED_DECIMAL_SEP)

        # Prepare currency display:
        currency_display = ''
        if detected_currency_tokens:
            # If exactly one currency and it's simple ($ or € or EUR or USD), try to place it in natural position:
            if len(detected_currency_tokens) == 1:
                only = next(iter(detected_currency_tokens)).upper()
                if only in ('$', 'USD'):
                    currency_display = '$' + final_formatted
                    final_message = "Sum: {}".format(currency_display)
                elif only in ('€', 'EUR'):
                    # common EU display uses trailing symbol; keep it trailing with a space
                    currency_display = final_formatted + ' ' + '€'
                    final_message = "Sum: {}".format(currency_display)
                else:
                    # unknown single token -> suffix
                    final_message = "Sum: {} {}".format(final_formatted, only)
            else:
                # multiple different currencies found -> show formatted sum and list currencies
                cur_list = ', '.join(sorted(detected_currency_tokens))
                final_message = "Sum: {}  (currencies detected: {})".format(final_formatted, cur_list)
        else:
            final_message = "Sum: {}".format(final_formatted)

        # If parse errors occurred, add short note
        if parse_errors:
            final_message += "\n\nNote: some tokens couldn't be parsed and were skipped. Examples:\n"
            for raw, err in parse_errors[:5]:
                final_message += " - '{}': {}\n".format(raw, err)
            if len(parse_errors) > 5:
                final_message += " - ...and {} more.\n".format(len(parse_errors) - 5)
        final_message = final_message.rstrip('0' + WANTED_DECIMAL_SEP)

        # Show final result in message box
        show_message("Sum of Selected Numbers", final_message)