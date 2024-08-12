class UCyanParser(Parser):
    """A parser for the uCyan language."""

    # Get the token list from the lexer (required)
    tokens = UCyanLexer.tokens

    precedence = (
        ('right', 'EQUALS'),
        ('left', 'OR', 'AND', 'EQ', 'NE'),
        ('left', 'LT', 'GT', 'LE', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'NOT'),
        ('right', 'ELSE'),
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
        print('program')
        return ('program', p.statements)

    # <statements> ::= { <statement> }*
    @_('statement { statement }')
    def statements(self, p):
        print(p.statement0)
        print('Dentro do p.statement1:')
        for x in p.statement1:
          print(x)
        return [p.statement0] + p.statement1

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
       'variable_definition',
       'const_definition',
       'if_statement',
       'while_statement',
       'break_statement',
       'continue_statement')
    def statement(self, p):
        print('statement ')
        return p[0]

    @_('expr SEMI')
    def statement(self, p):
      return ('expr', p.expr,)

    # <print_statement> ::= PRINT <expr> ";"
    @_('PRINT expr SEMI')
    def print_statement(self, p):
        print('print_statement ')
        return ('print @ %d:%d' % self._token_coord(p), p.expr)

    # <assignment_statement> ::= <location> "=" <expr> ";"
    @_('location EQUALS expr SEMI')
    def assign_statement(self, p):
        print('assign_statement ')
        return ('assignment @ %d:%d' % self._token_coord(p), p.location, p.expr)

    # {símbolos}?  ==> Zero ou uma ocorrência de símbolos (opcional)
    # <variable_definition> ::= "var" { <type> }? <identifier> "=" <expr> ";"
    #                         | "var" <type> <identifier> { "=" <expr> }? ";"
    @_('VAR type ID EQUALS expr SEMI')
    def variable_definition(self, p):
      print('variable_definition1 ' + p.ID)
      return ('variable: ' + p.ID + ' @ %d:%d' % self._token_coord(p), p.type, p.expr)

    @_('VAR ID EQUALS expr SEMI')
    def variable_definition(self, p):
      print('variable_definition2 ' + p.ID)
      return ('variable: ' + p.ID + ' @ %d:%d' % self._token_coord(p), p.type, p.expr)

    @_('VAR type ID SEMI')
    def variable_definition(self, p):
      print('variable_definition3 ' + p.ID)
      return ('variable: ' + p.ID + ' @ %d:%d' % self._token_coord(p), p.type, p.expr)

    # <const_definition> ::= "let" { <type> }? <identifier> "=" <expr> ";"
    @_('LET type ID EQUALS expr SEMI')
    def const_definition(self, p):
      print('const_definition1' + p.ID)
      return ('const: ' + p.ID + ' @ %d:%d' % self._token_coord(p), p.type, p.expr)

    @_('LET ID EQUALS expr SEMI ')
    def const_definition(self, p):
      print('const_definition2' + p.ID)
      return ('const: ' + p.ID + ' @ %d:%d' % self._token_coord(p), p.type, p.expr)

    # <if_statement> ::= "if" <expr> "{" <statements> "}" { "else" "{" <statements> "}" }?
    @_('IF expr LBRACE statements RBRACE { ELSE LBRACE statements RBRACE }')
    def if_statement(self, p):
      print('if_statement')
      return ('if @ %d:%d' % self._token_coord(p), p.expr, p.statements0, p.statements1)

    # <while_statement> ::= "while" <expr> "{" <statements> "}"
    @_('WHILE expr LBRACE statements RBRACE')
    def while_statement(self, p):
      print('while')
      return ('while @ %d:%d' % self._token_coord(p), p.expr, p.statements)

    # <break_statement> ::= "break" ";"
    @_('BREAK SEMI')
    def break_statement(self, p):
      print('break_statement')
      return ('break @ %d:%d' % self._token_coord(p),)

    # <continue_statement> ::= "continue" ";"
    @_('CONTINUE SEMI')
    def continue_statement(self, p):
      print('continue_statement')
      return ('continue @ %d:%d' % self._token_coord(p),)

    # <type>     ::= <identifier>
    @_('ID')
    def type(self, p):
      print('type')
      return ('type: ' + str(p.ID) + ' @ %d:%d' % self._token_coord(p))

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
    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
	     'expr DIVIDE expr',
       'expr LT expr',
       'expr LE expr',
       'expr GT expr',
       'expr GE expr',
       'expr EQ expr',
       'expr NE expr',
       'expr AND expr',
       'expr OR expr')
    def expr(self, p):
        print('binary expr ') 
        return ('binary_op: ' + p[1] + ' @ %d:%d' %self._token_coord(p), p.expr0, p.expr1)    
        # tuple('binary_op: + @ lineno:column', expr0, expr1)   
        
    # <expr> ::= "+" <expr>
    #         | "-" <expr>
    #         | "!" <expr>
    @_('PLUS expr',
       'MINUS expr',
       'NE expr')
    def expr(self, p):
        print ('unary expr ')
        return ('unary_op: ' + p[0] + ' @ %d:%d' %self._token_coord(p), p.expr)

    # <expr> ::= "(" <expr> ")"
    @_('LPAREN expr RPAREN')
    def expr(self, p):
        print('( expr )')
        return p.expr

    # <expr> ::= <literal>
    @_('literal')
    def expr(self, p):
        print('expr literal ')
        return p.literal

    # <expr> ::= <location>
    @_('location')
    def expr(self, p):
      print('expr location ')
      return p.location

    '''
    literal = tuple('literal: int, ' + str(INT_CONST) + ' @ lineno:column')
        | tuple('literal: float, ' + str(FLOAT_CONST) + ' @ lineno:column')
        | tuple('literal: char, ' + str(CHAR_CONST) + ' @ lineno:column')
    '''
    # <literal> ::= <integer_constant>
    #             | <float_constant>
    #             | <character_constant>
    @_('INT_CONST',
       'FLOAT_CONST',
       'CHAR_CONST')
    def literal(self, p):
      if hasattr(p, 'INT_CONST'): return ('literal: int, %s @ %d:%d' % ((p[0],) + self._token_coord(p)))
      elif hasattr(p, 'FLOAT_CONST'): return ('literal: float, %s @ %d:%d' % ((p[0],) + self._token_coord(p)))
      elif hasattr(p, 'CHAR_CONST'): return ('literal: char, %s @ %d:%d' % ((p[0],) + self._token_coord(p)))
      # tuple('literal: int, ' + str(INT_CONST) + ' @ lineno:column')

    '''
    literal = tuple('literal: bool, true @ lineno:column')
           | tuple('literal: bool, false @ lineno:column')
    '''
    # <literal> ::= "true"
    #             | "false"
    @_('TRUE',
       'FALSE')
    def literal(self, p):
        print('literal bool ')
        return ('literal: bool, @ %d:%d' + self._token_coord(p),)

    # <location> ::= <identifier>
    @_('ID')
    def location(self, p):
      print('location @d:@d', p.ID)
      return ('location: ' + str(p.ID) + ' @ %d:%d' % self._token_coord(p))
