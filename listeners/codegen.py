from util.structure import * 
from util.structure import _allInts, _allStrings, _allClasses
import listeners.aTemplates as aTemplates
import math


codeAssemblyOutput = ""
def auxTable(nameOfClass, globalInheritance):
    #get class from name
    klass = lookupClass(nameOfClass)
    if klass.inherits != 'Object':
        globalInheritance = auxTable(klass.inherits, globalInheritance)
        globalInheritance.insert(0, nameOfClass)
    if klass.inherits == 'Object' and nameOfClass != 'Object':
        globalInheritance.insert(0, nameOfClass)
    return globalInheritance
     
    
def dispTable(): 
    temp = ""
    for singleClass in _allClasses:
        temp += singleClass + "_dispTab:\n"
        globalInheritance = auxTable(singleClass, ['Object'])
        #print(singleClass + ": " + str(globalInheritance))
        for index in range (len(globalInheritance)-1,-1,-1):
            actualKlass = lookupClass(globalInheritance[index])
            for method in actualKlass.methods:
                temp  += "       .word    " +globalInheritance[index] +"."+method + "\n"
    return temp

def previousTable():
    # create nameTable & ObjectTable
    objectIndex = _allStrings.index('Object')
    temp = "class_nameTab: \n"
    for index in range(objectIndex, len(_allStrings)-1):
        temp += "       .word    str_const" + str(index) + "\n"

    temp  += "class_objTab: \n"
    for singleClass in _allClasses:
        temp  += "       .word    " + str(singleClass) + "_protObj \n"
        temp += "       .word    " + str(singleClass) + "_init \n"
    return temp


def protObject():
    # create Object_protObj
    i = 0
    temp = ""
    for singleClass in _allClasses:
        print(singleClass)
        temp += str(singleClass) + "_protObj: \n"
        temp  += "\t.word    "+str(i)+" \n"
        actualKlass = lookupClass(singleClass)
        size = len(actualKlass.attributes)
        if actualKlass.inherits:
            size += len(lookupClass(singleClass).attributes)
        temp += "\t.word    "+str(size)+"\n"
        temp  += "\t.word    "+str(singleClass)+"dispTab\n"
        if size > 3:
            for att in actualKlass.attributes:
                if att == "Int":
                    temp += "\t.word    str_const"+str(len(_allStrings)-1) + "\n"
                elif att == "String":
                    temp  += "\t.word    int_const0 \n"
                else:
                    temp  += "\t.word    0 \n"
        temp  += "\t.word    -1\n"
        i +=1
    return temp

def methods():
    temp = ""
    for singleClass in _allClasses:
        actualKlass = lookupClass(singleClass)
        temp2=""
        for method in actualKlass.methods:
            actualMethod = actualKlass.lookupMethod(method)
            #Get number of locals
            nLocals = 0
            ts = (3+nLocals)*4 #3+ nLocals * 4
            temp2 += str(aTemplates.protEnterMethod.substitute(className= singleClass, methodName = method,ts=ts, fp=ts, s0=ts-4, ra=ts-8, nLocal=nLocals))
        temp = temp2 + temp
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
    codeAssemblyOutput += str(aTemplates.boolConst.substitute())
    codeAssemblyOutput += previousTable()
    codeAssemblyOutput += dispTable()
    codeAssemblyOutput += protObject()
    codeAssemblyOutput +=str(aTemplates.heap.substitute())
    codeAssemblyOutput +=str(aTemplates.objInit.substitute())
    for singleClass in _allClasses:
        actualKlass = lookupClass(singleClass)
        codeAssemblyOutput += str(aTemplates.protInit.substitute(classInit = singleClass+"_init", jal=actualKlass.inherits+"_init"))
    codeAssemblyOutput +=methods()

    print(codeAssemblyOutput)