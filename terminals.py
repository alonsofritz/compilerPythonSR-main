""" Dicionários usados para facilitar a identificação de tokens da linguagem. """

# Delimitadores => t1
delimiters = dict({
    't100': 'DEL_LP',    # (
    't101': 'DEL_RP',    # )
    't102': 'DEL_LCB',   # {
    't103': 'DEL_RCB',   # }
    't104': 'DEL_SC',    # ;
    't105': 'DEL_COM',   # ,
})

# Palavras reservadas = t2
keywords = dict({
    't200': 'KW_Number',
    't201': 'KW_String',
    't202': 'KW_Boolean',
    't203': 'KW_read',
    't204': 'KW_write',
    't205': 'KW_if',
    't206': 'KW_else',
    't207': 'KW_for',
    't208': 'KW_while',
})

# Constantes = t3
constants = dict({
    't300': 'id',
    't301': 'number',
    't302': 'string',
    't303': 'boolean',
})

# Operadores = t4
operators = dict({
    't400': 'OP_ADD',       # +
    't401': 'OP_SUB',       # -
    't402': 'OP_MUL',       # *
    't403': 'OP_DIV',       # /
    't404': 'OP_EQ',        # ==
    't405': 'OP_NEQ',       # <>
    't406': 'OP_ASS',       # =
    't407': 'OP_GT',        # >
    't408': 'OP_GE',        # >=
    't409': 'OP_LT',        # <
    't410': 'OP_LE',        # <=
    't411': 'OP_AND',       # and
    't412': 'OP_OR',        # or
    't413': 'OP_NOT',       # not
})
