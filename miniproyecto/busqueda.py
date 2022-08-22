import types as t
import numpy as np
class Nodo:

    # Clase para crear los nodos

    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo

def nodo_hijo(problema, madre, accion):

    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo

    estado = problema.transicion(madre.estado, accion)
    costo_camino = madre.costo_camino + problema.costo(madre.estado, accion)
    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)

def solucion(n):
    if n.madre == None:
        return []
    else:
        return solucion(n.madre) + [n.accion]

def backtracking_search(problema, estado):

    '''Función de búsqueda recursiva de backtracking'''

    if problema.test_objetivo(estado):
            return estado
    acciones = problema.acciones_aplicables(estado)
    for a in acciones:
        hijo = problema.transicion(estado, a)
        resultado = backtracking_search(problema, hijo)
        if resultado is not None:
            return resultado
    return None

def breadth_first_search(problema):

    '''Función de búsqueda breadth-first'''

    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.codigo(problema.estado_inicial))
    if problema.test_objetivo(nodo.estado):
            return nodo
    frontera = [nodo]
    explorados = []
    while len(frontera) > 0:
        nodo = frontera.pop(0)
        explorados.append(nodo.codigo)
        acciones = problema.acciones_aplicables(nodo.estado)
        for a in acciones:
            hijo = nodo_hijo(problema, nodo, a)
            if problema.test_objetivo(hijo.estado):
                return hijo
            if hijo.codigo not in explorados:
                frontera.append(hijo)
    return None

def depth_first_search(problema):

    '''Función de búsqueda depth-first'''

    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.codigo(problema.estado_inicial))
    if problema.test_objetivo(nodo.estado):
            return nodo
    frontera = [nodo]
    explorados = []
    while len(frontera) > 0:
        nodo = frontera.pop()
        explorados.append(nodo.codigo)
        acciones = problema.acciones_aplicables(nodo.estado)
        for a in acciones:
            hijo = nodo_hijo(problema, nodo, a)
            if problema.test_objetivo(hijo.estado):
                return hijo
            if hijo.codigo not in explorados:
                frontera.append(hijo)
    return None

def depth(n):
    if n.madre == None:
        return 0
    else:
        return 1 + depth(n.madre)

def ancestros(n):
    if n.madre == None:
        return [n.codigo] 
    else:
        return ancestros(n.madre) + [n.codigo]

def is_cycle(n): #verdadero si el camino por el que se creo tiene estados repetidos buscar lista de codigos de los ancestros y buscar repeticiones
    codes = ancestros(n)
    return len(set(codes)) != len(codes)

def expand(problema, nodo):
    s = nodo.estado
    nodos = []
    for accion in problema.acciones_aplicables(s):
        hijo = nodo_hijo(problema, nodo, accion)
        nodos.append(hijo)
    return nodos

def depth_limited_search(problema, l):
    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.codigo(problema.estado_inicial))
    frontera = [nodo]
    resultado = "Falla"
    while len(frontera) > 0:
        nodo = frontera.pop()
        if problema.test_objetivo(nodo.estado):
            return nodo
        if depth(nodo) >= l:
            resultado = "Cutoff"
        elif is_cycle(nodo) == False:
            for hijo in expand(problema, nodo):
                frontera.append(hijo)
    return resultado

def iterative_deepening_search(problema, l_max):
    for i in range (0, l_max+1):
        resultado = depth_limited_search(problema, i)
        if resultado != "Cutoff":
            return resultado 

class ListaPrioritaria():
    
    def __init__(self):
        self.diccionario = {}
        
    def __str__(self):
        cadena = '['
        inicial = True
        for costo in self.diccionario:
            elementos = self.diccionario[costo]
            for elemento in elementos:
                if inicial:
                    cadena += '(' + str(elemento) + ',' + str(costo) + ')'
                    inicial = False
                else:
                    cadena += ', (' + str(elemento) + ',' + str(costo) + ')'

        return cadena + ']'
    
    def push(self, elemento, costo):
        try:
            self.diccionario[costo].append(elemento)
        except:
            self.diccionario[costo] = [elemento]
            
    def pop(self):
        min_costo = min(list(self.diccionario.keys()))
        candidatos = self.diccionario[min_costo]
        elemento = candidatos.pop()
        if len(candidatos) == 0:
            del self.diccionario[min_costo]
        return elemento
    
    def is_empty(self):
        return len(self.diccionario) == 0
        

def best_first_search(problema, f):
    if not f == None:
        problema.costo = t.MethodType(f,problema)
    s = problema.estado_inicial
    cod = problema.codigo(s)
    nodo = Nodo(s, None, None, 0, cod)
    frontera = ListaPrioritaria()
    frontera.push(nodo, 0)
    explorados = {cod : 0}
    while not frontera.is_empty():
        nodo = frontera.pop()
        if problema.test_objetivo(nodo.estado):
            return nodo
        for hijo in expand(problema, nodo):
            s = hijo.estado
            cod = problema.codigo(s)
            c = hijo.costo_camino
            if cod not in explorados.keys() or c < explorados[cod]:
                frontera.push(hijo,c)
                explorados[cod] = c
    return None

def costo_uniforme(self,estado, accion):
    return 1

def greedy_search(problema, f):
    s = problema.estado_inicial
    nodo = Nodo(s, None, None, 0, problema.codigo(s))
    v = f(s)
    frontera = ListaPrioritaria()
    frontera.push(nodo, v)
    cod = problema.codigo(s)
    explorados = [cod]
    while (not frontera.is_empty()) and frontera.len < 100:
        nodo = frontera.pop()
        if problema.test_objetivo(nodo.estado):
            return nodo
        for hijo in expand(problema, nodo):
            s = hijo.estado
            cod = problema.codigo (s)
            if cod not in explorados:
                v = f(s)
                frontera.push(hijo, v)
                explorados.append(cod)
    return None