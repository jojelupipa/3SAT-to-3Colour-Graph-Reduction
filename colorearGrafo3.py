# colorearGrafo3.py
# Autores: Miguel Lentisco Ballesteros y Jesús Sánchez de Lechina Tejada
# Descripción:
# Este programa lee de un archivo de texto un problema de tipo SAT3 (unas variables y unas cláusulas que
# para toda cláusula tiene que ser cierta) y lo reduce al problema de colorear un grafo con 3 colores (creando así
# una grafo que si se puede colorear con 3 colores entonces se puede resolver el problema SAT3 inicial). Además este
# se implementa un algoritmo para ver si se puede colorear el grafo con 3 colores (exponencial) y en cuyo caso imprime
# el grafo resultante y además imprime los valores de verdad para resolver el problema SAT3

# Imports
import copy
import sys

# Parser para leer las variables y las variables del fichero de entrada
def lectura_fichero():
    if len(sys.argv) != 2:
        print("Error en nº de argumentos. Uso: python colorearGrafo3.py nombreFichero.txt")
        sys.exit()
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

    # Procesamos el contenido del fichero. Las variables las metemos en un
    # string con el resto de variables y las cláusulas como strings en una lista
    listaStringClausulas = []
    for linea in sinSaltos:
        if linea.find("variables:") != -1:
            indice = linea.find(":")
            stringVariables = linea[indice + 1:]
            # Borramos los primeros espacios si los hubiera
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
    # (eliminamos los "or")
    for i in range(0, len(listaStringClausulas)):
        while listaStringClausulas[i].find("or") != -1:
            listaStringClausulas[i] = listaStringClausulas[i].replace("or", "")


    # Pasamos los strings de las cláusulas a una lista de objetos de la clase Clausula
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

    # Muestra resultados
    print("Variables:")
    print(listaVariables)
    print("\nCláusulas:")
    for clausula in listaClausulas:
        print(clausula.l1 + " " + clausula.l2 + " " + clausula.l3)
    print()
    return [listaVariables, listaClausulas]

# Representa un nodo del grafo
class Nodo:
    def __init__(self, nombre, nodos_conectados, color):
        self.nombre = nombre
        self.nodos_conectados = list(nodos_conectados)
        self.conectar_nodo(self.nodos_conectados)
        self.color = color

    def __str__(self):
        msg = "Nodo: " + self.nombre + ", color: " + self.color + ", nodos conectados: ["
        for nodo in self.nodos_conectados:
            msg = msg + nodo.nombre + ", "
        if len(self.nodos_conectados) > 0:
            msg = msg[:-1]
            msg = msg[:-1]
        msg = msg + "]"
        return msg

    def __repr__(self):
        return str(self)

    # Añade una conexión entre nodo argumento y el actual
    def conectar_nodo(self, nodos):
        for nodo in nodos:
            if nodo not in self.nodos_conectados:
                self.nodos_conectados.append(nodo)
            if self not in nodo.nodos_conectados:
                nodo.nodos_conectados.append(self)

# Una cláusula en 3-SAT son 3 literales unidos por OR (representamos con cadenas de texto)
class Clausula:
    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
    def __str__(self):
        return self.l1 + " OR " + self.l2 + " OR " + self.l3
    def __repr__(self):
        return str(self)

# Representa la reducción del problema SAT3 al problema de colorear un grafo con 3 colores
class Grafo:
    def __init__ (self, variables, clausulas):
        self.nodos_base = []
        self.nodos_variable = []
        self.nodos_puertas = []
        self.variables = list(variables)
        self.clausulas = list(clausulas)

    def __str__(self):
        return "Grafo: \n" + str(self.nodos_base + self.nodos_variable + self.nodos_puertas)

    # Aux: Buscar un nodo por nombre
    def busca_nodo(self, nombre):
        return next(x for x in self.nodos_variable if x.nombre == nombre)

    # Inicializa el grafo con los nodo base, verdad y falso
    def inicializar_grafo(self):
        base = Nodo("Base", [], "B")
        verdad = Nodo("Verdad", [base], "V")
        falso = Nodo("Falso", [verdad, base], "F")
        self.nodos_base = [base, verdad, falso]

    # Crea los nodos de variables (variable y variable negada) y forma un triángulo
    def crea_nodos_variables(self):
        for variable in self.variables:
            n_var = Nodo(variable, [self.nodos_base[0]], "")
            n_var_negada = Nodo("¬" + variable, [self.nodos_base[0], n_var], "")
            self.nodos_variable = self.nodos_variable + [n_var, n_var_negada]

    # Crea la estructura de puerta OR en el grafo y devuelve el nodo resultado de la puerta
    def crea_puerta_or(self, n1, n2, i, j):
        n11 = Nodo("C" + str(i) + str(j), [n1], "")
        n21 = Nodo("C" + str(i) + str(j + 1), [n11, n2], "")
        n3 = Nodo("C" + str(i) + str(j + 2), [n11, n21], "")
        self.nodos_puertas = self.nodos_puertas + [n11, n21, n3]
        return n3

    # Crea las puertas OR según las cláusulas
    def crea_nodos_puertas(self):
        # Para cada cláusula repetimos la misma estructura
        for i in range(0, len(self.clausulas)):
            clausula = self.clausulas[i]
            # Tomamos los nodos de los literales de la cláusula
            n1 = self.busca_nodo(clausula.l1)
            n2 = self.busca_nodo(clausula.l2)
            n3 = self.busca_nodo(clausula.l3)
            nRes1 = self.crea_puerta_or(n1, n2, i + 1, 1)
            nRes2 = self.crea_puerta_or(nRes1, n3, i + 1, 4)
            # Conectamos la última con base y falso para que se pinte con "T"
            nRes2.conectar_nodo([self.nodos_base[0], self.nodos_base[2]])

    # Crea el grafo a partir de la reducción SAT
    def crear_grafo(self):
        self.inicializar_grafo()
        self.crea_nodos_variables()
        self.crea_nodos_puertas()

    # Los colores disponibles para pintar el nodo
    def colores_disponibles(self, nodo):
        colores = ["B", "V", "F"]
        for vecino in nodo.nodos_conectados:
            try:
                colores.remove(vecino.color)
            except ValueError:
                pass
        return colores

    # Función que devuelve si se puede colorear o no el grafo con 3 colores, en caso de que sí deja el grafo coloreado
    def alg_colorear_3_colores(self):
        nodos = []
        for nodo in (self.nodos_puertas + self.nodos_variable):
            if nodo.color == "":
                nodos.append(nodo)
        return self.colorea_grafo(nodos)

    # Función recursiva para colorear el subgrafo
    def colorea_grafo(self, nodos):
        # Si no hay nodos por pintar, el grafo es coloreable
        if nodos == []:
            return True
        # Si quedan nodos por pintar, tomo el primero
        nodo = nodos[0]
        # Tomo la lista de colores disponibles para pintar
        colores = self.colores_disponibles(nodo)
        # Si no se puede pintar el subgrafo no es coloreable
        if len(colores) == 0:
            return False
        nodos_nuevos = copy.copy(nodos)
        nodos_nuevos.remove(nodo)
        # Por cada color disponible pinto el nodo y veo si es coloreable el subgrafo
        for color in colores:
            nodo.color = color
            res = self.colorea_grafo(nodos_nuevos)
            # Si se puede colorear devuelvo que sí
            if res:
                return True
        # Si no se puede colorear de ninguna manera devuelvo que no
        nodo.color = ""
        return False

    # Devuelve los valores de verdad de SAT3 si se puede colorear
    def to_sat3(self):
        es_resoluble = self.alg_colorear_3_colores()
        msg = ""
        if es_resoluble:
            msg = "Resolución SAT3, valores de verdad:"
            for i in range(0, len(self.nodos_variable), 2):
                msg = msg + "\n" + self.nodos_variable[i].nombre + " = " + self.nodos_variable[i].color
        else:
            msg = "No se puede resolver el problema SAT3/Colorear el grafo con 3 colores."
        return msg

# Main
def main():
    res = lectura_fichero()
    grafo_SAT3 = Grafo(res[0], res[1])
    grafo_SAT3.crear_grafo()
    print(grafo_SAT3)
    print()
    print(grafo_SAT3.to_sat3())

if __name__ == '__main__':
    main()
