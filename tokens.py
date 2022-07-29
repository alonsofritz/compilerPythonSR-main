""" Classe token, representação dos símbolos, palavras-chave, identificadores, outros lexemas. """
class Token():
    """ 
    Instâcia objeto da classe:
        lexema = String que guarda lexema do token
        line = Inteiro que guarda a LINHA onde esse token esta no programa.
        column = Inteiro que guarda a COLUNA onde esse token esta no programa.
        type = Tipo do token, com base nos tipos da classe Types
    """
    def __init__(self, _type, _lexema, _line, _column):
        self.type = _type
        self.lexema = _lexema
        self.line = _line
        self.column = _column

    def __str__(self):
        return "[ " + self.type + ", " + self.lexema + ", " + self.line + " ]"

    def getType(self):
        return self.type

    def getLexema(self):
        return self.lexema

    def getLine(self):
        return self.line
    
    def getColumn(self):
        return self.column

    def setLine(self, _line):
        self.line = _line

    def setColumn(self, _column):
        self.column = _column

# https://docs.python.org/3/tutorial/classes.html
# https://stackoverflow.com/questions/551038/private-implementation-class-in-python