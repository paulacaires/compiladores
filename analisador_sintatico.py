class UCyanParser(Parser):
    """A parser for the uCyan language."""

    # Get the token list from the lexer (required)
    tokens = UCyanLexer.tokens

    precedence = (
        # <<< YOUR CODE HERE >>>
    )

    def __init__(self, error_func=lambda msg, x, y: print("Lexical error: %s at %d:%d" % (msg, x, y), file=sys.stdout)):
        """Create a new Parser.
        An error function for the lexer.
        """
        self.lexer = UCyanLexer(error_func)

    def parse(self, text, lineno=1, index=0):
        return super().parse(self.lexer.tokenize(text, lineno, index))

    # Internal auxiliary methods
    def _token_coord(self, p):
        return self.lexer._make_location(p)

    # Error handling rule
    def error(self, p):
        if p:
            if hasattr(p, 'lineno'):
                print("Error at line %d near the symbol %s " % (p.lineno, p.value))
            else:
                print("Error near the symbol %s" % p.value)
        else:
            print("Error at the end of input")

    # <program> ::= <statements> EOF
    @_('statements')
    def program(self, p):
			return ('program', p.statements)

    # <statements> ::= { <statement> }*
    @_('statement { statement }')
    def statements(self, p):
		  return [p.statement[0]] + p.statement1

    # <statement> ::= <print_statement>
    #               | <assignment_statement>
    #               | <variable_definition>
    #               | <const_definition>
    #               | <if_statement>
    #               | <while_statement>
    #               | <break_statement>
    #               | <continue_statement>
    #               | <expr> ";"
    @_('print_statement',
       'assign_statement',
       'if_statement',
       'variable_definition',
       'const_definition',
       'while_statement',
       'break_statement',
       'continue_statement',
       'expr SEMI'
       )
    def statement(self, p):
        return p[0]  
    
    # <print_statement> ::= "print" <expr> ";"
    @_('PRINT expr SEMI')
    def print_statement(self, p):
		return ('print @ %d:%d' % self._token_coord(p), p.expr)
    
    # <assignment_statement> ::= <location> "=" <expr> ";"
    @_('location EQUALS expr SEMI')
    def assign_statement(self, p):
		return ('assign @ %d:%d' % self._token_coord(p), p.identifier, p.expr)

    # <variable_definition> ::= "var" { <type> }? <identifier> "=" <expr> ";"
    #                         | "var" <type> <identifier> { "=" <expr> }? ";"
    @_('VAR type identifier EQUALS expr SEMI',
	   'VAR identifier EQUALS expr SEMI',
	   'VAR type identifier SEMI')
	def variable_definition (self, p):
		return ('variable: @ %d:%d' % p.ID, self._token_coord(p))
		# tuple('variable: ' + str(ID) + ' @ lineno:column', type, expr)
				
    # <const_definition> ::= "let" { <type> }? <identifier> "=" <expr> ";"
    @_('LET type identifier EQUALS expr SEMI',
       'LET identifier EQUALS expr SEMI')
    def const_definition (self, p):
		pass
		
    # <if_statement> ::= "if" <expr> "{" <statements> "}" { "else" "{" <statements> "}" }?
    @_('IF expr LBRACE statements RBRACE { ELSE LBRACE statements RBRACE }')
    def if_statement(self, p):
		pass

    # <while_statement> ::= "while" <expr> "{" <statements> "}"
    @_('WHILE expr LBRACE statements RBRACE')
    def while_statement(self, p):
		pass

    # <break_statement> ::= "break" ";"
    @_('BREAK SEMI')
    def break_statement(self, p):
		pass

    # <continue_statement> ::= "continue" ";"
    @_('CONTINUE SEMI')
    def continue_statement(self, p):
		pass

    # <expr> ::= <expr> "+" <expr>
    #         | <expr> "-" <expr>
    #         | <expr> "*" <expr>
    #         | <expr> "/" <expr>
    #         | <expr> "<" <expr>
    #         | <expr> "<=" <expr>
    #         | <expr> ">" <expr>
    #         | <expr> ">=" <expr>
    #         | <expr> "==" <expr>
    #         | <expr> "!=" <expr>
    #         | <expr> "&&" <expr>
    #         | <expr> "||" <expr>
    #         | "+" <expr>
    #         | "-" <expr>
    #         | "!" <expr>
    #         | "(" <expr> ")"
    #         | <literal>
    #         | <location>
    @_('expr PLUS expr',
	   'expr MINUS expr',
	   'expr TIMES expr',
	   'expr DIVIDE expr',
	   'expr LT expr',
	   'expr LTE expr',
	   'expr GT expr',
	   'expr GE expr',
	   'expr EQ expr',
	   'expr NE expr', 
	   'expr AND expr',
	   'expr OR expr',
	   'PLUS expr',
	   'MINUS expr',
	   'LPAREN expr RPAREN',
	   'literal',
	   'location')
	def expr(self, p):
		pass

    # <literal> ::= <integer_constant>
    #             | <float_constant>
    #             | <character_constant>
    #             | "true"
    #             | "false"
    @_('integer_constant',
       'float_constant',
       'character_constant',
       'TRUE',
       'FALSE')
    def literal(self, p):
		if hasattr(p, 'integer_constant'):
			return ('literal: int, %d @ %d:%d' + str(p.integer_constant) + self._token_coord(p))
		elif hasattr(p, 'float_constant'):
			return ('literal: float, %f @ %d:%d' + str(p.float_constant) + self._token_coord(p))
		elif hasattr(p, 'character_constant'):
			return ('literal: char, %c @ %d:%d' + str(p.character_constant) + self._token_coord(p))s
		elif hasattr(p, 'TRUE'):
			return ('literal: bool, true @ %d:%d' + self._token_coord(p))
		elif hasattr(p, 'TRUE'):
			return ('literal: bool, false @ %d:%d' + self._token_coord(p))
	
    # <location> ::= <identifier>
    @_('identifier')
    def location(self, p):
		return ('location: ' + str(p.identifier) + ' @ %d:%d', % self._token_coord(p))

    # <type>     ::= <identifier>
    @_('identifier')
    def type(self, p):
		return ('type: ' + str(p.identifier) + ' @ %d:%d', % self._token_coord(p))
