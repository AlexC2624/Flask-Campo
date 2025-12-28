import sys
from flask import Flask
from routes import configurar_rotas
from manage import Manage

app = Flask(__name__)
db = Manage()
configurar_rotas(app, db)

if __name__ == '__main__':
    PORTA = 5000
    USAR_TUNEL_NGROK = True
    USAR_TUNEL_CLOUDFLARE = False

    # Instancia a classe do tunel
    if USAR_TUNEL_NGROK:
        from tunnel import NgrokTunnel
        tunel = NgrokTunnel(porta=PORTA, auth_token=open('ngrok_token.txt').read().strip())
        tunel.iniciar()

    elif USAR_TUNEL_CLOUDFLARE:
        from tunnel import CloudflareTunnel
        tunel = CloudflareTunnel(porta=PORTA)
        tunel.iniciar()
    
    try:
        app.run(host='0.0.0.0', port=PORTA, debug=False)
    except KeyboardInterrupt:
        print("\nSaindo do programa...")
    finally:
        if USAR_TUNEL_NGROK:
            tunel.finalizar()
        elif USAR_TUNEL_CLOUDFLARE:
            tunel.finalizar()
            sys.exit(0)