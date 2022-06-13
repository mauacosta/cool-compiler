from util.structure import * 
from util.structure import _allInts, _allStrings, _allClasses
import listeners.aTemplates as aTemplates
import math

globalInheritance = []
codeAssemblyOutput = ""
def auxDispTable(nameOfClass):
    #get class from name
    klass = lookupClass(nameOfClass)
    if klass.inherits != 'Object':
        globalInheritance.append(nameOfClass)
        auxDispTable(klass.inherits)
    if klass.inherits == 'Object':
        return 
     
    
def dispTable(): 
    temp = ""
    for singleClass in _allClasses:
        globalInheritance = []
        auxDispTable(singleClass)
        for index in range (len(globalInheritance)-1,-1,-1):
            actualKlass = lookupClass(globalInheritance[index])
            for method in actualKlass.methods:
                temp  += "     .word    " + actualKlass.name +"."+method.name + "\n"
    return temp

def previousTable():
    # create nameTable & ObjectTable
    objectIndex = _allStrings.index('Object')
    temp = "class_nameTab: \n"
    for index in range(objectIndex, len(_allStrings)-1):
        temp += "    .word    str_const" + str(index) + "\n"

    temp  += "class_objTab: \n"
    for singleClass in _allClasses:
        temp  += "    .word    " + str(singleClass) + "_protObj \n"
        temp += "    .word    " + str(singleClass) + "_init \n"
    return temp


def protObject():
    # create Object_protObj
    i = 0
    for singleClass in _allClasses:
        temp = ""
        temp += "    .word    -1 \n"
        temp += str(singleClass) + "_protObj: \n"
        temp  += "     .word    "+str(i)+" \n"
        actualKlass = lookupClass(singleClass)
        size =len(actualKlass.attributes)
        temp += "     .word    "+str(size)+"\n"
        temp  += "     .word    "+str(singleClass)+"dispTab\n"
        if size > 3:
            for attribute in actualKlass.attributes:
                if attribute == "Int":
                    temp += "     .word    str_const"+str(len(_allStrings)-1) + "\n"
                elif attribute == "String":
                    temp  += "     .word    int_const0 \n"
                else:
                    temp  += "     .word    0 \n"
        i +=1
        return temp

def codeGenerator():
    codeAssemblyOutput = ""
    codeAssemblyOutput += str(aTemplates.globalData)
    #string, int, bool const
    for i in range(len(_allStrings) -1,-1,-1):
        #get len of string without \\
        strLen = len(_allStrings[i])
        #get len in bytes
        size = int(4+math.ceil((strLen+1)/4))
        if not strLen in _allInts:
            #si tienen misma longitud PES TA ÑASTE
            _allInts.append(strLen)
            index = len(_allInts) - 1
        else:
            index = _allInts.index(strLen)
        codeAssemblyOutput += aTemplates.stringConst.substitute(index=i, size=size, intIndex =index ,value=_allStrings[i])
    for i in range(len(_allInts) -1,-1,-1):
        codeAssemblyOutput += str(aTemplates.intConst.substitute(index=i, value=_allInts[i]))
    codeAssemblyOutput += str(aTemplates.boolConst)
    codeAssemblyOutput += previousTable()
    codeAssemblyOutput +=dispTable()
    codeAssemblyOutput +=protObject()
    codeAssemblyOutput +=str(aTemplates.heap)
    codeAssemblyOutput +=str(aTemplates.objInit)
    codeAssemblyOutput +=str(aTemplates.iOInit)
    codeAssemblyOutput +=str(aTemplates.intInit)
    codeAssemblyOutput +=str(aTemplates.boolInit)
    codeAssemblyOutput +=str(aTemplates.stringInit)
    codeAssemblyOutput +=str(aTemplates.mainInit)
    print(codeAssemblyOutput)
    print("fin")