import os
from sockgen.builder.settings import BuilderSettings as Set
from sockgen.data.models import *
from sockgen.core.messagecore import *

def createEnumeration(enum: EnumXML):
    if Set.DEBUG: print(enum)

    fileName = "{}.{}".format(enum.name, Set.fileExtension)
    filePath = os.path.join(os.path.curdir, Set.outputDir, Set.EnumerationSettings.outputDir, fileName)
    f = open(filePath, 'w')

    print("package {};\n".format(Set.EnumerationSettings.outputDir), file=f)
    print("import java.util.*;", file=f)
    print("", file=f)
    
    print("public enum {} {{\n".format(enum.name), file=f)
    for e in enum.values[:-1]:
        print(Set.tabstop * Set.tab + "{}({}),".format(e.enumName, e.enumValue), file=f)
    print(Set.tabstop * Set.tab + "{}({});\n".format(enum.values[-1].enumName, enum.values[-1].enumValue), file=f)
    
    print(Set.tabstop * Set.tab + "private final int value;", file=f)
    print(Set.tabstop * Set.tab + "private static Map<" + enum.name + ", String> map = new TreeMap<>();", file=f)
    print("\n")

    print(Set.tabstop * Set.tab + "static {", file=f)
    for e in enum.values:
        print(Set.tabstop * 2 * Set.tab + "map.put({}, \"{}\");".format(e.enumName, e.enumName), file=f)
    print(Set.tabstop * Set.tab + "}\n", file=f)
    
    print(Set.tabstop * Set.tab + "{} (int value) {{".format(enum.name), file=f)
    print(Set.tabstop * 2 * Set.tab + "this.value = value;", file=f)
    print(Set.tabstop * Set.tab + "}\n", file=f)
    
    print(Set.tabstop * Set.tab + "public int getValue() {", file=f)
    print(Set.tabstop * 2 * Set.tab + "return this.value;", file=f)
    print(Set.tabstop * Set.tab + "}\n", file=f)
    
    print(Set.tabstop * Set.tab + "public String getString() {", file=f)
    print(Set.tabstop * 2 * Set.tab + "if (map.isEmpty()) return super.toString();", file=f)
    print(Set.tabstop * 2 * Set.tab + "return map.get(getEnum(value));", file=f)
    print(Set.tabstop * Set.tab + "}\n", file=f)
    
    print(Set.tabstop * Set.tab + "public static Collection<String> getStringList() {", file=f)
    print(Set.tabstop * 2 * Set.tab + "return map.values();", file=f)
    print(Set.tabstop * Set.tab + "}\n", file=f)
    
    print(Set.tabstop * Set.tab + "public static {} getEnum(int value) {{".format(enum.name), file=f)
    print(Set.tabstop * 2 * Set.tab + "for ({e} e : {e}.values()) {{".format(e=enum.name), file=f)
    print(Set.tabstop * 3 * Set.tab + "if (e.getValue() == value) {", file=f)
    print(Set.tabstop * 4 * Set.tab + "return e;", file=f)
    print(Set.tabstop * 3 * Set.tab + "}", file=f)
    print(Set.tabstop * 2 * Set.tab + "}", file=f)
    print(Set.tabstop * 2 * Set.tab + "return null;", file=f)
    print(Set.tabstop * Set.tab + "}\n", file=f)
    
    print(Set.tabstop * Set.tab + "public static {} getEnum(String value) {{".format(enum.name), file=f)
    print(Set.tabstop * 2 * Set.tab + "for ({e} e : {e}.keySet()) {{".format(e=enum.name), file=f)
    print(Set.tabstop * 3 * Set.tab + "String temp = map.get(e);", file=f)
    print(Set.tabstop * 3 * Set.tab + "if (temp == value) {", file=f)
    print(Set.tabstop * 4 * Set.tab + "return e;", file=f)
    print(Set.tabstop * 3 * Set.tab + "}", file=f)
    print(Set.tabstop * 2 * Set.tab + "}", file=f)
    print(Set.tabstop * 2 * Set.tab + "return null;", file=f)
    print(Set.tabstop * Set.tab + "}\n", file=f)
    
    print("}", file=f)
    # End Of Create Enumeration