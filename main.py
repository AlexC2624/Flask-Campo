import sys
from flask import Flask
from tunnel import iniciar_ngrok, finalizar_ngrok
from routes import configurar_rotas
from manage import Manage

# Inicialização
app = Flask(__name__)
db = Manage()

# Aplicar as rotas ao app
configurar_rotas(app, db)

if __name__ == '__main__':
    PORTA = 5000
    TUNEL_ATIVO = True  # Defina como True para ativar o túnel Ngrok
    
    # Tenta iniciar o túnel Ngrok se ativado
    if TUNEL_ATIVO:
        url_publica = iniciar_ngrok(PORTA)
    
    try:
        # Executa o servidor Flask
        # host='0.0.0.0' é fundamental para acesso na rede local
        app.run(host='0.0.0.0', port=PORTA, debug=False)
    except KeyboardInterrupt:
        print("\nSaindo do programa...")
    finally:
        if TUNEL_ATIVO: finalizar_ngrok()
        sys.exit(0)