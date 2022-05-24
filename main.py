from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.semantic import semanticListener
from listeners.type import typeListener


def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    walker.walk(typeListener(), tree)
    walker.walk(semanticListener(), tree)



def dummy():
    raise SystemExit(1)


if __name__ == '__main__':
    compile('resources/semantic/input/nomain.cool')
