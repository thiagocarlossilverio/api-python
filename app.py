import mysql.connector

from flask import Flask, make_response, jsonify, request


app = Flask(__name__)

banco = mysql.connector.connect(
        host="sistema_api.mysql.dbaas.com.br",
        user="sistema_api",
        password="Api@2024!",
        database="sistema_api"
)

@app.route('/usuarios', methods=['GET'])
def obterUsuarios():
    conexao = banco.cursor()
    conexao.execute('SELECT * FROM usuarios')
    resultado = conexao.fetchall()

    usuarios = list()
    for usuario in resultado:
        usuarios.append(
            {
                'id': usuario[0],
                'nome': usuario[1],
                'email': usuario[2],
                'login': usuario[3],
                'senha': usuario[4],
                'ativo': usuario[5]
            }
        )


    return make_response(
        jsonify(usuarios)
    )


@app.route('/usuarios/<int:id>', methods=['GET'])
def obterUsuarioPorId(id):
      conexao = banco.cursor()
      sql = f"SELECT * FROM usuarios where id = {id}"
      conexao.execute(sql)
      usuario = conexao.fetchone()

      return make_response(
      jsonify({
                'id': usuario[0],
                'nome': usuario[1],
                'email': usuario[2],
                'login': usuario[3],
                'senha': usuario[4],
                'ativo': usuario[5]
            })
      )


@app.route('/usuarios/<int:id>', methods=['PUT'])
def editarUsuarioPorId(id):
   dadosUsuario = request.get_json()

   conexao = banco.cursor()
   sql = f"UPDATE usuarios SET nome='{dadosUsuario['nome']}', email='{dadosUsuario['email']}', login='{dadosUsuario['login']}', senha='{dadosUsuario['senha']}' WHERE id = {id}"
    
   conexao.execute(sql)
   banco.commit()


   return make_response(
       jsonify(dadosUsuario)
   )

@app.route('/usuarios/', methods=['POST'])
def incluirUsuario():
    dadosUsuario = request.get_json()

    conexao = banco.cursor()
    sql = f"INSERT INTO usuarios (nome, email, login, senha) VALUES('{dadosUsuario['nome']}', '{dadosUsuario['email']}', '{dadosUsuario['login']}', '{dadosUsuario['senha']}')"
    conexao.execute(sql)
    banco.commit()


    return make_response(
        jsonify(dadosUsuario)
    )


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def excluirUsuario(id):
     conexao = banco.cursor()
     sql = f"DELETE FROM usuarios where id = {id}"
     conexao.execute(sql)
     banco.commit()

     return make_response(
     jsonify(mensagem='usuario excluido com sucesso')           
     )


app.run(port=5000, host='localhost', debug=True)