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
            #print ("{}{}:{}".format(s, type(ctx).__name__[:-7], poner el tipo en su estructura))



            if type(ctx).__name__[:-7] == "Klass":
                ##Class NombreClase: Tipo 
                self.currentKlass = ctx.TYPE(0).getText()
                
                if(ctx.TYPE(1)):
                    print ("{}{} {}: inherits {}".format(s, type(ctx).__name__[:-7],  self.currentKlass, ctx.TYPE(1).getText()))
                else:
                    print("{}{} {}".format(s, type(ctx).__name__[:-7],  self.currentKlass))
            elif type(ctx).__name__[:-7] == "Method":
                self.currentMethod = ctx.ID().getText()
                print ("{}{} {}:{}".format(s, type(ctx).__name__[:-7],self.currentMethod, ctx.TYPE().getText()))
            elif type(ctx).__name__[:-7] == "Assignment" or type(ctx).__name__[:-7] == "Assignment_new_type" or type(ctx).__name__[:-7] == "Let_decl" or type(ctx).__name__[:-7] == "Case_stat":
                print ("{}{} {}: {}".format(s, type(ctx).__name__[:-7], ctx.ID().getText(), ctx.TYPE().getText()))
            elif type(ctx).__name__[:-7] == "Formal":
                print ("{}Param:{}".format(s, ctx.TYPE().getText()))
            elif type(ctx).__name__[:-7] == "Function_call":
                print ("{} Call method {}".format(s, ctx.ID().getText()))
            elif type(ctx).__name__[:-7] == "Primary":
                if(ctx.ID()):
                    print("{}Primary:{} ".format(s, ctx.getText()))
                elif(ctx.INTEGER()):
                    print("{}Primary:Int value {}".format(s, ctx.getText()))
                elif(ctx.STRING()):
                    print("{}Primary:String value {}".format(s, ctx.getText()))
                elif(ctx.TRUE() ):
                    print("{}Primary:Bool value True".format(s))
                elif(ctx.FALSE()):
                    print("{}Primary:Bool value False".format(s))
            elif type(ctx).__name__[:-7] == "While_loop" or type(ctx).__name__[:-7] == "If_decl":
                print("{} enters {}".format(s,type(ctx).__name__[:-7]))
            elif(ctx.expr(0).primary()):
                print ("{}{}:{}".format(s, type(ctx).__name__[:-7], getType(ctx.expr(0).primary(), self.currentKlass, self.currentMethod)))
            else:
                print ("{}{}:{}".format(s, type(ctx).__name__[:-7], ctx.TYPE().getText()))

        except:
            if type(ctx).__name__[:-7] == "Method":
                if( not ctx.ID().getText() == self.currentMethod):
                    print ("{}{} = {}".format(s, type(ctx).__name__[:-7],ctx.ID().getText()))
            else:
                #print(type(ctx).__name__[:-7])
                print ("{}{}".format(s, type(ctx).__name__[:-7]))

            


    def exitEveryRule(self, ctx):
        self.depth = self.depth - 1