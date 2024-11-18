from datetime import datetime

from flask import Flask, render_template, request
from persistencia import cargar_turnos, guardar_turnos

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)


# Página inicial
@app.route("/")
def index():
    return render_template("index.html")


# Mostrar turnos
@app.route("/<area>")
def mostrar_turnos(area):
    turnos = cargar_turnos()
    return render_template("tabla.html", area=area, turnos=turnos.get(area, []))


# Mostrar formulario para agregar o modificar
@app.route("/<area>/formulario", methods=["GET"])
@app.route("/<area>/formulario/<int:id_turno>", methods=["GET"])
def formulario_turno(area, id_turno=None):
    turnos = cargar_turnos()
    turno = turnos[area][id_turno] if id_turno is not None else None
    return render_template("formulario.html", area=area, turno=turno, id=id_turno)


# Crear turno
@app.route("/<area>/nuevo", methods=["POST"])
def crear_turno(area):
    turnos = cargar_turnos()
    nombre = request.form["nombre"]
    fecha_hora = request.form["fecha_hora"]
    turnos[area].append({"nombre": nombre, "fecha_hora": fecha_hora})
    guardar_turnos(turnos)
    return mostrar_turnos(area)


# Modificar turno
@app.route("/<area>/modificar/<int:id_turno>", methods=["PUT"])
def modificar_turno(area, id_turno):
    turnos = cargar_turnos()
    nombre = request.form["nombre"]
    fecha_hora = request.form["fecha_hora"]
    turnos[area][id_turno] = {"nombre": nombre, "fecha_hora": fecha_hora}
    guardar_turnos(turnos)
    return mostrar_turnos(area)


# Eliminar turno
@app.route("/<area>/eliminar/<int:id_turno>", methods=["DELETE"])
def eliminar_turno(area, id_turno):
    turnos = cargar_turnos()
    if id_turno < len(turnos[area]):
        del turnos[area][id_turno]
        guardar_turnos(turnos)
    return mostrar_turnos(area)


def formatear_fecha(fecha_iso: str) -> str:
    try:
        fecha = datetime.fromisoformat(fecha_iso)
        return fecha.strftime("%d/%m/%Y  -  %H:%M")
    except ValueError:
        return fecha_iso


app.jinja_env.filters["formatear_fecha"] = formatear_fecha

if __name__ == "__main__":
    app.run(debug=True)
