import ply.yacc as yacc
from lexer import HQLLexer

class HQLParser:
    def __init__(self):
        self.lexer = HQLLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        self.lexer.build()
        return self.parser.parse(data, lexer=self.lexer.lexer)

    # Grammar rules
    def p_command(self, p):
        '''command : find_command
                   | show_command
                   | alert_command'''
        p[0] = p[1]

    def p_find_command(self, p):
        '''find_command : FIND ID where_clause'''
        p[0] = {'command_type': 'find', 'target': p[2], 'condition': p[3]}

    def p_show_command(self, p):
        '''show_command : SHOW aggregate_function ID FOR ID WITH condition
                        | SHOW aggregate_function ID FOR ID WITH ID EQ value'''
        if len(p) == 8:
            # SHOW aggregate_function ID FOR ID WITH condition
            p[0] = {'command_type': 'show', 'function': p[2], 'attribute': p[3], 
                   'target': p[5], 'condition': p[7]}
        else:
            # SHOW aggregate_function ID FOR ID WITH ID EQ value
            p[0] = {'command_type': 'show', 'function': p[2], 'attribute': p[3], 
                   'target': p[5], 'condition': {'field': p[7], 'operator': p[8], 'value': p[9]}}

    def p_alert_command(self, p):
        '''alert_command : ALERT IF condition'''
        p[0] = {'command_type': 'alert', 'condition': p[3]}

    def p_where_clause(self, p):
        '''where_clause : WHERE condition'''
        p[0] = p[2]

    def p_condition(self, p):
        '''condition : expression
                     | expression AND condition
                     | expression OR condition'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = {'operator': p[2].lower(), 'left': p[1], 'right': p[3]}

    def p_expression(self, p):
        '''expression : ID comparison_op value'''
        p[0] = {'field': p[1], 'operator': p[2], 'value': p[3]}

    def p_comparison_op(self, p):
        '''comparison_op : GT
                         | LT
                         | EQ
                         | GEQ
                         | LEQ
                         | NEQ'''
        p[0] = p[1]

    def p_value(self, p):
        '''value : NUMBER
                 | STRING
                 | ID'''
        p[0] = p[1]

    def p_aggregate_function(self, p):
        '''aggregate_function : AVERAGE
                              | COUNT
                              | MAX
                              | MIN'''
        p[0] = p[1].lower()

    # Error rule for syntax errors
    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")