class UCyanLexer(Lexer):
    """A lexer for the uCyan language."""

    def __init__(self, error_func):
        """Create a new Lexer.
        An error function. Will be called with an error
        message, line and column as arguments, in case of
        an error during lexing.
        """
        self.error_func = error_func

    # Reserved keywords
    keywords = {
        'print': "PRINT",
        'if': "IF",
        'else': "ELSE",
        'var': "VAR",
        'while': "WHILE",
		'true': "TRUE",
    'false': "FALSE",
		'let': "LET",
		'break': "BREAK",
		'continue': "CONTINUE"
    }

    # All the tokens recognized by the lexer
    tokens = tuple(keywords.values()) + (
        # Identifiers
        "ID",
        "VAR",
        # constants
        "FLOAT_CONST",
        "INT_CONST",
        "CHAR_CONST",
        "GE",
        "LE",
        "EQ",
		"EQUALS",
		"SEMI",
		"LT",
		"LBRACE",
		"TIMES",
		"PRINT",
		"PLUS",
		"RBRACE",
		"MINUS",
		"DIVIDE",
		"LPAREN",
		"RPAREN",
		"GT",
		"AND",
		"ERROR_UNTERM_COMMENT",
    "NE",
    "OR",
    "NOT"
    )

    # String containing ignored characters (between tokens)
    ignore = " \t"

    # Other ignored patterns
    ignore_newline = r"\n"
    ignore_comment = r"\/{2}.*|\/\*(.|\n)*?\*\/"

    # Regular expression rules for tokens
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    FLOAT_CONST = r"[0-9]+.[0-9]+"
    INT_CONST = r"[0-9]+"
    CHAR_CONST = r"'.*(\\n)?'" #PROBLEMAS: print 'BLABLA' não pode, tem que ser um só
    ERROR_UNTERM_COMMENT = r"\/\*.*"
    EQ = r'=='
    NE = r'\!\='
    NOT = r'\!'
    OR = r'\|\|'
    EQUALS = r"="
    SEMI = r";"
    # <= deve vir aqui!
    GE = r">="
    LE = r"<="
    LT = r"<"
    LBRACE = r"{"
    TIMES = r"\*"
    PLUS = r"\+"
    RBRACE = r"}"
    MINUS = r"-"
    DIVIDE = r"\/"
    LPAREN = r"\("
    RPAREN = r"\)"
    GT = r">"
    AND = r"&&"

    # Special cases
    def ID(self, t):
      t.type = self.keywords.get(t.value, "ID")
      return t

    # Define a rule so we can track line numbers
    def ignore_newline(self, t):
      self.lineno += len(t.value)

    def ignore_comment(self, t):
      self.lineno += t.value.count("\n")

    def find_column(self, token):
        """Find the column of the token in its line."""
        last_cr = self.text.rfind('\n', 0, token.index)
        return token.index - last_cr

    # Internal auxiliary methods
    def _error(self, msg, token):
        location = self._make_location(token)
        self.error_func(msg, location[0], location[1])
        self.index += 1

    def _make_location(self, token):
        return token.lineno, self.find_column(token)

    # Error handling rule
    def ERROR_UNTERM_COMMENT(self, t):
	    msg = "Unterminated comment"
	    self._error(msg, t)

    def error(self, t):
        msg = "Illegal character %s" % repr(t.value[0])
        self._error(msg, t)

    def error_char(self, t):
        msg = "lineno: Unterminated character const"
        self._error(msg, t)

    # Scanner (used only for test)
    def scan(self, text):
        output = ""
        for tok in self.tokenize(text):
            print(tok)
            output += str(tok) + "\n"
        return output
