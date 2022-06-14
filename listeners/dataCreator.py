from this import s
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import *
from util.structure import _allClasses as classDict
from util.structure import _allStrings, _allInts, _allBool


arithmeticSymbols = ['+', '-', '*', '/']
relationalSymbols = ['=', '>', '>=']
  

class dataCreatorListener(coolListener):

    def __init__(self):
        self.currentKlass = None
        self.currentMethod = None
        self.currentMethodName = None
    
    def enterProgram(self, ctx: coolParser.ProgramContext):
        _allStrings.append('--filename--')
        _allStrings.append('\\n')

    def getLastPrimary(primary):
        if primary.expr():
            if primary.expr().primary():
                return semanticListener.getLastPrimary(primary.expr().primary())
        return primary
    

    def enterKlass(self, ctx: coolParser.KlassContext):
        className = ctx.TYPE(0).getText()
        self.currentKlass = classDict[className]
        if ctx.TYPE(1):
            if ctx.TYPE(1).getText() != 'Object':
                self.currentKlass.inherits = ctx.TYPE(1).getText()
            
        
        

      
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
        if ctx.expr():
            if ctx.expr().primary():
                primary = semanticListener.getLastPrimary(ctx.expr().primary())
        ##Could bring error
        try:
            x = self.currentKlass.lookupAttribute(featureID)
        except KeyError:
            pass
        
        self.currentKlass.addAttribute(featureID, ctx.TYPE().getText())

    def enterExpr(self, ctx: coolParser.ExprContext):

        if ctx.ID():
            exprName = ctx.ID().getText()
            # Check if the expression is self
            
        # Check if exist function in the variable
        if ctx.function_call():
            methodID = ctx.function_call().ID().getText()
            try:
                if ctx.expr(0).primary().expr().TYPE():
                    callerType = ctx.expr(0).primary().expr().TYPE().getText()
                    methodParams = lookupClass(callerType).lookupMethod(methodID).params
                    methodParams = list(methodParams.values())
                    for p in ctx.function_call().params:
                        i = 0
                        pType = getParamType(p.getText(), self.currentKlass, self.currentMethod)
                        i += 1
            except:
                pass
 
                 
            try:
                if ctx.expr(0): 
                    attributeCaller = ctx.expr(0).getText() 
                    attributeType = self.currentKlass.lookupAttribute(attributeCaller)            
            except KeyError:
                pass
            

            

            try:
                if attributeCaller == 'self':
                    attributeCaller = self.currentKlass.name #B
                callerType = ctx.TYPE().getText() #C
            except:
                pass
            

            try:
                klassName = self.currentMethod.params[attributeCaller]
                klass = lookupClass(klassName)
                klass.lookupMethod(ctx.function_call().ID().getText())
            except:
                pass    
            
        if ctx.primary():
            primary = ctx.primary()



    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        # Si me parece, pero no entiendo como vamos a tomar el tipo de la derecha
        # Cree en el G4 algo que se llama assign_new_type si quieres checalo, ahí esta el id <- new_type 
        # el problema de eso es que mataba a outofscope y assignnoconform porque me aparece un error de que pues su expr no tiene assignment_new_type
        self.currentKlass.openScope()
        let_ID = ctx.ID().getText()


        self.currentKlass.addScopeVariable(let_ID, ctx.TYPE().getText())


    def enterCase(self, ctx: coolParser.CaseContext):
        typesCS = {''}
        for e in ctx.case_stat():
            typesCS.add(e.TYPE().getText())


    def exitKlass(self, ctx: coolParser.KlassContext):
        self.currentKlass = None

    def exitExpr(self, ctx: coolParser.ExprContext):
        if ctx.let_decl(0):
            self.currentKlass.closeScope()

    def exitProgram(self, ctx: coolParser.ProgramContext):
        print("class Dict")
        for a in classDict:
            print(a)
        print("end exit")

