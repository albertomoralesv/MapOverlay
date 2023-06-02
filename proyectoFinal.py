import pygame
import pygame.locals
from copy import copy
import random
import math
####
segmentos = {}
####

class Vertice:
    def __init__(self, *args):
        self.x, self.y = args[0], args[1]
        self.i = args[2]
        self.x = round(self.x,2)
        self.y = round(self.y,2)
    
    def __repr__(self):
        return f"({self.x:.2f},{self.y:.2f})"
    def __eq__(self, other):
      return abs(self.x-other.x)<0.0001 and abs(self.y-other.y)<0.0001
      #if len(self.coords)!= len(other.coords):
      #if len(self.coords)!= len(other.coords):
    def __hash__(self):
          return hash((self.x, self.y))
  
class Arista:
    def __init__(self, *args):
        self.nombre, self.origen, self.pareja, self.cara, self.sigue, self.antes = args[0],args[1],args[2],args[3],args[4],args[5]

class Segmento:
    def __init__(self, nombre, p1, p2):
        self.nombre = nombre
        self.inicio = {}
        self.final = {}
        if p1.y > p2.y:
            self.p1 = p1
            self.p2 = p2
        elif p1.y < p2.y:
            self.p1 = p2
            self.p2 = p1
        else:
            if p1.x < p2.x:
                self.p1 = p1
                self.p2 = p2
            else:
                self.p1 = p2
                self.p2 = p1
    #### 
    def getX(self,y):
        if self.p1.x != self.p2.x:
            m = (self.p2.y-self.p1.y)/(self.p2.x-self.p1.x)
            b = self.p1.y - m*self.p1.x
            if self.p1.y != self.p2.y:
                x = (y - b) / m
            else:
                x = None
        else:
            x = self.p1.x
        if x is not None:
            x = round(x,2)
        return x
    ###
    def __eq__(self, other):
      return self.p1==other.p1 and self.p2==other.p2
    def __hash__(self):
          return hash((self.p1, self.p2))
    def __repr__(self):
        return f"({self.p1.x},{self.p1.y}) ({self.p2.x},{self.p2.y}) {self.nombre}"

pygame.init()
mult = 30
width = 15*mult
additional_height = (15*mult)/12
height = 15*mult+additional_height
screen = pygame.display.set_mode((width, height))
running = True
screen.fill("purple")

#################################################
#################################################

figuras = {}

numLayers = 5

for layer in range(1,numLayers+1):
    figuras[layer] = {}
    figuras[layer]["vertices"] = {}
    figuras[layer]["aristas"] = {}
    figuras[layer]["segmentos"] = {}
    figuras[layer]["caras"] = {}
    nLayer = str(layer)
    if layer < 10:
        nLayer = "0"+str(layer)
    docVertices = "layer"+nLayer+".vertices"
    verticesTxt = open(docVertices)
    verticesTxt.readline()
    verticesTxt.readline()
    verticesTxt.readline()
    verticesTxt.readline()
    for linea in verticesTxt.readlines():
        linea = linea.split()
        figuras[layer]["vertices"][linea[0]] = Vertice(float(linea[1]),float(linea[2]),linea[3])
        #print(figuras[layer]["vertices"][linea[0]])
    docAristas = "layer"+nLayer+".aristas"
    aristasTxt = open(docAristas)
    aristasTxt.readline()
    aristasTxt.readline()
    aristasTxt.readline()
    aristasTxt.readline()
    for linea in aristasTxt.readlines():
        linea = linea.split()
        figuras[layer]["aristas"][linea[0]] = Arista(linea[0],linea[1],linea[2],linea[3],linea[4],linea[5])
    for arista in figuras[layer]["aristas"]:
        v1 = figuras[layer]["aristas"][arista].origen
        p1 = figuras[layer]["vertices"][v1]
        v2 = figuras[layer]["aristas"][figuras[layer]["aristas"][arista].pareja].origen
        p2 = figuras[layer]["vertices"][v2]
        segmento = Segmento(arista, p1, p2)
        figuras[layer]["segmentos"][arista] = segmento
        ##
        segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),p1,p2)
        ##
    for segmento in figuras[layer]["segmentos"]:
        p1 = figuras[layer]["segmentos"][segmento].p1
        p2 = figuras[layer]["segmentos"][segmento].p2
        pygame.draw.line(screen, (0,255,0), (p1.x*mult,abs(p1.y*mult-height)), (p2.x*mult,abs(p2.y*mult-height)), 1)
        pygame.display.update()
################


class Evento:
    def __init__(self,punto,numSegmento,tipo):
        self.punto = punto
        self.numSegmento = numSegmento
        self.tipo = tipo
    def __repr__(self):
      return f"[{self.punto},{self.numSegmento},{self.tipo}]"
        
eventos = []

segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),Vertice(0,0,"b1"),Vertice(0,15,"b2"))
segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),Vertice(0,15,"b1"),Vertice(0,0,"b2"))
pygame.draw.line(screen, (0,255,0), (segmentos[len(segmentos)].p1.x*mult,abs(segmentos[len(segmentos)].p1.y*mult-height)), (segmentos[len(segmentos)].p2.x*mult,abs(segmentos[len(segmentos)].p2.y*mult-height)), 1)
segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),Vertice(0,15,"b2"),Vertice(15,15,"b3"))
segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),Vertice(15,15,"b2"),Vertice(0,15,"b3"))
pygame.draw.line(screen, (0,255,0), (segmentos[len(segmentos)].p1.x*mult,abs(segmentos[len(segmentos)].p1.y*mult-height)), (segmentos[len(segmentos)].p2.x*mult,abs(segmentos[len(segmentos)].p2.y*mult-height)), 1)
segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),Vertice(15,15,"b3"),Vertice(15,0,"b4"))
segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),Vertice(15,0,"b3"),Vertice(15,15,"b4"))
pygame.draw.line(screen, (0,255,0), (segmentos[len(segmentos)].p1.x*mult,abs(segmentos[len(segmentos)].p1.y*mult-height)), (segmentos[len(segmentos)].p2.x*mult,abs(segmentos[len(segmentos)].p2.y*mult-height)), 1)
segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),Vertice(15,0,"b4"),Vertice(0,0,"b1"))
segmentos[len(segmentos)+1] = Segmento(str(len(segmentos)+1),Vertice(0,0,"b4"),Vertice(15,0,"b1"))
pygame.draw.line(screen, (0,255,0), (segmentos[len(segmentos)].p1.x*mult,abs(segmentos[len(segmentos)].p1.y*mult-height)), (segmentos[len(segmentos)].p2.x*mult,abs(segmentos[len(segmentos)].p2.y*mult-height)), 1)
pygame.draw.line(screen, (0,255,0), (segmentos[len(segmentos)].p1.x*mult,abs(segmentos[len(segmentos)].p1.y*mult-height)), (segmentos[len(segmentos)].p2.x*mult,abs(segmentos[len(segmentos)].p2.y*mult-height)), 1)

pygame.display.update()

for segmento in segmentos:
    eventos.append(Evento(segmentos[segmento].p1,segmento,"superior"))
    eventos.append(Evento(segmentos[segmento].p2,segmento,"inferior"))
"""
for segmento in segmentos:
    print(segmento, segmentos[segmento])
"""
eventos =  sorted(eventos, key = lambda evento:(-evento.punto.y,evento.punto.x,-ord(evento.tipo[0])))

activas = set()

for evento in eventos:
    if evento.tipo == "inferior":
        activas.remove(evento.numSegmento)
    for numSegmento in activas:
        segmento = segmentos[numSegmento]
        intX = segmento.getX(evento.punto.y)
        if intX is None:
            intX = evento.punto.x
        if intX < evento.punto.x:
            if evento.tipo == "superior":
                segmentos[evento.numSegmento].inicio[numSegmento] = -1
                segmentos[numSegmento].inicio[evento.numSegmento] = 1
            else:
                if numSegmento in segmentos[evento.numSegmento].inicio:
                    if segmentos[evento.numSegmento].inicio[numSegmento] != -1:
                        segmentos[evento.numSegmento].final[numSegmento] = -1
                    else:
                        pass
                        #segmentos[evento.numSegmento].inicio.pop(numSegmento)
                elif evento.numSegmento in segmentos[numSegmento].inicio:
                    if segmentos[numSegmento].inicio[evento.numSegmento] != 1:
                        segmentos[numSegmento].final[evento.numSegmento] = 1
                    else:
                        pass
                        #segmentos[numSegmento].final.pop(evento.numSegmento)
        elif intX > evento.punto.x:
            if evento.tipo == "superior":
                segmentos[evento.numSegmento].inicio[numSegmento] = 1
                segmentos[numSegmento].inicio[evento.numSegmento] = -1
            else:
                if numSegmento in segmentos[evento.numSegmento].inicio:
                   if segmentos[evento.numSegmento].inicio[numSegmento] != 1:
                       segmentos[evento.numSegmento].final[numSegmento] = 1
                   else:
                       pass
                       #segmentos[evento.numSegmento].inicio.pop(numSegmento)
                elif evento.numSegmento in segmentos[numSegmento].inicio:
                    if segmentos[numSegmento].inicio[evento.numSegmento] != -1:
                        segmentos[numSegmento].final[evento.numSegmento] = -1
                    else:
                        pass
                        #segmentos[numSegmento].final.pop(evento.numSegmento)
        elif intX == evento.punto.x:
            if evento.tipo == "superior":
                segmentos[evento.numSegmento].inicio[numSegmento] = 0
                segmentos[numSegmento].inicio[evento.numSegmento] = 0
            else:
                if numSegmento in segmentos[evento.numSegmento].inicio:
                    segmentos[evento.numSegmento].final[numSegmento] = 0
                elif evento.numSegmento in segmentos[numSegmento].inicio:
                    segmentos[numSegmento].final[evento.numSegmento] = 0
    if evento.tipo == "superior":
        activas.add(evento.numSegmento)    


def interseccionSegmentos(p1, p2, q1, q2):
    interseccion = []
    
    # Calculate slopes
    if p2.x != p1.x:
        mp = (p2.y - p1.y) / (p2.x - p1.x)
    else:
        mp = None

    if q2.x != q1.x:
        mq = (q2.y - q1.y) / (q2.x - q1.x)
    else:
        mq = None
    
    # Check if the lines are parallel
    if mp == mq:
        if p1.x == q1.x and is_between(p1.y, q1.y, q2.y):
            interseccion.append(Vertice(p1.x, p1.y, None))
        if p2.x == q1.x and is_between(p2.y, q1.y, q2.y):
            interseccion.append(Vertice(p2.x, p2.y, None))
        if q1.x == p1.x and is_between(q1.y, p1.y, p2.y):
            interseccion.append(Vertice(q1.x, q1.y, None))
        if q2.x == p1.x and is_between(q2.y, p1.y, p2.y):
            interseccion.append(Vertice(q2.x, q2.y, None))
            
        return interseccion
    
    # Calculate intersection coordinates
    if mp is not None and mq is not None:
        interseccionX = (q1.y - p1.y + mp * p1.x - mq * q1.x) / (mp - mq)
        interseccionY = p1.y + mp * (interseccionX - p1.x)
    elif mp is None:
        interseccionX = p1.x
        interseccionY = q1.y + mq * (interseccionX - q1.x)
    else:  # mq is None
        interseccionX = q1.x
        interseccionY = p1.y + mp * (interseccionX - p1.x)
    
    # Check if the intersection point is within the range of the line segments
    if (
        is_between(interseccionX, p1.x, p2.x)
        and is_between(interseccionY, p1.y, p2.y)
        and is_between(interseccionX, q1.x, q2.x)
        and is_between(interseccionY, q1.y, q2.y)
    ):
        interseccion.append(Vertice(round(interseccionX, 2), round(interseccionY, 2), None))
    
    return interseccion


def is_between(value, a, b):
    return min(a, b) <= value <= max(a, b)

intersecciones = {}    
for segmento in segmentos:
    #print("--- ",segmentos[segmento].nombre, segmentos[segmento].p1,segmentos[segmento].p2,segmentos[segmento].final)
    for segmentoInterseccion in segmentos[segmento].final:
        it = interseccionSegmentos(copy(segmentos[segmento].p1),
                                   copy(segmentos[segmento].p2),
                                   copy(segmentos[segmentoInterseccion].p1),
                                   copy(segmentos[segmentoInterseccion].p2))
        if len(it)>0:
            #interseccion = it[0]
            for interseccion in it:
                if interseccion.x not in intersecciones:
                    intersecciones[interseccion.x] = {}
                    intersecciones[interseccion.x][interseccion.y] = set()
                    intersecciones[interseccion.x][interseccion.y].add(segmento)
                    intersecciones[interseccion.x][interseccion.y].add(segmentoInterseccion)
                else:
                    if interseccion.y not in intersecciones[interseccion.x]:
                        intersecciones[interseccion.x][interseccion.y] = set()
                        intersecciones[interseccion.x][interseccion.y].add(segmento)
                        intersecciones[interseccion.x][interseccion.y].add(segmentoInterseccion)
                    else:
                        intersecciones[interseccion.x][interseccion.y].add(segmento)
                        intersecciones[interseccion.x][interseccion.y].add(segmentoInterseccion)
        else:
            pass
            #print("??????? ",segmentos[segmento].nombre, segmentos[segmento].p1,segmentos[segmento].p2,segmentos[segmento].final)
for interseccionX in intersecciones:
    for interseccionY in intersecciones[interseccionX]:
        pygame.draw.circle(screen, (255,0,0), (interseccionX*mult,abs(interseccionY*mult-height)), 3)
        pygame.display.update()
        #print(f"({interseccionX},{interseccionY}), {intersecciones[interseccionX][interseccionY]}")
#################

##########################
interseccionesSegmentos = {}
for interseccionX in intersecciones:
    for interseccionY in intersecciones[interseccionX]:
        v = Vertice(interseccionX,interseccionY,None)
        for segmento in intersecciones[interseccionX][interseccionY]:
            if segmento in interseccionesSegmentos:
                if v == segmentos[segmento].p1 or v == segmentos[segmento].p2:
                    if len(interseccionesSegmentos[segmento]["extremos"])>0:
                        interseccionesSegmentos[segmento]["extremos"].append(v)
                    else:
                        interseccionesSegmentos[segmento]["extremos"] = [v]
                else:
                    if len(interseccionesSegmentos[segmento]["medios"])>0:
                        interseccionesSegmentos[segmento]["medios"].append(v)
                    else:
                        interseccionesSegmentos[segmento]["medios"] = [v]
            else:
                interseccionesSegmentos[segmento] = {}
                interseccionesSegmentos[segmento]["extremos"] = {}
                interseccionesSegmentos[segmento]["medios"] = {}
                if v == segmentos[segmento].p1 or v == segmentos[segmento].p2:
                    interseccionesSegmentos[segmento]["extremos"] = [v]
                else:
                    interseccionesSegmentos[segmento]["medios"] = [v]
suma = 0
for segmento in interseccionesSegmentos:
    interseccionesSegmentos[segmento]["medios"] =  sorted(interseccionesSegmentos[segmento]["medios"], key = lambda interseccion:(-interseccion.y,interseccion.x))
    interseccionesSegmentos[segmento]["extremos"] =  sorted(interseccionesSegmentos[segmento]["extremos"], key = lambda interseccion:(-interseccion.y,interseccion.x))
    #print(segmentos[segmento] , interseccionesSegmentos[segmento])
    suma += len(interseccionesSegmentos[segmento]["medios"])+1
##########################
####################################
nuevosSegmentos = {}
segmentosRevisados = {}
for segmento in interseccionesSegmentos:
    if 1:
        pInicial = segmentos[segmento].p1
        for inter in interseccionesSegmentos[segmento]["medios"]:
            pFinal = inter
            if Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal) not in segmentosRevisados or segmentosRevisados[Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal)]<2:
                nuevosSegmentos[len(nuevosSegmentos)+1] = Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal)
            if Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal) not in segmentosRevisados:
                segmentosRevisados[Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal)] = 1
            else:
                segmentosRevisados[Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal)]+= 1
            pInicial = inter
        if pInicial == segmentos[segmento].p1 or pInicial == interseccionesSegmentos[segmento]["medios"][len(interseccionesSegmentos[segmento]["medios"])-1]:
            pFinal = segmentos[segmento].p2
            #print("(",pInicial,")","(",pFinal,")",interseccionesSegmentos[segmento])
            if Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal) not in segmentosRevisados or segmentosRevisados[Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal)]<2:
                nuevosSegmentos[len(nuevosSegmentos)+1] = Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal)
            if Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal) not in segmentosRevisados:
                segmentosRevisados[Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal)] = 1
            else:
                segmentosRevisados[Segmento(str(len(nuevosSegmentos)+1),pInicial,pFinal)]+= 1
    else:
        pass
####################################
def generar_color_aleatorio():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b
SCREEN_COLOR = (240,240,240) 
screen.fill(SCREEN_COLOR)
pygame.display.update()
for segmento in nuevosSegmentos:
    color = ("blue")
    pygame.draw.line(screen, color, (nuevosSegmentos[segmento].p1.x*mult,abs(nuevosSegmentos[segmento].p1.y*mult-height)), (nuevosSegmentos[segmento].p2.x*mult,abs(nuevosSegmentos[segmento].p2.y*mult-height)), 1)
pygame.display.update()

eventos = []
for segmento in nuevosSegmentos:
    eventos.append(Evento(nuevosSegmentos[segmento].p1, segmento, "superior"))
    eventos.append(Evento(nuevosSegmentos[segmento].p2, segmento, "inferior"))

eventos = sorted(eventos, key=lambda evento: (-evento.punto.y, evento.punto.x, -ord(evento.tipo[0])))

activas = set()

for evento in eventos:
    if evento.tipo == "inferior":
        activas.remove(evento.numSegmento)
    for numSegmento in activas:
        segmento = nuevosSegmentos[numSegmento]
        intX = segmento.getX(evento.punto.y)
        if intX is None:
            intX = evento.punto.x
        if intX < evento.punto.x:
            if evento.tipo == "superior":
                nuevosSegmentos[evento.numSegmento].inicio[numSegmento] = -1
                nuevosSegmentos[numSegmento].inicio[evento.numSegmento] = 1
            else:
                if numSegmento in nuevosSegmentos[evento.numSegmento].inicio:
                    if nuevosSegmentos[evento.numSegmento].inicio[numSegmento] != -1:
                        nuevosSegmentos[evento.numSegmento].final[numSegmento] = -1
                    else:
                        pass
                        # nuevosSegmentos[evento.numSegmento].inicio.pop(numSegmento)
                elif evento.numSegmento in nuevosSegmentos[numSegmento].inicio:
                    if nuevosSegmentos[numSegmento].inicio[evento.numSegmento] != 1:
                        nuevosSegmentos[numSegmento].final[evento.numSegmento] = 1
                    else:
                        pass
                        # nuevosSegmentos[numSegmento].final.pop(evento.numSegmento)
        elif intX > evento.punto.x:
            if evento.tipo == "superior":
                nuevosSegmentos[evento.numSegmento].inicio[numSegmento] = 1
                nuevosSegmentos[numSegmento].inicio[evento.numSegmento] = -1
            else:
                if numSegmento in nuevosSegmentos[evento.numSegmento].inicio:
                    if nuevosSegmentos[evento.numSegmento].inicio[numSegmento] != 1:
                        nuevosSegmentos[evento.numSegmento].final[numSegmento] = 1
                    else:
                        pass
                        # nuevosSegmentos[evento.numSegmento].inicio.pop(numSegmento)
                elif evento.numSegmento in nuevosSegmentos[numSegmento].inicio:
                    if nuevosSegmentos[numSegmento].inicio[evento.numSegmento] != -1:
                        nuevosSegmentos[numSegmento].final[evento.numSegmento] = -1
                    else:
                        pass
                        # nuevosSegmentos[numSegmento].final.pop(evento.numSegmento)
        elif intX == evento.punto.x:
            if evento.tipo == "superior":
                nuevosSegmentos[evento.numSegmento].inicio[numSegmento] = 0
                nuevosSegmentos[numSegmento].inicio[evento.numSegmento] = 0
            else:
                if numSegmento in nuevosSegmentos[evento.numSegmento].inicio:
                    nuevosSegmentos[evento.numSegmento].final[numSegmento] = 0
                elif evento.numSegmento in nuevosSegmentos[numSegmento].inicio:
                    nuevosSegmentos[numSegmento].final[evento.numSegmento] = 0
    if evento.tipo == "superior":
        activas.add(evento.numSegmento)

intersecciones = {}

for segmento in nuevosSegmentos:
    for segmentoInterseccion in nuevosSegmentos[segmento].final:
        it = interseccionSegmentos(
            copy(nuevosSegmentos[segmento].p1),
            copy(nuevosSegmentos[segmento].p2),
            copy(nuevosSegmentos[segmentoInterseccion].p1),
            copy(nuevosSegmentos[segmentoInterseccion].p2)
        )
        if len(it) > 0:
            #interseccion = it[0]
            for interseccion in it:
                if interseccion.x not in intersecciones:
                    intersecciones[interseccion.x] = {}
                    intersecciones[interseccion.x][interseccion.y] = set()
                    intersecciones[interseccion.x][interseccion.y].add(segmento)
                    intersecciones[interseccion.x][interseccion.y].add(segmentoInterseccion)
                else:
                    if interseccion.y not in intersecciones[interseccion.x]:
                        intersecciones[interseccion.x][interseccion.y] = set()
                        intersecciones[interseccion.x][interseccion.y].add(segmento)
                        intersecciones[interseccion.x][interseccion.y].add(segmentoInterseccion)
                    else:
                        intersecciones[interseccion.x][interseccion.y].add(segmento)
                        intersecciones[interseccion.x][interseccion.y].add(segmentoInterseccion)

for interseccionX in intersecciones:
    for interseccionY in intersecciones[interseccionX]:
        pygame.draw.circle(screen, (255, 0, 0), (interseccionX * mult, abs(interseccionY * mult - height)), 3)
        pygame.display.update()
        #print(f"({interseccionX},{interseccionY}), {intersecciones[interseccionX][interseccionY]}")

interseccionesSegmentos = {}

for interseccionX in intersecciones:
    for interseccionY in intersecciones[interseccionX]:
        v = Vertice(interseccionX, interseccionY, None)
        for segmento in intersecciones[interseccionX][interseccionY]:
            if segmento in interseccionesSegmentos:
                if v == nuevosSegmentos[segmento].p1 or v == nuevosSegmentos[segmento].p2:
                    if len(interseccionesSegmentos[segmento]["extremos"]) > 0:
                        interseccionesSegmentos[segmento]["extremos"].append(v)
                    else:
                        interseccionesSegmentos[segmento]["extremos"] = [v]
                else:
                    if len(interseccionesSegmentos[segmento]["medios"]) > 0:
                        interseccionesSegmentos[segmento]["medios"].append(v)
                    else:
                        interseccionesSegmentos[segmento]["medios"] = [v]
            else:
                interseccionesSegmentos[segmento] = {}
                interseccionesSegmentos[segmento]["extremos"] = {}
                interseccionesSegmentos[segmento]["medios"] = {}
                if v == nuevosSegmentos[segmento].p1 or v == nuevosSegmentos[segmento].p2:
                    interseccionesSegmentos[segmento]["extremos"] = [v]
                else:
                    interseccionesSegmentos[segmento]["medios"] = [v]

nuevosSegmentosOrdenados = sorted(nuevosSegmentos, key=lambda segmento: (nuevosSegmentos[segmento].p1.x,nuevosSegmentos[segmento].p1.y, nuevosSegmentos[segmento].p2.x,nuevosSegmentos[segmento].p2.y))

cont = 1
for segmento in nuevosSegmentosOrdenados:
    nuevosSegmentos[segmento].nombre = str(cont)
    if int(cont)%2==0:
        temp = nuevosSegmentos[segmento].p1
        nuevosSegmentos[segmento].p1 = nuevosSegmentos[segmento].p2
        nuevosSegmentos[segmento].p2 = temp
    #print(nuevosSegmentos[segmento])
    cont+=1

segmentosConexiones = {}
segmentosConexiones2 = {}
for segmento in nuevosSegmentosOrdenados:
    if int(nuevosSegmentos[segmento].nombre)%2!=0:
        pFinal = nuevosSegmentos[segmento].p2
        for segmento2 in nuevosSegmentos:
            if nuevosSegmentos[segmento2] != nuevosSegmentos[segmento]:
                if nuevosSegmentos[segmento2].p1 == pFinal:
                    if nuevosSegmentos[segmento] not in segmentosConexiones:
                        if int(nuevosSegmentos[segmento2].nombre)-1!=int(nuevosSegmentos[segmento].nombre):
                            segmentosConexiones[nuevosSegmentos[segmento]] = [nuevosSegmentos[segmento2]]
                    else:
                        if nuevosSegmentos[segmento2] not in segmentosConexiones[nuevosSegmentos[segmento]]:
                            if int(nuevosSegmentos[segmento2].nombre)-1!=int(nuevosSegmentos[segmento].nombre):
                                segmentosConexiones[nuevosSegmentos[segmento]].append(nuevosSegmentos[segmento2])
    else:
        pFinal = nuevosSegmentos[segmento].p2
        for segmento2 in nuevosSegmentos:
            if nuevosSegmentos[segmento2] != nuevosSegmentos[segmento]:
                if nuevosSegmentos[segmento2].p1 == pFinal:
                    if nuevosSegmentos[segmento] not in segmentosConexiones2:
                        if int(nuevosSegmentos[segmento2].nombre)+1!=int(nuevosSegmentos[segmento].nombre):
                            segmentosConexiones2[nuevosSegmentos[segmento]] = [nuevosSegmentos[segmento2]]
                    else:
                        if nuevosSegmentos[segmento2] not in segmentosConexiones2[nuevosSegmentos[segmento]]:
                            if int(nuevosSegmentos[segmento2].nombre)+1!=int(nuevosSegmentos[segmento].nombre):
                                segmentosConexiones2[nuevosSegmentos[segmento]].append(nuevosSegmentos[segmento2])
#print("-----------------------------------------------------------------------------")
#print("-----------------------------------------------------------------------------")
####################################
todosSegmentosConexiones = copy(segmentosConexiones)
todosSegmentosConexiones.update(segmentosConexiones2)
#print("----------------------------------------------")
#####################################
def calculate_angle(segment1, segment2):
    #print(segment1,segment2)
    x1 = segment1.p1.x
    y1 = segment1.p1.y
    x2 = segment1.p2.x
    y2 = segment1.p2.y
    x3 = segment2.p2.x
    y3 = segment2.p2.y
    # Calculate vectors
    ux = x1 - x2
    uy = y1 - y2
    vx = x3 - x2
    vy = y3 - y2
    #print(ux,uy,vx,vy)
    m1 = math.sqrt(ux*ux+uy*uy)
    m2 = math.sqrt(vx*vx+vy*vy)

    # Calculate dot product
    dot_product = (ux * vx + uy * vy) / (m1*m2)
    # Calculate cross product
    cross_product = (ux * vy - uy * vx) / (m1*m2)

    # Calculate the angle in radians
    angle_rad = math.atan2(cross_product, dot_product)

    # Convert angle to degrees
    angle_deg = math.degrees(angle_rad)

    # Adjust the angle to be in the range of [0, 360)
    if angle_deg < 0:
        angle_deg += 360
        
        
    return angle_deg
#####################################
for s in nuevosSegmentos:
    pass
    #print(s, nuevosSegmentos[s])
#print("----------------------------------------")
for s in todosSegmentosConexiones:
    pass
    #print(s, todosSegmentosConexiones[s])
def maxAngleCycle(segmento, segmentsSet, initSegment, conexionesDict):
    if len(segmentsSet) > 2 and segmento == initSegment:
        return segmentsSet
    else:
        if segmento in conexionesDict:
            if segmento.p2 == initSegment.p1:
                return segmentsSet
            angles = []
            angleSegment = []
            for conexion in conexionesDict[segmento]:
                if 1:
                #if Segmento(None,conexion.p2,conexion.p1)!=initSegment:
                    
                    #angle = calculate_angle(segmento, conexion)
                    angle = calculate_angle(segmento, conexion)
                    angles.append(angle)
                    angleSegment.append(conexion)
            maxAngleIndex = angles.index(min(angles))
            nextSegment = angleSegment[maxAngleIndex]
            segmentsSet.append(nextSegment)
            return maxAngleCycle(nextSegment, segmentsSet, initSegment, conexionesDict)
        else:
            nuevoSegmentIndex = -1
            if int(segmento.nombre)%2==0:
                nuevoSegmentIndex = str(int(segmento.nombre)-1)
            else:
                nuevoSegmentIndex = str(int(segmento.nombre)+1)
            sName = -1
            for s in nuevosSegmentos:
                if nuevoSegmentIndex == nuevosSegmentos[s].nombre:
                    sName = s
                    break
            backSegment = nuevosSegmentos[sName]
            #print("???",segmento, backSegment)
            segmentsSet.append(backSegment)
            return []
            return maxAngleCycle(backSegment, segmentsSet, initSegment, conexionesDict)

def isSegmentOrPair(completeSet, set1):
    set2 = set()
    for num in set1:
        if int(num)%2==0:
            set2.add(str(int(num)-1))
        else:
            set2.add(str(int(num)+1))
    if set1 in completeSet or set2 in completeSet:
        return False
    return True

max_segments_checked = []
min_segments_checked = set()
polygon = []
poligonos = []
poligonosNamesList = []
poligonosSet = set()
for segmento in todosSegmentosConexiones:
    polygon = []
    max_segments_checked = []
    poligonosSet = set()
    polygon.append(segmento)
    cycle = maxAngleCycle(segmento, max_segments_checked,segmento,todosSegmentosConexiones)
    if cycle is not None:
        polygon += cycle
    else:
        pass
        #print("none")
    if len(polygon)>2:
        for p in polygon:
            poligonosSet.add(p.nombre)
        if isSegmentOrPair(poligonosNamesList, poligonosSet):
            poligonosNamesList.append(poligonosSet)
            poligonos.append(polygon)
        else:
            pass
for poligono in poligonosNamesList: 
    poligono2 = sorted_poligono = sorted(poligono, key=lambda x: int(x))
    #print(poligonosNamesList.index(poligono), poligono)
for segmento in poligonos[0]:
    #pygame.draw.line(screen, (0, 255, 0), (segmento.p1.x * mult, abs(segmento.p1.y * mult - height)), (segmento.p2.x * mult, abs(segmento.p2.y * mult - height)), 1)
    pass
    #pygame.display.update()
#print(len(poligonos))
#print(poligonos)
###################################
class Polygon:
    def __init__(self, vertices, color, pygamePoly):
        self.vertices = vertices
        self.color = color
        self.pygamePoly = pygamePoly

    def draw(self, screen):
        self.pygamePoly = pygame.draw.polygon(screen, self.color, self.vertices)

    def point_in_polygon(self, point):
        # Initialize the collision count
        collision_count = 0
    
        # Iterate over each edge of the polygon
        for i in range(len(self.vertices)):
            # Get the current and next vertex
            current_vertex = self.vertices[i]
            next_vertex = self.vertices[(i + 1) % len(self.vertices)]
    
            # Unpack the coordinates of the vertices
            x1, y1 = current_vertex
            x2, y2 = next_vertex
    
            # Check if the point is within the y-bounds of the edge
            if (y1 < point[1] <= y2) or (y1 >= point[1] > y2):
                # Calculate the x-coordinate of the edge at the y-coordinate of the point
                x = x1 + (point[1] - y1) * (x2 - x1) / (y2 - y1)
    
                # Check if the point is to the left of the edge
                if point[0] < x:
                    # Increment the collision count
                    collision_count += 1
    
        # If the collision count is odd, the point is inside the polygon
        return collision_count % 2 == 1

####################################
poligonosDict = {}
minPol = 1
maxPol = len(poligonos)
if maxPol == 1:
    minPol = 0
for n in range(minPol, maxPol):
    a = []
    for p in poligonos[n]:
        a.append((p.p1.x*mult,abs(p.p1.y*mult-height)))
    b = pygame.draw.polygon(screen,SCREEN_COLOR,a)
    pygame.display.update()
    poligonosDict[n] = Polygon(a,SCREEN_COLOR,b)
for segmento in nuevosSegmentos:
    color = ("blue")
    pygame.draw.line(screen, color, (nuevosSegmentos[segmento].p1.x*mult,abs(nuevosSegmentos[segmento].p1.y*mult-height)), (nuevosSegmentos[segmento].p2.x*mult,abs(nuevosSegmentos[segmento].p2.y*mult-height)), 1)
pygame.display.update()
for interseccionX in intersecciones:
    for interseccionY in intersecciones[interseccionX]:
        pygame.draw.circle(screen, (255, 0, 0), (interseccionX * mult, abs(interseccionY * mult - height)), 3)
        pygame.display.update()
####################################
COLORES = []
for i in range(10):
    COLORES.append(generar_color_aleatorio())
COLOR_ACTIVO = COLORES[0]
# Create a list of rectangles and their colors
rectangles = []
####################################
polygon_index = 0  # Index of the current polygon
while running:
    # Define the yellow rectangle at the top
    yellow_rect = pygame.Rect(0, 0, width, additional_height)
    # Draw the yellow rectangle on the screen
    pygame.draw.rect(screen, "yellow", yellow_rect)   
    # Calculate the height and spacing of the blue rectangles
    rectHeight = yellow_rect.height - additional_height/4  # Adjust the height as needed
    spacing = width / 12 / 10
    # Calculate the width and height of each blue rectangle
    rectWidth = width / 12
    # Draw the blue rectangles with spacing
    for i in range(10):
        rectX = yellow_rect.x + (spacing * (i + 1)) + (rectWidth * i)
        rectY = yellow_rect.y + yellow_rect.height / 4
        rect = pygame.Rect(rectX, rectY, rectWidth, 2 * rectHeight / 3)
        if COLOR_ACTIVO == COLORES[i]:
            pygame.draw.rect(screen, COLORES[i], rect,mult//4)
        else:
            pygame.draw.rect(screen, COLORES[i], rect)
        rectangles.append((rect, COLORES[i]))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for p in poligonosDict:
                if poligonosDict[p].point_in_polygon(mouse_pos):
                    # Change the color of the selected polygon
                    poligonosDict[p].color = COLOR_ACTIVO
                    poligonosDict[p].draw(screen)
                    pygame.display.update()
            for rect, color in rectangles:
                    if rect.collidepoint(mouse_pos):
                        COLOR_ACTIVO = color
    """
    # Draw the current polygon
    current_polygon = poligonos[polygon_index]
    for segmento in current_polygon:
        pygame.draw.line(screen, (255, 255, 255), (segmento.p1.x * mult, abs(segmento.p1.y * mult - height)), (segmento.p2.x * mult, abs(segmento.p2.y * mult - height)), 4)
    
    # Update the display
    pygame.display.update()
    print(polygon_index)
    # Wait for 5 seconds
    pygame.time.delay(3000)
    
    for segmento in current_polygon:
        pygame.draw.line(screen, (0, 0, 255), (segmento.p1.x * mult, abs(segmento.p1.y * mult - height)), (segmento.p2.x * mult, abs(segmento.p2.y * mult - height)), 1)
    
    # Increment the polygon index for the next iteration
    polygon_index = (polygon_index + 1) % len(poligonos)
    """
    for segmento in nuevosSegmentos:
        color = ("blue")
        pygame.draw.line(screen, color, (nuevosSegmentos[segmento].p1.x*mult,abs(nuevosSegmentos[segmento].p1.y*mult-height)), (nuevosSegmentos[segmento].p2.x*mult,abs(nuevosSegmentos[segmento].p2.y*mult-height)), 1)
    pygame.display.update()
    for interseccionX in intersecciones:
        for interseccionY in intersecciones[interseccionX]:
            pygame.draw.circle(screen, (255, 0, 0), (interseccionX * mult, abs(interseccionY * mult - height)), 3)
            pygame.display.update()
            
pygame.quit()