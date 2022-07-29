import sys
import os.path
import lex as l
import string

class Semantic ():

    # Construtor da Classe
    def __init__ (self):

        # Start léxico
        self.lex = l.Lex()
        self.lex.start()
        # self.lex.printTokenList()
        
        ## Criação de arquivo de saída
        self.outputSemantic = "sem_output.txt"
        self.outputSemantic = open(self.outputSemantic, 'w')
        
        ## Flags
        self.errorFlag = False
        self.warningFlag = False
        
        # Tabelas Semanticas
        self.declarationTable = []

    def getTypeOfVariableInDeclarationTable(self, lexema):
        for declaration in self.declarationTable:
            if declaration[1] == lexema:
                return declaration[0]
    
    def setVariableToUsed(self, lexema):
        for declaration in self.declarationTable:
            if declaration[1] == lexema:
                declaration[2] = True
    
    def varIsDeclared(self, lexema):
        for declaration in self.declarationTable:
            if declaration[1] == lexema:
                return True
        return False
    
    def checkUnusedVariables(self):
        for declaration in self.declarationTable:
            if not declaration[2]:
                print('\033[93m' + "!!WARNING!! {", declaration[1], "} foi declarada mas nao eh utilizada." + '\x1b[0m', "\n" )
                self.outputSemantic.write("!!WARNING!! {" + declaration[1] + "} foi declarada mas nao eh utilizada")
                self.warningFlag = True
    
    def checkAssignmentVariable(self, lexema):
        while(not "DEL_SC" in self.lex.tokens_list[self.buffer].getType()):
            if(self.lex.tokens_list[self.buffer].getType() == "number" or 
                self.lex.tokens_list[self.buffer].getType() == "string" or 
                self.lex.tokens_list[self.buffer].getType() == "boolean"):
                typeOfTargetVar = self.getTypeOfVariableInDeclarationTable(lexema)
                
                if(self.lex.tokens_list[self.buffer].getType() != typeOfTargetVar.lower()):
                    print('\x1b[1;31m' + "ERRO!! Atribuicao de tipos nao esta correta para a variavel (Nao existe conversao de tipo) - linha: ", self.lex.tokens_list[self.buffer].getLine() + '\x1b[0m' "\n")
                    self.outputSemantic.write("ERRO!! Atribuicao de tipos nao esta correta para a variavel (Nao existe conversao de tipo) - linha: " + self.lex.tokens_list[self.buffer].getLine() + "\n")
                    self.errorFlag = True
            self.buffer += 1
    
    def checkVariableCall(self):
        if(self.varIsDeclared(self.lex.tokens_list[self.buffer].getLexema())):
            self.setVariableToUsed(self.lex.tokens_list[self.buffer].getLexema())
            self.checkAssignmentVariable(self.lex.tokens_list[self.buffer].getLexema())

        else:
            print('\x1b[1;31m' + "ERRO!! {", self.lex.tokens_list[self.buffer].getLexema(), "} nao foi declarado - linha: ", self.lex.tokens_list[self.buffer].getLine() + '\x1b[0m' "\n")
            self.outputSemantic.write("ERRO!! {" + self.lex.tokens_list[self.buffer].getLexema() + "} nao foi declarado - linha: " + self.lex.tokens_list[self.buffer].getLine() + "\n")
            self.errorFlag = True

    def fillDeclarationTable(self):
        declaration = []
        
        while(not "DEL_SC" in self.lex.tokens_list[self.buffer].getType()):
            if("OP_ASS" in self.lex.tokens_list[self.buffer].getType()):
                declaration.append(True)
                self.declarationTable.append(declaration)
                self.checkAssignmentVariable(declaration[1])
                return
            else:
                if(not(self.varIsDeclared(self.lex.tokens_list[self.buffer].getLexema()))):
                    declaration.append(self.lex.tokens_list[self.buffer].getLexema())
                else:
                    print('\x1b[1;31m' + "ERRO!! {", self.lex.tokens_list[self.buffer].getLexema(), "} ja foi declarado - linha: ", self.lex.tokens_list[self.buffer].getLine() + '\x1b[0m' "\n")
                    self.outputSemantic.write("ERRO!! {" + self.lex.tokens_list[self.buffer].getLexema() + "} ja foi declarado - linha: " + self.lex.tokens_list[self.buffer].getLine() + "\n")
                    self.errorFlag = True
                    return
                self.buffer += 1
        
        declaration.append(False)
        self.declarationTable.append(declaration)
    
    def start(self):

        self.buffer = 0

        while(not "$" in self.lex.tokens_list[self.buffer].getType()):          
        
            # Verifica: Declaracao de variaveis
            if(self.lex.tokens_list[self.buffer].getType() == "KW_Number" or 
                self.lex.tokens_list[self.buffer].getType() == "KW_String" or 
                self.lex.tokens_list[self.buffer].getType() == "KW_Boolean" ):

                self.fillDeclarationTable()
            
            # Verifica: Utilizacao/Declaracao de Variavel
            elif(self.lex.tokens_list[self.buffer].getType() == "id"):
                
                self.checkVariableCall()
            
            self.buffer+=1

        self.checkUnusedVariables()

        if(not self.errorFlag):
            if(self.warningFlag):
                print('\033[93m' + 'Compilado com Sucesso' + '\x1b[0m')
            else:
                print('\x1b[1;32m' + 'Compilado com Sucesso' + '\x1b[0m')

sem = Semantic()
sem.start()