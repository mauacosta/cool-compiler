from this import s
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import *
from util.structure import _allClasses as classDict


arithmeticSymbols = ['+', '-', '*', '/']
relationalSymbols = ['=', '>', '>=']



    

class semanticListener(coolListener):

    def __init__(self):
        self.currentKlass = None
        self.currentMethod = None
        self.currentMethodName = None

    def getLastPrimary(primary):
        hola = primary.expr()
        if primary.expr():
            if primary.expr().primary():
                return semanticListener.getLastPrimary(primary.expr().primary())

        return primary

    def enterKlass(self, ctx: coolParser.KlassContext):
        className = ctx.TYPE(0).getText()
        self.currentKlass = classDict[className]

      
    def enterMethod(self, ctx: coolParser.MethodContext):
        methodID = ctx.ID().getText()
        methodType = ctx.TYPE().getText()
        this_params = []
        if ctx.params:
            for param in ctx.params:
                this_params.append([param.ID().getText(), param.TYPE().getText()])
            self.currentMethod = Method(methodType, params=this_params)
        else:
            self.currentMethod = Method(methodType)
        self.currentMethodName = methodID


    def enterAssignment(self, ctx: coolParser.AssignmentContext):
        featureID = ctx.ID().getText()
        if featureID == 'self' or featureID == 'SELF_TYPE':
            raise anattributenamedself("Feature ID not valid (self)")

        if ctx.expr():
            if ctx.expr().primary():
                primary = semanticListener.getLastPrimary(ctx.expr().primary())
                if getType(primary, self.currentKlass, self.currentMethod) == None:
                    raise attrbadinit( primary.getText() +  ' was not found in this scope')

        self.currentKlass.addAttribute(featureID, ctx.TYPE().getText())

    def enterExpr(self, ctx: coolParser.ExprContext):
        if ctx.ID():
            exprName = ctx.ID().getText()
            # Check if the expression is self
            if exprName == 'self':
                raise selfassignment('Assignment to self is prohibited')


        # Check if exist function in the variable
        if ctx.function_call():
            #try:
                #hola = self.currentKlass.lookupMethod(ctx.function_call().ID().getText())
            #except KeyError:
                #raise badwhilebody('The function does not exists')
            if self.currentMethodName == ctx.function_call().ID().getText():
                raise badmethodcallsitself("a method can´t call iteself")


        if ctx.primary():
            primary = ctx.primary()
            if not primary.expr():
                if getType(ctx.primary(), self.currentKlass, self.currentMethod) == None:
                    raise outofscope(ctx.primary().getText() + ' was not found in this scope')

        if ctx.getChild(1):
            # Check for operations with Integers
            if ctx.getChild(1).getText() in arithmeticSymbols:
                first_item = getType(ctx.expr(0).primary(), self.currentKlass, self.currentMethod)
                second_item = getType(ctx.expr(1).primary(), self.currentKlass, self.currentMethod)
                if first_item != 'Int' or second_item != 'Int':
                    raise badarith("Trying to do an arithmetic operation with incorrect types")
            # Check for relation in the same type
            if ctx.getChild(1).getText() in relationalSymbols:
                first_item = getType(ctx.expr(0).primary(), self.currentKlass, self.currentMethod)
                second_item = getType(ctx.expr(1).primary(), self.currentKlass, self.currentMethod)
                if first_item != second_item:
                    raise badequalitytest("Is not possible to compare" + first_item + "and" + second_item)
                
        
    def enterFormal(self, ctx: coolParser.FormalContext):
        if ctx.ID().getText() == 'self':
            raise selfinformalparameter(
                'Using self as a parameter is prohibited')
        if ctx.TYPE().getText() == 'SELF_TYPE':
            raise selftypeparameterposition(
                'SELF_TYPE cannot be used as a parameter type')

    def enterWhile_loop(self, ctx: coolParser.While_loopContext):
        typeExp0 = getType(semanticListener.getLastPrimary(ctx.expr(0).primary()), self.currentKlass, self.currentMethod)
        if typeExp0 != 'Bool':
            raise badwhilecond("While ")

        
        

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        self.currentKlass.openScope()
        let_ID = ctx.ID().getText()

        if let_ID == 'self' or let_ID == 'SELF_TYPE':
            raise letself("Let incorrect (using self)")

        self.currentKlass.addScopeVariable(let_ID, ctx.TYPE().getText())

    def enterFunction_call(self, ctx: coolParser.Function_callContext):
        method_name = ctx.ID().getText()
        caller_exp = ctx.parentCtx.getChild(0).primary()
        if method_name == self.currentMethod:
            raise badmethodcallsitself("A method can not call itself")
        if ctx.parentCtx.getChild(1).getText() == '@':
            caller_exp = semanticListener.getLastPrimary(caller_exp)
            other_exp = ctx.parentCtx.TYPE()

            if(lookupClass(getType(caller_exp, self.currentKlass, self.currentMethod)).conforms(other_exp.getText())):
                raise trickyatdispatch2(caller_exp.getText() + " is not of type " + other_exp.getText())
        
        try:
            self.currentKlass.lookupMethod(method_name)
        except KeyError:
            raise baddispatch('The function does not exists')


    def enterCase(self, ctx: coolParser.CaseContext):
        typesCS = {''}
        for e in ctx.case_stat():
            if e.TYPE().getText() in typesCS:
                raise caseidenticalbranch("You have two cases of the same type")
            else:
                typesCS.add(e.TYPE().getText())
        print(typesCS)

    def exitKlass(self, ctx: coolParser.KlassContext):
        self.currentKlass = None

    def exitExpr(self, ctx: coolParser.ExprContext):
        if ctx.let_decl(0):
            self.currentKlass.closeScope()
            
    
