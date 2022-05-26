# Generated from c:\Users\bryan\Documents\Semestre Feb-Jun 2022\Compiladores\Proyecto Final\cool-compiler\antlr\cool.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .coolParser import coolParser
else:
    from coolParser import coolParser

# This class defines a complete generic visitor for a parse tree produced by coolParser.

class coolVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by coolParser#program.
    def visitProgram(self, ctx:coolParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#klass.
    def visitKlass(self, ctx:coolParser.KlassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#method.
    def visitMethod(self, ctx:coolParser.MethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#assignment.
    def visitAssignment(self, ctx:coolParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#formal.
    def visitFormal(self, ctx:coolParser.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#expr.
    def visitExpr(self, ctx:coolParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#assignment_new_type.
    def visitAssignment_new_type(self, ctx:coolParser.Assignment_new_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#case.
    def visitCase(self, ctx:coolParser.CaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#case_stat.
    def visitCase_stat(self, ctx:coolParser.Case_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#if_decl.
    def visitIf_decl(self, ctx:coolParser.If_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#let_decl.
    def visitLet_decl(self, ctx:coolParser.Let_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#function_call.
    def visitFunction_call(self, ctx:coolParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#while_loop.
    def visitWhile_loop(self, ctx:coolParser.While_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#primary.
    def visitPrimary(self, ctx:coolParser.PrimaryContext):
        return self.visitChildren(ctx)



del coolParser