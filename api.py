from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

tareas = []

@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/tareas', methods=['GET'])
def get_tareas():
    return jsonify(tareas)


@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def get_tarea(tarea_id):
    tarea = next((t for t in tareas if t['id'] == tarea_id), None)
    if tarea:
        return jsonify(tarea)
    else:
        return jsonify({'message': 'Tarea no encontrada'}), 404

# Ruta para crear una nueva tarea (Crear)
@app.route('/tareas', methods=['POST'])
def create_tarea():
    data = request.json
    nueva_tarea = {
        'id': len(tareas) + 1,
        'titulo': data['titulo'],
        'descripcion': data.get('descripcion', ''),
        'completado': False
    }
    tareas.append(nueva_tarea)
    return jsonify(nueva_tarea), 201

# Ruta para actualizar una tarea (Actualizar)
@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def update_tarea(tarea_id):
    tarea = next((t for t in tareas if t['id'] == tarea_id), None)
    if tarea:
        data = request.json
        tarea['titulo'] = data.get('titulo', tarea['titulo'])
        tarea['descripcion'] = data.get('descripcion', tarea['descripcion'])
        tarea['completado'] = data.get('completado', tarea['completado'])
        return jsonify(tarea)
    else:
        return jsonify({'message': 'Tarea no encontrada'}), 404

# Ruta para eliminar una tarea (Eliminar)
@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def delete_tarea(tarea_id):
    global tareas
    tareas = [t for t in tareas if t['id'] != tarea_id]
    return jsonify({'message': 'Tarea eliminada'}), 200

if __name__ == '__main__':
    app.run(debug=True)
