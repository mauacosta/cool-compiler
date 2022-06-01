# Generated from c:\Users\gina1\Documents\Tec\Compiladores\cool-compiler\antlr\cool.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .coolParser import coolParser
else:
    from coolParser import coolParser

# This class defines a complete listener for a parse tree produced by coolParser.
class coolListener(ParseTreeListener):

    # Enter a parse tree produced by coolParser#program.
    def enterProgram(self, ctx:coolParser.ProgramContext):
        pass

    # Exit a parse tree produced by coolParser#program.
    def exitProgram(self, ctx:coolParser.ProgramContext):
        pass


    # Enter a parse tree produced by coolParser#klass.
    def enterKlass(self, ctx:coolParser.KlassContext):
        pass

    # Exit a parse tree produced by coolParser#klass.
    def exitKlass(self, ctx:coolParser.KlassContext):
        pass


    # Enter a parse tree produced by coolParser#method.
    def enterMethod(self, ctx:coolParser.MethodContext):
        pass

    # Exit a parse tree produced by coolParser#method.
    def exitMethod(self, ctx:coolParser.MethodContext):
        pass


    # Enter a parse tree produced by coolParser#assignment.
    def enterAssignment(self, ctx:coolParser.AssignmentContext):
        pass

    # Exit a parse tree produced by coolParser#assignment.
    def exitAssignment(self, ctx:coolParser.AssignmentContext):
        pass


    # Enter a parse tree produced by coolParser#formal.
    def enterFormal(self, ctx:coolParser.FormalContext):
        pass

    # Exit a parse tree produced by coolParser#formal.
    def exitFormal(self, ctx:coolParser.FormalContext):
        pass


    # Enter a parse tree produced by coolParser#expr.
    def enterExpr(self, ctx:coolParser.ExprContext):
        pass

    # Exit a parse tree produced by coolParser#expr.
    def exitExpr(self, ctx:coolParser.ExprContext):
        pass


    # Enter a parse tree produced by coolParser#assignment_new_type.
    def enterAssignment_new_type(self, ctx:coolParser.Assignment_new_typeContext):
        pass

    # Exit a parse tree produced by coolParser#assignment_new_type.
    def exitAssignment_new_type(self, ctx:coolParser.Assignment_new_typeContext):
        pass


    # Enter a parse tree produced by coolParser#case.
    def enterCase(self, ctx:coolParser.CaseContext):
        pass

    # Exit a parse tree produced by coolParser#case.
    def exitCase(self, ctx:coolParser.CaseContext):
        pass


    # Enter a parse tree produced by coolParser#case_stat.
    def enterCase_stat(self, ctx:coolParser.Case_statContext):
        pass

    # Exit a parse tree produced by coolParser#case_stat.
    def exitCase_stat(self, ctx:coolParser.Case_statContext):
        pass


    # Enter a parse tree produced by coolParser#if_decl.
    def enterIf_decl(self, ctx:coolParser.If_declContext):
        pass

    # Exit a parse tree produced by coolParser#if_decl.
    def exitIf_decl(self, ctx:coolParser.If_declContext):
        pass


    # Enter a parse tree produced by coolParser#let_decl.
    def enterLet_decl(self, ctx:coolParser.Let_declContext):
        pass

    # Exit a parse tree produced by coolParser#let_decl.
    def exitLet_decl(self, ctx:coolParser.Let_declContext):
        pass


    # Enter a parse tree produced by coolParser#function_call.
    def enterFunction_call(self, ctx:coolParser.Function_callContext):
        pass

    # Exit a parse tree produced by coolParser#function_call.
    def exitFunction_call(self, ctx:coolParser.Function_callContext):
        pass


    # Enter a parse tree produced by coolParser#while_loop.
    def enterWhile_loop(self, ctx:coolParser.While_loopContext):
        pass

    # Exit a parse tree produced by coolParser#while_loop.
    def exitWhile_loop(self, ctx:coolParser.While_loopContext):
        pass


    # Enter a parse tree produced by coolParser#primary.
    def enterPrimary(self, ctx:coolParser.PrimaryContext):
        pass

    # Exit a parse tree produced by coolParser#primary.
    def exitPrimary(self, ctx:coolParser.PrimaryContext):
        pass



del coolParser