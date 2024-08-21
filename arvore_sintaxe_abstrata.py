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
        line, column = self.lexer._make_location(p)
        return Coord(line, column)

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
        return Program(p.statements)








    # <statements> ::= { <statement> }*
    @_('statement { statement }',
       ' ')
    def statements(self, p):
        if hasattr(p, 'statement1'):
          return [p.statement0] + p.statement1
        elif hasattr(p, 'statement0'):
          return [p.statement0]
        else:
          return []








    # <statement> ::= <print_statement>
    #               | <assignment_statement>
    #               | <variable_definition>
    #               | <const_definition>
    #               | <if_statement>
    #               | <while_statement>
    #               | <break_statement>
    #               | <continue_statement>
    @_('print_statement',
       'assign_statement',
       'variable_definition',
       'const_definition',
       'if_statement',
       'while_statement',
       'break_statement',
       'continue_statement')
    def statement(self, p):
        return p[0]








    @_('expr SEMI')
    def statement(self, p):
      return ExpressionAsStatement(p.expr)








    # <print_statement> ::= PRINT <expr> ";"
    @_('PRINT expr SEMI')
    def print_statement(self, p):
        return PrintStatement(p.expr, coord=self._token_coord(p))






    # <assignment_statement> ::= <location> "=" <expr> ";"
    @_('location EQUALS expr SEMI')
    def assign_statement(self, p):
        return AssignmentStatement(p.location, p.expr, coord=self._token_coord(p))








    # {símbolos}?  ==> Zero ou uma ocorrência de símbolos (opcional)
    # <variable_definition> ::= "var" { <type> }? <identifier> "=" <expr> ";"
    #                         | "var" <type> <identifier> { "=" <expr> }? ";"
    @_('VAR type ID EQUALS expr SEMI')
    def variable_definition(self, p):
      # VarDefinition(ID, type, expr, coord=(lineno, column))
      return VarDefinition(p.ID, p.type, p.expr, coord=self._token_coord(p))








    @_('VAR ID EQUALS expr SEMI')
    def variable_definition(self, p):
      # VarDefinition(ID, type, expr, coord=(lineno, column))
      return VarDefinition(p.ID, None, p.expr, coord=self._token_coord(p))








    @_('VAR type ID SEMI')
    def variable_definition(self, p):
      # VarDefinition(ID, type, expr, coord=(lineno, column))
      return VarDefinition(p.ID, p.type, None, coord=self._token_coord(p))








    # <const_definition> ::= "let" { <type> }? <identifier> "=" <expr> ";"
    @_('LET type ID EQUALS expr SEMI')
    def const_definition(self, p):
      # ConstDefinition(ID, type, expr, coord=(lineno, column))
      return ConstDefinition(p.ID, p.type, p.expr, coord=self._token_coord(p))
     







    @_('LET ID EQUALS expr SEMI ')
    def const_definition(self, p):
      # ConstDefinition(ID, type, expr, coord=(lineno, column))
      return ConstDefinition(p.ID, None, p.expr, coord=self._token_coord(p))








    # <if_statement> ::= "if" <expr> "{" <statements> "}" { "else" "{" <statements> "}" }?
    @_('IF expr LBRACE statements RBRACE ELSE LBRACE statements RBRACE')
    def if_statement(self, p):
      # IfStatement(expr, statements0, statements1, coord=(lineno, column))
      return IfStatement(p.expr, p.statements0, p.statements1, coord=self._token_coord(p))








    @_('IF expr LBRACE statements RBRACE')
    def if_statement(self, p):
      # IfStatement(expr, statements0, statements1, coord=(lineno, column))
      return IfStatement(p.expr, p.statements, None, coord=self._token_coord(p))








    # <while_statement> ::= "while" <expr> "{" <statements> "}"
    @_('WHILE expr LBRACE statements RBRACE')
    def while_statement(self, p):
      return WhileStatement(p.expr, p.statements, coord=self._token_coord(p))








    # <break_statement> ::= "break" ";"
    @_('BREAK SEMI')
    def break_statement(self, p):
      return BreakStatement(coord=self._token_coord(p))








    # <continue_statement> ::= "continue" ";"
    @_('CONTINUE SEMI')
    def continue_statement(self, p):
      return ContinueStatement(coord=self._token_coord(p))








    # <type>     ::= <identifier>
    @_('ID')
    def type(self, p):
      # Type(ID, coord=(lineno, column))
      return Type(p.ID, coord=self._token_coord(p))








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
        return BinaryOp(p[1], p.expr0, p.expr1, coord=self._token_coord(p))








    # <expr> ::= "+" <expr>
    #         | "-" <expr>
    #         | "!" <expr>
    @_('PLUS expr',
       'MINUS expr',
       'NOT expr')
    def expr(self, p):
        # UnaryOp('+', expr, coord=(lineno, column))
        return UnaryOp(p[0], p.expr, coord=self._token_coord(p))








    # <expr> ::= "(" <expr> ")"
    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr








    # <expr> ::= <literal>
    @_('literal')
    def expr(self, p):
        return p.literal








    # <expr> ::= <location>
    @_('location')
    def expr(self, p):
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
      if hasattr(p, 'INT_CONST'): return Literal('int', p.INT_CONST, coord=self._token_coord(p)) # Literal('int', INT_CONST, coord=(lineno, column))
      elif hasattr(p, 'FLOAT_CONST'): return Literal('float', p.FLOAT_CONST, coord=self._token_coord(p))
      elif hasattr(p, 'CHAR_CONST'): return Literal('char', p.CHAR_CONST, coord=self._token_coord(p))








    '''
    literal = tuple('literal: bool, true @ lineno:column')
           | tuple('literal: bool, false @ lineno:column')
    '''
    # <literal> ::= "true"
    #             | "false"
    @_('TRUE',
       'FALSE')
    def literal(self, p):
        return Literal('bool', p[0], coord=self._token_coord(p))








    # <location> ::= <identifier>
    @_('ID')
    def location(self, p):
      return Location(p.ID, coord=self._token_coord(p))
