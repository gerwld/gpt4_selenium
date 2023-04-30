# This is an attempt to provide an alternative to ''.title() that works with
# acronyms.
# There are several tricky cases to worry about in typical order of importance:
# 0. Upper case first letter of each word that is not an 'minor' word.
# 1. Always upper case first word.
# 2. Do not down case acronyms
# 3. Quotes
# 4. Hyphenated words: drive-in
# 5. Titles within titles: 2001 A Space Odyssey
# 6. Maintain leading spacing
# 7. Maintain given spacing: This is a test.  This is only a test.

# The following code addresses 0-3 & 7.  It was felt that addressing the others
# would add considerable complexity.


def titlecase(
    s,
    exceptions=(
        'and', 'or', 'nor', 'but', 'a', 'an', 'and', 'the', 'as', 'at', 'by',
        'for', 'in', 'of', 'on', 'per', 'to'
    )
):
    words = s.strip().split(' ')
    # split on single space to maintain word spacing
    # remove leading and trailing spaces -- needed for first word casing

    def upper(s):
        if s:
            if s[0] in '‘“"‛‟' + "'":
                return s[0] + upper(s[1:])
            return s[0].upper() + s[1:]
        return ''

    # always capitalize the first word
    first = upper(words[0])

    return ' '.join([first] + [
        word if word.lower() in exceptions else upper(word)
        for word in words[1:]
    ])
