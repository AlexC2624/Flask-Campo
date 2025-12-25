from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session

def configurar_rotas(app, db):
    # CHAVE SECRETA: Necessária para o Flask gerenciar o login (session)
    app.secret_key = 'agro_cargnin_secret_key'

    @app.route('/')
    def index():
        # Se já estiver logado, pula o login e vai para o menu
        if session.get('logado'):
            return redirect(url_for('menu'))
        return render_template('login.html')

    @app.route('/auth', methods=['POST'])
    def auth():
        dados = request.json
        usuario = dados.get('usuario')
        senha = dados.get('senha')
        
        if usuario == "admin" and senha == "123":
            session['logado'] = True  # Marca como logado
            return jsonify({"status": "sucesso"}), 200
        return jsonify({"status": "erro"}), 401

    @app.route('/logout')
    def logout():
        session.pop('logado', None) # Remove a marca de logado
        return redirect(url_for('index'))

    @app.route('/menu')
    def menu():
        if not session.get('logado'):
            return redirect(url_for('index'))
        return render_template('menu.html')

    @app.route('/coleta')
    def coleta():
        if not session.get('logado'):
            return redirect(url_for('index'))
        return render_template('coleta.html')

    @app.route('/ver_dados')
    def ver_dados():
        if not session.get('logado'):
            return redirect(url_for('index'))
        
        registros = db.ler()
        # CORREÇÃO AQUI: O link agora aponta para /menu
        corpo = """
        <style>
            body { font-family: sans-serif; padding: 20px; background: #f4f7f6; }
            table { width: 100%; border-collapse: collapse; background: white; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background: #2e7d32; color: white; }
            .btn-voltar { display: inline-block; margin-top: 20px; padding: 10px 20px; 
                          background: #2e7d32; color: white; text-decoration: none; border-radius: 5px; }
        </style>
        <h2>Dados Coletados no Campo</h2>
        <table>
            <tr><th>ID</th><th>Talhão</th><th>Atividade</th><th>Qtd</th><th>Data</th></tr>
        """
        for r in registros:
            corpo += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
        
        corpo += "</table><br><a href='/menu' class='btn-voltar'>⬅️ Voltar para o Menu</a>"
        return corpo

    # Rotas de arquivos estáticos permanecem iguais
    @app.route('/sw.js')
    def serve_sw():
        return send_from_directory('static', 'sw.js')

    @app.route('/manifest.json')
    def serve_manifest():
        return send_from_directory('static', 'manifest.json')

    @app.route('/salvar', methods=['POST'])
    def salvar():
        if db.inserir(request.json):
            return jsonify({"status": "sucesso"}), 200
        return jsonify({"status": "erro"}), 500