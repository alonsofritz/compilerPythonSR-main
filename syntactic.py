import sys
import os.path
import string
import lex as l
import stack as s
import pandas as pd      # Para manipular os dados da Tabela Excel .xlsx

""" Classe que representa o analisador léxico """
""" Bottom-up => LR(1) """
""" LR(1)     => Redução pelo lado esquerdo """


class Syntactic():

    def __init__(self):

        # Start léxico
        self.lex = l.Lex()
        self.lex.start()
        # self.lex.printTokenList()

        # Tabela sintática
        self.tableExcel = pd.read_excel(
            './utils/SyntaticTable.xlsx', skiprows=1, index_col=0)
        self.tableSyntax = self.tableExcel.to_numpy()

        # Arquivo de saída do sintático
        self.output_file = "sync_output.txt"
        self.output_file = open(self.output_file, 'w')

        # Pilha para análise sintática
        self.stack = s.Stack()
        self.stack.push(0)

        # Quantidade de elementos gerados por uma produção
        self.sizeProduction = [1, 1, 1, 2, 2, 2, 3, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1,
                               1, 1, 1, 1, 1, 1, 1, 1, 7, 8, 4, 17, 7, 5, 5, 1, 1,
                               1, 1, 3, 4, 4, 1, 2, 2, 3, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1,
                               3, 2, 3, 1, 1, 1, 1, 3, 4, 4, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # Gramática
        self.grammar = [
            'START -> STMTS',
            'STMTS -> DECLARATION_VAR',
            'STMTS -> DECLARATION_COM',
            'STMTS -> DECLARATION_VAR STMTS',
            'STMTS -> DECLARATION_COM STMTS',
            'DECLARATION_VAR -> DECLARATION ;',
            'DECLARATION_VAR -> DECLARATION INIT ;',
            'DECLARATION_VAR -> id ;',
            'DECLARATION_VAR -> DECLARATION INIT',
            'DECLARATION_VAR -> ASSIGN_STR',
            'DECLARATION -> TYPE id',
            'INIT -> = TOKEN',
            'TYPE -> Number',
            'TYPE -> String',
            'TYPE -> Boolean',
            'TOKEN -> id',
            'TOKEN -> number',
            'TOKEN -> string',
            'TOKEN -> boolean',
            'DECLARATION_COM -> DECLARATION_IF',
            'DECLARATION_COM -> DECLARATION_FOR',
            'DECLARATION_COM -> DECLARATION_WHILE',
            'DECLARATION_COM -> DECLARATION_READ',
            'DECLARATION_COM -> DECLARATION_WRITE',
            'DECLARATION_COM -> DECLARATION_EXP_ARIT',
            'DECLARATION_IF -> if ( EXP_REL ) { STMTS }',
            'DECLARATION_IF -> if ( EXP_REL ) { STMTS } DECLARATION_ELSE',
            'DECLARATION_ELSE -> else { STMTS }',
            'DECLARATION_FOR -> for ( id = number , id OP_REL number , id = SIMPLE_EXP ) { STMTS }',
            'DECLARATION_WHILE -> while ( EXP_REL ) { STMTS }',
            'DECLARATION_READ -> read ( id ) ;',
            'DECLARATION_WRITE -> write ( EXP_WRITE ) ;',
            'EXP_WRITE -> id',
            'EXP_WRITE -> number',
            'EXP_WRITE -> string',
            'EXP_WRITE -> boolean',
            'EXP_WRITE -> ( SIMPLE_EXP )',
            'DECLARATION_EXP_ARIT -> id = SIMPLE_EXP ;',
            'ASSIGN_STR -> id = string ; ',
            'SIMPLE_EXP -> TERM',
            'SIMPLE_EXP -> OP_SIGNAL TERM',
            'SIMPLE_EXP -> TERM TERM_DERIVATION',
            'SIMPLE_EXP -> OP_SIGNAL TERM TERM_DERIVATION',
            'TERM -> COEFF',
            'TERM -> COEFF COEFF_DERIVATION',
            'TERM_DERIVATION -> + OP_SUM_DERIVATION',
            'TERM_DERIVATION -> - OP_SUB_DERIVATION',
            'OP_SUM_DERIVATION -> TERM',
            'OP_SUM_DERIVATION -> TERM TERM_DERIVATION',
            'OP_SUB_DERIVATION -> TERM',
            'OP_SUB_DERIVATION -> TERM TERM_DERIVATION',
            'COEFF -> id ',
            'COEFF -> number',
            'COEFF -> ( SIMPLE_EXP )',
            'COEFF_DERIVATION -> OP_MULDIV COEFF',
            'COEFF_DERIVATION -> OP_MULDIV COEFF COEFF_DERIVATION',
            'OP_MULDIV -> *',
            'OP_MULDIV -> /',
            'OP_SIGNAL -> +',
            'OP_SIGNAL -> -',
            'EXP_REL -> SIMPLE_EXP OP_REL SIMPLE_EXP',
            'EXP_REL -> SIMPLE_EXP OP_REL SIMPLE_EXP EXP_REL_DERIVATION',
            'EXP_REL_DERIVATION -> OP_COND SIMPLE_EXP OP_REL SIMPLE_EXP',
            'EXP_REL_DERIVATION -> OP_COND SIMPLE_EXP OP_REL SIMPLE_EXP EXP_REL_DERIVATION',
            'OP_REL -> <',
            'OP_REL -> >',
            'OP_REL -> <=',
            'OP_REL -> >=',
            'OP_REL -> ==',
            'OP_REL -> <>',
            'OP_COND -> and',
            'OP_COND -> or',
            'OP_COND -> not'
        ]

        # Produções existentes
        self.productions = [
            'START',
            'STMTS',
            'STMTS',
            'STMTS',
            'STMTS',
            'DECLARATION_VAR',
            'DECLARATION_VAR',
            'DECLARATION_VAR',
            'DECLARATION_VAR',
            'DECLARATION_VAR',
            'DECLARATION',
            'INIT',
            'TYPE',
            'TYPE',
            'TYPE',
            'TOKEN',
            'TOKEN',
            'TOKEN',
            'TOKEN',
            'DECLARATION_COM',
            'DECLARATION_COM',
            'DECLARATION_COM',
            'DECLARATION_COM',
            'DECLARATION_COM',
            'DECLARATION_COM',
            'DECLARATION_IF',
            'DECLARATION_IF',
            'DECLARATION_ELSE',
            'DECLARATION_FOR',
            'DECLARATION_WHILE',
            'DECLARATION_READ',
            'DECLARATION_WRITE',
            'EXP_WRITE',
            'EXP_WRITE',
            'EXP_WRITE',
            'EXP_WRITE',
            'EXP_WRITE',
            'DECLARATION_EXP_ARIT',
            'ASSIGN_STR',
            'SIMPLE_EXP',
            'SIMPLE_EXP',
            'SIMPLE_EXP',
            'SIMPLE_EXP',
            'TERM',
            'TERM',
            'TERM_DERIVATION',
            'TERM_DERIVATION',
            'OP_SUM_DERIVATION',
            'OP_SUM_DERIVATION',
            'OP_SUB_DERIVATION',
            'OP_SUB_DERIVATION',
            'COEFF',
            'COEFF',
            'COEFF',
            'COEFF_DERIVATION',
            'COEFF_DERIVATION',
            'OP_MULDIV',
            'OP_MULDIV',
            'OP_SIGNAL',
            'OP_SIGNAL',
            'EXP_REL',
            'EXP_REL',
            'EXP_REL_DERIVATION',
            'EXP_REL_DERIVATION',
            'OP_REL',
            'OP_REL',
            'OP_REL',
            'OP_REL',
            'OP_REL',
            'OP_REL',
            'OP_COND',
            'OP_COND',
            'OP_COND'
        ]

    def columns(self, x):
        if x == 0:
            return 'DEL_SC'
        elif x == 1:
            return 'id'
        elif x == 2:
            return 'OP_ASS'
        elif x == 3:
            return 'KW_Number'
        elif x == 4:
            return 'KW_String'
        elif x == 5:
            return 'KW_Boolean'
        elif x == 6:
            return 'number'
        elif x == 7:
            return 'string'
        elif x == 8:
            return 'boolean'
        elif x == 9:
            return 'KW_if'
        elif x == 10:
            return 'DEL_LP'
        elif x == 11:
            return 'DEL_RP'
        elif x == 12:
            return 'DEL_LCB'
        elif x == 13:
            return 'DEL_RCB'
        elif x == 14:
            return 'KW_else'
        elif x == 15:
            return 'KW_for'
        elif x == 16:
            return 'DEL_COM'
        elif x == 17:
            return 'KW_while'
        elif x == 18:
            return 'KW_read'
        elif x == 19:
            return 'KW_write'
        elif x == 20:
            return 'OP_ADD'
        elif x == 21:
            return 'OP_SUB'
        elif x == 22:
            return 'OP_MUL'
        elif x == 23:
            return 'OP_DIV'
        elif x == 24:
            return 'OP_LT'
        elif x == 25:
            return 'OP_GT'
        elif x == 26:
            return 'OP_LE'
        elif x == 27:
            return 'OP_GE'
        elif x == 28:
            return 'OP_EQ'
        elif x == 29:
            return 'OP_NEQ'
        elif x == 30:
            return 'OP_AND'
        elif x == 31:
            return 'OP_OR'
        elif x == 32:
            return 'OP_NOT'
        elif x == 33:
            return '$'

    def terminals(self, x):
        if x == 'DEL_SC':
            return 0
        elif x == 'id':
            return 1
        elif x == 'OP_ASS':
            return 2
        elif x == 'KW_Number':
            return 3
        elif x == 'KW_String':
            return 4
        elif x == 'KW_Boolean':
            return 5
        elif x == 'number':
            return 6
        elif x == 'string':
            return 7
        elif x == 'boolean':
            return 8
        elif x == 'KW_if':
            return 9
        elif x == 'DEL_LP':
            return 10
        elif x == 'DEL_RP':
            return 11
        elif x == 'DEL_LCB':
            return 12
        elif x == 'DEL_RCB':
            return 13
        elif x == 'KW_else':
            return 14
        elif x == 'KW_for':
            return 15
        elif x == 'DEL_COM':
            return 16
        elif x == 'KW_while':
            return 17
        elif x == 'KW_read':
            return 18
        elif x == 'KW_write':
            return 19
        elif x == 'OP_ADD':
            return 20
        elif x == 'OP_SUB':
            return 21
        elif x == 'OP_MUL':
            return 22
        elif x == 'OP_DIV':
            return 23
        elif x == 'OP_LT':
            return 24
        elif x == 'OP_GT':
            return 25
        elif x == 'OP_LE':
            return 26
        elif x == 'OP_GE':
            return 27
        elif x == 'OP_EQ':
            return 28
        elif x == 'OP_NEQ':
            return 29
        elif x == 'OP_AND':
            return 30
        elif x == 'OP_OR':
            return 31
        elif x == 'OP_NOT':
            return 32
        elif x == '$':
            return 33

    def notTerminals(self, X):
        if X == 'START':
            return 34
        elif X == 'STMTS':
            return 35
        elif X == 'DECLARATION_VAR':
            return 36
        elif X == 'DECLARATION':
            return 37
        elif X == 'INIT':
            return 38
        elif X == 'TYPE':
            return 39
        elif X == 'TOKEN':
            return 40
        elif X == 'DECLARATION_COM':
            return 41
        elif X == 'DECLARATION_IF':
            return 42
        elif X == 'DECLARATION_ELSE':
            return 43
        elif X == 'DECLARATION_FOR':
            return 44
        elif X == 'DECLARATION_WHILE':
            return 45
        elif X == 'DECLARATION_READ':
            return 46
        elif X == 'DECLARATION_WRITE':
            return 47
        elif X == 'EXP_WRITE':
            return 48
        elif X == 'DECLARATION_EXP_ARIT':
            return 49
        elif X == 'ASSIGN_STR':
            return 50
        elif X == 'SIMPLE_EXP':
            return 51
        elif X == 'TERM':
            return 52
        elif X == 'TERM_DERIVATION':
            return 53
        elif X == 'OP_SUM_DERIVATION':
            return 54
        elif X == 'OP_SUB_DERIVATION':
            return 55
        elif X == 'COEFF':
            return 56
        elif X == 'COEFF_DERIVATION':
            return 57
        elif X == 'OP_MULDIV':
            return 58
        elif X == 'OP_SIGNAL':
            return 59
        elif X == 'EXP_REL':
            return 60
        elif X == 'EXP_REL_DERIVATION':
            return 61
        elif X == 'OP_REL':
            return 62
        elif X == 'OP_COND':
            return 63

    # Semântico => S-Atribuído
    # O que vai ser avaliado de aspecto semântico? (Especificação)
    #
    #   Tabela de Símbolos (constrói conforme roda o sintático)
    #       Ex: x + y
    #           x já foi declarado? olha na tabela
    #           y já foi declarado? olha na tabela
    #           eles são do mesmo tipo? preciso converter? pode parar ou fazer um cast
    #               Especificar que operações só podem com tipos iguais !!!
    #               Pode-se fazer uma coerção tbm

    def start(self):
        # Verificar erros léxicos
        print("\n")

        buffer = 0

        while True:
            top = self.stack.items[len(self.stack.items)-1]

            # Olha o topo da lista de tokens
            action = self.tableSyntax[top][self.terminals(
                self.lex.tokens_list[buffer].getType())]

            if action[0] == 's':
                self.shift(int(action[1:]), buffer)
                buffer += 1
            elif action[0] == 'r':
                self.reduce(int(action[1:]), buffer)
            elif action[0] == 'e':
                errorList = []

                for i in range(34):
                    action = self.tableSyntax[top][self.terminals(
                        self.lex.tokens_list[i].getType())]
                    if action[0] == 's':
                        errorList.append(self.columns(i))

                print("Erro na Linha: ",
                      self.lex.tokens_list[buffer].getLine())
                print("Encontrado: ", self.lex.tokens_list[buffer].getType())
                print("Esperado: ", errorList)

                if (len(self.lex.tokens_list) - 1) > buffer:
                    buffer += 1
                else:
                    print("Não Compilado")
                    break
            elif action == 'acc':
                print("Compilado com Sucesso")
                break
            else:
                print("Something is wrong...")

    def shift(self, state, buffer):
        self.stack.push(self.lex.tokens_list[buffer].getLexema())
        self.stack.push(state)
        #print(self.stack.items)

    def reduce(self, state, buffer):
        
        for x in range(0, self.sizeProduction[state]):
            self.stack.pop()
            self.stack.pop()

        self.stack.push(self.productions[state])
        action = int(self.tableSyntax[self.stack.items[len(
            self.stack.items)-2]][self.notTerminals(self.stack.items[len(self.stack.items)-1])])
        self.stack.push(action)
        # print(self.stack.items, "\n")


sync = Syntactic()
sync.start()
