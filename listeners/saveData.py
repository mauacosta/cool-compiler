from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allStrings, _allInts, _allBool, _allClasses;

class saveDataListener(coolListener):

    def __init__(self):
        self.main = False

    def enterKlass(self, ctx: coolParser.KlassContext):
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True
        _allClasses.append('--filename--')
        _allClasses.append('\\n')

    def exitKlass(self, ctx: coolParser.KlassContext):
        if (not self.main):
            raise nomain("Class 'Main' not found")

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if (ctx.STRING()):
            # guardar en allString
            s = ctx.STRING.getText()[1:-1]
            if s not in _allStrings:
                _allStrings.append(s)
        elif (ctx.INTEGER()):
            # guardar en allInt
            i = int(ctx.INTEGER.getText())
            if i not in _allInts:
                _allInts.append(i)
        elif (ctx.TRUE()):
            # guardar en allBool
            b = ctx.TRUE().getText()
            if b not in _allBool:
                _allBool.append(b)
        elif(ctx.FALSE()):
            # guardar en allBool
            b = ctx.FALSE().getText()
            if b not in _allBool:
                _allBool.append(b)
        else:
            print("Error")
    def exitProgram(self, ctx: coolParser.ProgramContext):
        _allStrings.append('<basic_class>')
        for singleClass in _allClasses:
            _allStrings.append(singleClass)
            




