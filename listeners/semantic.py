from posixpath import split
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser


class semanticListener(coolListener):

    prohibitedClasses = ['SELF_TYPE', 'Int', 'Object']

    prohibitedInheritence = ['String', 'Bool', 'SELF_TYPE']

    def __init__(self):
        self.main = False

    def enterKlass(self, ctx: coolParser.KlassContext):

        # Check if inherits is valid
        if ctx.TYPE(1):
            classInheritance = ctx.TYPE(1).getText()
            if classInheritance == 'Bool':
                raise inheritsbool("'Bool' is a reserved word")
            if classInheritance == 'String':
                raise inheritsstring("'String' is a reserved word")
            if classInheritance == 'SELF_TYPE':
                raise inheritsselftype("'SELF_TYPE' is a reserved word")

        # Check if classname is valid
        if ctx.TYPE(0).getText() == 'SELF_TYPE':
            raise selftyperedeclared("'SELF_TYPE' is a reserved word")
        if ctx.TYPE(0).getText() == 'Object':
            raise redefinedobject("'Object' is a reserved word")
        if ctx.TYPE(0).getText() == 'Int':
            raise badredefineint("'Int' is a reserved word")
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True

    def exitKlass(self, ctx: coolParser.KlassContext):
        if (not self.main):
            raise nomain()

    def enterFeature(self, ctx: coolParser.FeatureContext):
        hola = ctx.ID().getText()
        if ctx.ID().getText() == 'self':
            raise anattributenamedself("'Self' is a reserved word")
        if ctx.params:
            for param in ctx.params:
                if param.ID().getText() == 'self' or param.ID().getText() == 'SELF_TYPE':
                    raise selfinformalparameter("'Self' is a reserved word")
        hola = ctx._formal
        if ctx._formal:
            for formal in ctx._formal.children:
                if formal.getText() == 'self' or formal.getText() == 'SELF_TYPE':
                    raise selftypeparameterposition(
                        "'Self' is a reserved word"
                    )
        if ctx.expr():
            if ctx.expr().getChildCount() > 0:
                if ctx.expr().getChild(0).getText() == 'let':
                    if ctx.expr().getChild(1).getText() == 'self' or ctx.expr().getChild(1).getText().split(':')[0] == 'self':
                        raise letself("'Let self' is a reserved word")
                if ctx.expr().getChildCount() > 1:
                    for child in ctx.expr().getChildren():
                        if child.getText() == 'self' or child.getText().split(':')[0] == 'self':
                            raise selfassignment(
                                "'Self assignment' is a reserved word")
