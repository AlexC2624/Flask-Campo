from flask import Flask, render_template, request, jsonify, send_from_directory

def configurar_rotas(app, db):
    @app.route('/')
    def index():
        # Verifique se o nome do arquivo é login.html ou loguin.html
        return render_template('login.html')
    
    @app.route('/menu')
    def menu():
        return render_template('menu.html')

    @app.route('/relatorios')
    def relatorios():
        # Aqui futuramente você criará a lógica de exportação para Excel
        return "<h2>Página de Relatórios em construção...</h2><br><a href='/menu'>Voltar</a>"

    @app.route('/coleta')
    def coleta():
        return render_template('coleta.html')

    @app.route('/auth', methods=['POST'])
    def auth():
        dados = request.json
        usuario = dados.get('usuario')
        senha = dados.get('senha')
        
        # Validação simples
        if usuario == "admin" and senha == "123":
            print(f"✅ Acesso liberado para: {usuario}")
            return jsonify({"status": "sucesso"}), 200
        else:
            print(f"❌ Tentativa de login inválida: {usuario}")
            return jsonify({"status": "erro"}), 401

    @app.route('/sw.js')
    def serve_sw():
        return send_from_directory('static', 'sw.js')

    @app.route('/manifest.json')
    def serve_manifest():
        return send_from_directory('static', 'manifest.json')

    @app.route('/salvar', methods=['POST'])
    def salvar():
        dados = request.json
        if db.inserir(dados):
            return jsonify({"status": "sucesso"}), 200
        return jsonify({"status": "erro"}), 500

    @app.route('/ver_dados')
    def ver_dados():
        registros = db.ler()
        corpo = "<h2>Dados Coletados</h2><table border='1'><tr><th>ID</th><th>Talhão</th><th>Atividade</th><th>Qtd</th><th>Data</th></tr>"
        for r in registros:
            corpo += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
        corpo += "</table><br><a href='/coleta'>Voltar</a>"
        return corpo