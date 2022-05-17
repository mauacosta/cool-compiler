from antlr.coolListener import coolListener
from antlr.coolListener import TerminalNode
from util.structure import *

class TreePrinter(coolListener):
    currentKlass = ""
    currentMethod = ""
    def __init__(self, types={}):
        self.depth = 0
        self.types = types

    def enterEveryRule(self, ctx):
        self.depth = self.depth + 1
        s = ''

        for i in range(self.depth-1):
            s += " "        
        try:
            # Modificar aquí el nombre del atributo que contiene el tipo de dato, para imprimirlo en donde exista en cada
            # nodo del árbol, si es una clase, debe de tener una manera de convertirse a string
            # def __str__(self):
            #     return "foo"
            # si no encuentra el atributo simplement va a escribir el nombre del nodo
            if type(ctx).__name__[:-7] == "Klass":
                self.currentKlass = ctx.TYPE(0).getText()
                print ("{}{}: inherits {}".format(s, type(ctx).__name__[:-7], ctx.TYPE(1).getText()))
            if type(ctx).__name__[:-7] == "Method":
                self.currentMethod = ctx.ID().getText()
                print ("{}{}:{}".format(s, type(ctx).__name__[:-7], ctx.TYPE().getText()))

            if(ctx.expr(0).primary()):
                print ("{}{}:{}".format(s, type(ctx).__name__[:-7], getType(ctx.expr(0).primary(), self.currentKlass, self.currentMethod)))
            else:
                print ("{}{}:{}".format(s, type(ctx).__name__[:-7], ctx.TYPE().getText()))
        except:
            print ("{}{}".format(s, type(ctx).__name__[:-7]))
            


    def exitEveryRule(self, ctx):
        self.depth = self.depth - 1