import ply.lex as lex

class HQLLexer:
    # List of token names
    tokens = (
        'FIND', 'SHOW', 'ALERT', 'WHERE', 'FOR', 'WITH', 'IF', 'AND', 'OR',
        'GT', 'LT', 'EQ', 'GEQ', 'LEQ', 'NEQ',
        'NUMBER', 'STRING', 'ID', 'AVERAGE', 'COUNT', 'MAX', 'MIN'
    )

    # Regular expression rules for simple tokens
    t_GT = r'>'
    t_LT = r'<'
    t_EQ = r'='
    t_GEQ = r'>='
    t_LEQ = r'<='
    t_NEQ = r'!='

    # Reserved words
    reserved = {
        'find': 'FIND',
        'show': 'SHOW',
        'alert': 'ALERT',
        'where': 'WHERE',
        'for': 'FOR',
        'with': 'WITH',
        'if': 'IF',
        'and': 'AND',
        'or': 'OR',
        'average': 'AVERAGE',
        'count': 'COUNT',
        'max': 'MAX',
        'min': 'MIN',
    }

    # Regular expression rules with actions
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        # Check for reserved words
        t.type = self.reserved.get(t.value.lower(), 'ID')
        return t

    def t_STRING(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]  # Strip the quotes
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    def tokenize(self, data):
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens