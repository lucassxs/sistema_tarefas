from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# carregando tarefas
def carregar_tarefas():
    try:
        with open('tarefas.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Salvar tarefas no arquivo JSON
def salvar_tarefas(tarefas):
    with open('tarefas.json', 'w') as f:
        json.dump(tarefas, f, indent=2)

# Rota para exibir a lista de tarefas
@app.route('/')
def listar_tarefas():
    tarefas = carregar_tarefas()
    return render_template('lista_tarefas.html', tarefas=tarefas)

# Rota para adicionar uma nova tarefa
@app.route('/adicionar', methods=['POST'])
def adicionar_tarefa():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    status = request.form['status']

    tarefas = carregar_tarefas()
    nova_tarefa = {'titulo': titulo, 'descricao': descricao, 'status': status}
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)

    return redirect(url_for('listar_tarefas'))

# Rota para editar uma tarefa existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarefa(id):
    tarefas = carregar_tarefas()
    tarefa = tarefas[id - 1]

    if request.method == 'POST':
        tarefa['titulo'] = request.form['titulo']
        tarefa['descricao'] = request.form['descricao']
        tarefa['status'] = request.form['status']
        salvar_tarefas(tarefas)
        return redirect(url_for('listar_tarefas'))

    return render_template('editar_tarefa.html', tarefa=tarefa)

# Rota para excluir uma tarefa
@app.route('/excluir/<int:id>')
def excluir_tarefa(id):
    tarefas = carregar_tarefas()
    tarefas.pop(id - 1)
    salvar_tarefas(tarefas)
    return redirect(url_for('listar_tarefas'))

if __name__ == '__main__':
    app.run(debug=True)