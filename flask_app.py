import math
import random
from flask import Flask, render_template, request
from operator import itemgetter

app = Flask(__name__)

coord = {
    'Jilotepec': (19.984146, -99.519127),
    'Toluca': (19.286167856525594, -99.65473296644892),
    'Atlacomulco': (19.796802401380955, -99.87643301629244),
    'Guadalajara': (20.655773344775373, -103.35773871581326),
    'Monterrey': (25.675859554333684, -100.31405053526082),
    'Cancún': (21.158135651777727, -86.85092947858692),
    'Morelia': (19.720961251258654, -101.15929186858635),
    'Aguascalientes': (21.88473831747085, -102.29198705069501),
    'Queretaro': (20.57005870003398, -100.45222862892079),
    'CDMX': (19.429550164848152, -99.13000959477478)
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[-1]
    ciudad2 = ruta[0]
    total += distancia(coord[ciudad1], coord[ciudad2])
    return total

def i_hill_climbing(coord):
    mejor_ruta = list(coord.keys())  # Ruta inicial
    random.shuffle(mejor_ruta)
    mejor_distancia = evalua_ruta(mejor_ruta, coord)
    max_iteraciones = 1000  # Número máximo de iteraciones

    while max_iteraciones > 0:
        max_iteraciones -= 1
        ruta_actual = mejor_ruta[:]
        i, j = random.sample(range(len(ruta_actual)), 2)
        ruta_actual[i], ruta_actual[j] = ruta_actual[j], ruta_actual[i]
        distancia_actual = evalua_ruta(ruta_actual, coord)

        if distancia_actual < mejor_distancia:
            mejor_ruta = ruta_actual[:]
            mejor_distancia = distancia_actual

    return mejor_ruta

@app.route("/")
def pagina():
    ruta = i_hill_climbing(coord)
    res = str(evalua_ruta(ruta, coord))
    return render_template("index.html", ruta=ruta, distancia=res)

@app.route("/resultado")
def resultado():
    ruta = i_hill_climbing(coord)
    res = str(evalua_ruta(ruta, coord))
    return render_template("resultado.html", mejor_ruta=ruta, resultado=res)

if __name__ == '__main__':
    app.run()
