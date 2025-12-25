from pyngrok import ngrok

def iniciar_ngrok(porta):
    try:
        # Lê o token de um arquivo externo
        with open("MEU_TOKEN.txt", "r") as f:
            token = f.read().strip()
        
        ngrok.set_auth_token(token)
        tudnel = ngrok.connect(porta)
        
        print("\n" + "="*85)
        print(f"🚀 PROJETO ONLINE (HTTPS)")
        print(f"🔗 URL PARA O CELULAR: {tudnel.public_url}")
        print("="*85 + "\n")
        return tudnel.public_url
    except Exception as e:
        print(f"❌ Erro ao iniciar Ngrok: {e}")
        return None

def finalizar_ngrok():
    print("\n🛑 Encerrando conexões Ngrok...")
    ngrok.kill()