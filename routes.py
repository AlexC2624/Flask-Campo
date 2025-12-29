from flask import render_template, request, jsonify, send_from_directory, make_response, send_file
import pandas as pd
from io import BytesIO

def configurar_rotas(app, db):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/coleta')
    def coleta():
        return render_template('coleta.html')

    @app.route('/ver_dados')
    def ver_dados():
        registros = db.ler()
        corpo = """
        <style>
            body { font-family: sans-serif; padding: 20px; background: #f4f7f6; }
            table { width: 100%; border-collapse: collapse; background: white; margin-top: 10px; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background: #2e7d32; color: white; }
            .btn-voltar { display: inline-block; margin-top: 20px; padding: 10px 20px; 
                        background: #2e7d32; color: white; text-decoration: none; border-radius: 5px; }
        </style>
        <h2>Dados Coletados no Campo</h2>
        <table>
            <tr><th>ID</th><th>Dispositivo</th><th>Talhão</th><th>Atividade</th><th>Qtd</th><th>Data</th></tr>
        """
        for r in registros:
            corpo += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>"
        
        corpo += "</table><br><a href='/menu' class='btn-voltar'>⬅️ Voltar para o Menu</a>"
        
        # Criamos uma resposta formal
        response = make_response(corpo)
        # Cache-Control ajuda o Service Worker a saber que pode guardar essa página
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    
    @app.route('/relatorios')
    def relatorios():
        # Renderiza a página simples de exportação
        return render_template('relatorios.html')

    @app.route('/exportar_excel')
    def exportar_excel():
        # 1. Busca os dados no banco
        registros = db.ler()
        
        # 2. Converte para um DataFrame do Pandas
        df = pd.DataFrame(registros, columns=['ID', 'Dispositivo', 'Talhão', 'Atividade', 'Quantidade', 'Data', 'Observações'])
        
        # 3. Cria o arquivo Excel na memória (sem precisar salvar no HD do PC)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Coletas')
        
        output.seek(0)
        
        # 4. Envia o arquivo para o navegador/celular iniciar o download
        return send_file(output, 
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         as_attachment=True, 
                         download_name='Relatorio_Agro_Cargnin.xlsx')

    @app.route('/salvar', methods=['POST'])
    def salvar():
        if db.inserir(request.json):
            return jsonify({"status": "sucesso"}), 200
        return jsonify({"status": "erro"}), 500

    @app.route('/sw.js')
    def serve_sw():
        return send_from_directory('static', 'sw.js')

    @app.route('/manifest.json')
    def serve_manifest():
        return send_from_directory('static', 'manifest.json')