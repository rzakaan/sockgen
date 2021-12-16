from message_generator.data.models import *
from message_generator.core.messagecore import *



def createEnumeration(enum: EnumXML):
    if Conf.DEBUG: print(enum)
    
    f = open("{}.{}".format(enum.name, Conf.fileExtension), 'w')
    print("package enumeration;\n", file=f)
    print("import java.util.*;", file=f)
    print("", file=f)
    
    print("public enum {} {{\n".format(enum.name), file=f)
    for e in enum.values[:-1]:
        print(Conf.tabstop * ' ' + "{}({}),".format(e.enumName, e.enumValue), file=f)
    print(Conf.tabstop * ' ' + "{}({});\n".format(enum.values[-1].enumName, enum.values[-1].enumValue), file=f)
    
    print(Conf.tabstop * ' ' + "private final int value;", file=f)
    print(Conf.tabstop * ' ' + "private static Map<" + enum.name + ", String> map = new TreeMap<>();", file=f)
    print("\n")

    print(Conf.tabstop * ' ' + "static {", file=f)
    for e in enum.values:
        print(Conf.tabstop * 2 * ' ' + "map.put({}, \"{}\");".format(e.enumName, e.enumName), file=f)
    print(Conf.tabstop * ' ' + "}\n", file=f)
    
    print(Conf.tabstop * ' ' + "{} (int value) {{".format(enum.name), file=f)
    print(Conf.tabstop * 2 * ' ' + "this.value = value;", file=f)
    print(Conf.tabstop * ' ' + "}\n", file=f)
    
    print(Conf.tabstop * ' ' + "public int getValue() {", file=f)
    print(Conf.tabstop * 2 * ' ' + "return this.value;", file=f)
    print(Conf.tabstop * ' ' + "}\n", file=f)
    
    print(Conf.tabstop * ' ' + "public String getString() {", file=f)
    print(Conf.tabstop * 2 * ' ' + "if (map.isEmpty()) return super.toString();", file=f)
    print(Conf.tabstop * 2 * ' ' + "return map.get(getEnum(value));", file=f)
    print(Conf.tabstop * ' ' + "}\n", file=f)
    
    print(Conf.tabstop * ' ' + "public static Collection<String> getStringList() {", file=f)
    print(Conf.tabstop * 2 * ' ' + "return map.values();", file=f)
    print(Conf.tabstop * ' ' + "}\n", file=f)
    
    print(Conf.tabstop * ' ' + "public static {} getEnum(int value) {{".format(enum.name), file=f)
    print(Conf.tabstop * 2 * ' ' + "for ({e} e : {e}.values()) {{".format(e=enum.name), file=f)
    print(Conf.tabstop * 3 * ' ' + "if (e.getValue() == value) {", file=f)
    print(Conf.tabstop * 4 * ' ' + "return e;", file=f)
    print(Conf.tabstop * 3 * ' ' + "}", file=f)
    print(Conf.tabstop * 2 * ' ' + "}", file=f)
    print(Conf.tabstop * 2 * ' ' + "return null;", file=f)
    print(Conf.tabstop * ' ' + "}\n", file=f)
    
    print(Conf.tabstop * ' ' + "public static {} getEnum(String value) {{".format(enum.name), file=f)
    print(Conf.tabstop * 2 * ' ' + "for ({e} e : {e}.keySet()) {{".format(e=enum.name), file=f)
    print(Conf.tabstop * 3 * ' ' + "String temp = map.get(e);", file=f)
    print(Conf.tabstop * 3 * ' ' + "if (temp == value) {", file=f)
    print(Conf.tabstop * 4 * ' ' + "return e;", file=f)
    print(Conf.tabstop * 3 * ' ' + "}", file=f)
    print(Conf.tabstop * 2 * ' ' + "}", file=f)
    print(Conf.tabstop * 2 * ' ' + "return null;", file=f)
    print(Conf.tabstop * ' ' + "}\n", file=f)
    
    print("}", file=f)
    # End Of Create Enumeration

#getterAndSetter += "\n"
#getterAndSetter += Conf.tabstop * " " + "private void set{}({} value) {{\n".format(functionName, strDataFormatType)
#getterAndSetter += Conf.tabstop * 2 * " " + "{} = value;\n".format(recordElement.name)
#getterAndSetter += Conf.tabstop * " " + '}\n'

#getterAndSetter += "\n"
#getterAndSetter += Conf.tabstop * " " + "private {} get{}() {{\n".format(strDataFormatType, functionName)
#getterAndSetter += Conf.tabstop * 2 * " " + "return {};\n".format(recordElement.name)
#getterAndSetter += Conf.tabstop * " " + '}\n'