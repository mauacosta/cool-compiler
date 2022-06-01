from this import s
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import *
from util.structure import _allClasses as classDict


prohibitedClassnames = {'Int': badredefineint,
                        'Object': redefinedobject, 'SELF_TYPE': selftyperedeclared}

prohibitedInheritance = {'Bool': inheritsbool,
                         'String': inheritsstring, 'SELF_TYPE': inheritsselftype}


    

class typeListener(coolListener):

    def __init__(self):
        classDict.clear()
        setBaseKlasses()
        self.main = False
        self.currentKlass = None
        self.currentMethod = None

    def enterKlass(self, ctx: coolParser.KlassContext):
        className = ctx.TYPE(0).getText()
        if className in prohibitedClassnames:
            raise prohibitedClassnames[className]()
        if ctx.TYPE(1):
            classInherits = ctx.TYPE(1).getText()
            if classInherits in prohibitedInheritance:
                raise prohibitedInheritance[classInherits]()
            self.currentKlass = Klass(
                className, inherits=ctx.TYPE(1).getText())
        else:
            self.currentKlass = Klass(className)
        if className == 'Main':
            self.main = True
      
    def enterMethod(self, ctx: coolParser.MethodContext):
        methodID = ctx.ID().getText()
        methodType = ctx.TYPE().getText()
        if methodID == 'self' or methodID == 'SELF_TYPE':
            raise anattributenamedself("Method ID not valid (self)")
        if methodType == 'SELF_TYPE':
            if ctx.expr().children[0].getText() != 'self':
                raise selftypebadreturn("Invalid Self Type return")
        elif methodType not in classDict:
            raise returntypenoexist("Method" + methodType + "returns an invalid type")
        this_params = []
        if ctx.params:
            for param in ctx.params:
                for id in this_params:
                    hola = id[0]
                    if param.ID().getText() == id[0]:
                        hola = "duplicated"
                        raise dupformals("Duplicated formal")
                this_params.append([param.ID().getText(), param.TYPE().getText()])
            self.currentMethod = Method(methodType, params=this_params)
        else:
            self.currentMethod = Method(methodType)
        try:
            methodExist = self.currentKlass.lookupMethod(methodID)
            if methodExist:
                if len(methodExist.params) != len(ctx.params):
                    hola = len(methodExist.params)
                    hola2 = len(ctx.params)
                    raise signaturechange("Changing number of parameters")
                
                # For every param in params check if it has the same type as in the original declaration.
                for param in ctx.params:
                    if methodExist.params[param.ID().getText()] != param.TYPE().getText():
                        raise overridingmethod4("Overriding an existing method")
            else:
                pass
        except KeyError:
            pass
        self.currentKlass.addMethod(methodID, self.currentMethod)

    def exitKlass(self, ctx: coolParser.KlassContext):
        if (not self.main):
            raise nomain()
        self.currentKlass = None

            
    
