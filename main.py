from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.semantic import semanticListener
from listeners.tree import TreePrinter
from listeners.type import typeListener
from listeners.saveData import saveDataListener
from listeners.codegen import codeGenerator
from listeners.dataCreator import dataCreatorListener

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    #walker.walk(TreePrinter(), tree)
    #comentar para arbol y descomentar para pruebas
    walker.walk(typeListener(), tree)
    walker.walk(semanticListener(), tree)
    walker.walk(dataCreatorListener(), tree)
    walker.walk(saveDataListener(), tree)
    codeGenerator()

    
    #comentar para pruebas y descomentar para arbol
    



def dummy():
    raise SystemExit(1)


if __name__ == '__main__':
    compile('resources/codegen/input/fibo.cool')