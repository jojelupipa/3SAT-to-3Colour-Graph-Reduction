import sys

class Clausula:
    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3


ficheroEntrada = open(sys.argv[1], "r")
contenido = ficheroEntrada.readlines()
ficheroEntrada.close()

# Quitamos las líneas vacías
sinSaltos = list(filter(lambda x: x != '\n', contenido))
# Quitamos los saltos de línea al final de cada línea
sinSaltos = list(map(lambda x: x.rstrip('\n'), sinSaltos))

# Lo ponemos todo en minúscula
for i in range(0, len(sinSaltos)):
    sinSaltos[i] = sinSaltos[i].lower()

listaStringClausulas = []
for linea in sinSaltos:
    if linea.find("variables:") != -1:
        indice = linea.find(":")
        stringVariables = linea[indice + 1:]
        # Borramos los primeros espacios si ls hubiera
        while stringVariables[0] == ' ':
            stringVariables = stringVariables[1:]
    elif linea.find("clausulas") == -1:
        listaStringClausulas.append(linea)

# Obtenemos una lista de strings para las variables 
variable = ""
listaVariables = []
for caracter in stringVariables:
    if caracter == " " and variable != "":
        listaVariables.append(variable)
        variable = ""
    else:
        variable += caracter

listaVariables.append(variable)

# Formateamos correctamente el string de la lista de cláusulas
for i in range(0, len(listaStringClausulas)):
    while listaStringClausulas[i].find("or") != -1:
        listaStringClausulas[i] = listaStringClausulas[i].replace("or", "")

#print(listaStringClausulas)
listaLiterales = []
listaClausulas = []

for string in listaStringClausulas:
    literal = ""
    for c in string:
        if c == " " and literal != "":
            listaLiterales.append(literal)
            literal = ""
        elif c != " ":
            literal += c
    listaLiterales.append(literal)
    listaClausulas.append(Clausula(listaLiterales[0], listaLiterales[1], listaLiterales[2]))
    listaLiterales = []
        

print(listaVariables)

for clausula in listaClausulas:
    print(clausula.l1 + " " + clausula.l2 + " " + clausula.l3)

    