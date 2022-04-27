from posixpath import split
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

ariSymbols = {'+', '-', '*', '/', '%'}
opeSymbols = {'=', '<', '>', '<=', '>=', '!='}
defaultClasses = {'Object', 'Int', 'String', 'Bool', 'SELF_TYPE', 'Main'}


def checkType(x):
    if x.isdigit():
        return "Int"
    elif x == "true" or x == "false":
        return "Bool"
    elif x[0] == '"' and x[-1] == '"':
        return "String"
    else:
        return "Object"


class semanticListener(coolListener):

    prohibitedClasses = ['SELF_TYPE', 'Int', 'Object']

    prohibitedInheritence = ['String', 'Bool', 'SELF_TYPE']

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.classDict = {}

    def __init__(self):
        self.main = False
        self.actualClass = ""
        self.actualFeature = ""

    def enterKlass(self, ctx: coolParser.KlassContext):

        self.actualClass = ctx.TYPE(0).getText()
        # Check if classname is valid
        if self.actualClass == 'SELF_TYPE':
            raise selftyperedeclared("'SELF_TYPE' is a reserved word")
        elif self.actualClass == 'Object':
            raise redefinedobject("'Object' is a reserved word")
        elif self.actualClass == 'Int':
            raise badredefineint("'Int' is a reserved word")
        else:
            if self.actualClass in self.classDict:
                raise redefinedclass(
                    "Class '" + self.actualClass + "' is already defined")
            else:
                self.classDict[self.actualClass] = {
                    "expressions": {}, "inherits": ""}
                if self.actualClass == 'Main':
                    self.main = True

        # Check if inherits is valid
        if ctx.TYPE(1):
            classInheritance = ctx.TYPE(1).getText()
            if classInheritance == 'Bool':
                raise inheritsbool("'Bool' is a reserved word")
            elif classInheritance == 'String':
                raise inheritsstring("'String' is a reserved word")
            elif classInheritance == 'SELF_TYPE':
                raise inheritsselftype("'SELF_TYPE' is a reserved word")
            elif classInheritance not in self.classDict:
                raise missingclass(
                    "Class '" + classInheritance + "' is not defined")
            else:
                self.classDict[self.actualClass
                               ]['inherits'] = classInheritance

    def exitKlass(self, ctx: coolParser.KlassContext):
        if (not self.main):
            raise nomain()

    def enterFeature(self, ctx: coolParser.FeatureContext):

        self.actualFeature = ctx.ID().getText()

        if self.actualFeature == 'self':
            raise anattributenamedself("'Self' is a reserved word")
        else:
            self.classDict[self.actualClass]['expressions'][self.actualFeature] = {
                "params": {}}
            if ctx.TYPE():
                if ctx.TYPE().getText() in self.classDict or ctx.TYPE().getText() in defaultClasses:
                    self.classDict[self.actualClass]['expressions'][self.actualFeature]['type'] = ctx.TYPE(
                    ).getText()
                else:
                    raise returntypenoexist(
                        "Class '" + ctx.TYPE().getText() + "' is not defined")

        if ctx.params:
            for param in ctx.params:
                if param.ID().getText() == 'self' or param.ID().getText() == 'SELF_TYPE':
                    raise selfinformalparameter("'Self' is a reserved word")

        if ctx._formal:

            for formal in ctx._formal.children:
                if formal.getText() == 'self' or formal.getText() == 'SELF_TYPE':
                    raise selftypeparameterposition(
                        "'Self' is a reserved word"
                    )
                else:
                    # Raise error creating two params with the same ID.
                    pass
        if ctx.expr():
            if ctx.expr().getChildCount() > 0:
                if ctx.TYPE():
                    if ctx.TYPE().getText() == 'SELF_TYPE':
                        if ctx.expr().getChild(0).getText() != 'self':
                            raise selftypebadreturn(
                                "'SELF_TYPE' is a reserved word")
                    self.classDict[self.actualClass]['expressions'][self.actualFeature]['type'] = ctx.TYPE(
                    ).getText()

                if ctx.expr().let_decl():
                    let_params = ctx.expr().let_decl(0)
                    if let_params.ID().getText() == 'self' or let_params.TYPE().getText() == 'self':
                        raise letself("'Let self' is a reserved word")
                    else:
                        self.classDict[self.actualClass]['expressions'][self.actualFeature]['params'][let_params.ID(
                        ).getText()] = {'TYPE': let_params.TYPE().getText(), 'VALUE': let_params.expr()}
                    let_in = ctx.expr().getChild(ctx.expr().getChildCount() - 1)
                    if let_in and let_in.getText().split('.')[1]:
                        let_method = let_in.getText().split('.')[1]
                        methodType = self.classDict[self.actualClass]['expressions'][self.actualFeature]['params'][let_params.ID(
                        ).getText()]['TYPE']
                        if let_method not in self.classDict[methodType]['expressions']:
                            raise(baddispatch("Tan mal chavitos :0"))

                if ctx.expr().getChildCount() > 1:
                    for child in ctx.expr().getChildren():
                        if child.getText() == 'self' or child.getText().split(':')[0] == 'self':
                            raise selfassignment(
                                "'Self assignment' is a reserved word")

                        if child.getText() in opeSymbols or child.getText() in ariSymbols:
                            previousChild = ctx.expr().getChild(
                                ctx.expr().children.index(child) - 1).getText()
                            nextChild = ctx.expr().getChild(ctx.expr().children.index(child) + 1).getText()
                            if child.getText() == '=':
                                if previousChild in self.classDict[self.actualClass]['expressions'][self.actualFeature]['params']:
                                    previousType = self.classDict[self.actualClass]['expressions'][
                                        self.actualFeature]['params'][previousChild]['TYPE']
                                else:
                                    previousType = checkType(previousChild)
                                if nextChild in self.classDict[self.actualClass]['expressions'][self.actualFeature]['params']:
                                    nextType = self.classDict[self.actualClass]['expressions'][
                                        self.actualFeature]['params'][nextChild]['TYPE']
                                else:
                                    nextType = checkType(nextChild)

                                if previousType != nextType:
                                    if nextType == 'String':
                                        raise badequalitytest(
                                            "Type mismatch in equality test")
                                    if nextType == 'Bool':
                                        raise badequalitytest2(
                                            "Type mismatch in equality test")

                            if child.getText() in ariSymbols:
                                if(not previousChild.isdigit() or not nextChild.isdigit()):
                                    raise badarith(
                                        "Arithmetic operation between non-numbers")

    def enterFormal(self, ctx: coolParser.FormalContext):
        if ctx.ID().getText() not in self.classDict[self.actualClass]['expressions'][self.actualFeature]['params']:
            self.classDict[self.actualClass]['expressions'][self.actualFeature]['params'][ctx.ID().getText()] = {
                "type": ctx.TYPE().getText()
            }
