from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import *
from util.structure import _allClasses as classDict


prohibitedClassnames = {'Int': badredefineint,
                        'Object': redefinedobject, 'SELF_TYPE': selftyperedeclared}

prohibitedInheritance = {'Bool': inheritsbool,
                         'String': inheritsstring, 'SELF_TYPE': inheritsselftype}

symbolsArr = ['+', '-', '*', '/', '=', '<=', '<']


class semanticListener(coolListener):

    def __init__(self):
        setBaseKlasses()
        self.main = False
        self.currentKlass = None

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

        if ctx.feature():
            feature = ctx.feature()

        if className == 'Main':
            self.main = True

    def enterFeature(self, ctx: coolParser.FeatureContext):
        featureID = ctx.ID().getText()

        # Check if the feature is name self
        if featureID == 'self' or featureID == 'SELF_TYPE':
            raise anattributenamedself("Feature ID not valid (self)")

        if ctx.expr():
            if ctx.expr().getChild(1) in symbolsArr:
                if not ctx.expr().getChild(0) and ctx.expr().getChild(2):
                    raise badarith("")

            if ctx.expr().ID():
                exprName = ctx.expr().ID().getText()
                # Check if the expression is self
                if exprName == 'self':
                    raise selfassignment('Assignment to self is prohibited')
            # Check parameter
            if ctx.formal():
                if ctx.formal(0).ID().getText() == 'self':
                    raise selfinformalparameter(
                        'Using self as a parameter is prohibited')
                if ctx.formal(0).TYPE().getText() == 'SELF_TYPE':
                    raise selftypeparameterposition(
                        'SELF_TYPE cannot be used as a parameter type')

            expr = ctx.expr().getText()
            if ctx.expr().let_decl():
                let_params = ctx.expr().let_decl(0)
                if let_params.ID().getText() == 'self' or let_params.ID().getText() == 'SELF_TYPE':
                    raise letself("Let incorrect (using self)")

    def exitKlass(self, ctx: coolParser.KlassContext):
        if (not self.main):
            raise nomain()
