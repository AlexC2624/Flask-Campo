from pyngrok import ngrok

class NgrokTunnel:
    def __init__(self, porta=5000, auth_token=None):
        """
        :param porta: Porta local onde o Flask está rodando.
        :param auth_token: Seu token do painel do ngrok (necessário para recursos extras).
        """
        self.porta = porta
        self.url_publica = None
        
        if auth_token:
            ngrok.set_auth_token(auth_token)

    def iniciar(self):
        """Abre o túnel ngrok."""
        try:
            # Abre um túnel HTTP na porta especificada
            self.url_publica = ngrok.connect(self.porta).public_url
            print(f"\n✅ NGROK ONLINE: {self.url_publica}")
            print("📱 Acesse este link no celular.\n")
            # Nota: O ngrok grátis mostrará a página de aviso no primeiro acesso.
            return self.url_publica
        except Exception as e:
            print(f"❌ Erro ao iniciar o Ngrok: {e}")
            return None

    def finalizar(self):
        """Fecha todos os túneis ativos."""
        print("\n⏳ Encerrando túnel Ngrok...")
        try:
            ngrok.disconnect(self.url_publica)
            ngrok.kill()
            print("🛑 Ngrok fechado com sucesso.")
        except Exception as e:
            print(f"⚠️ Erro ao fechar o Ngrok: {e}")
##############################################################################################

import subprocess
import threading
import re
import os
import signal
import time

class CloudflareTunnel:
    def __init__(self, porta=5000):
        self.porta = porta
        self.processo = None
        self.url = None

    def iniciar(self):
        """Inicia o túnel em uma thread separada."""
        def run():
            try:
                # Comando para iniciar o túnel Quick de forma gratuita
                self.processo = subprocess.Popen(
                    ['cloudflared', 'tunnel', '--url', f'http://localhost:{self.porta}'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    preexec_fn=os.setsid  # Essencial para fechar o processo pai e filhos no Linux
                )
                
                # Monitora a saída para capturar a URL gerada
                for linha in self.processo.stdout:
                    match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', linha)
                    if match:
                        self.url = match.group(0)
                        print(f"\n✅ SISTEMA ONLINE: {self.url}")
                        print("📱 Abra este link no celular para usar no campo.\n")
                        break
            except FileNotFoundError:
                print("\n❌ Erro: 'cloudflared' não encontrado. Certifique-se de que está instalado.")
            except Exception as e:
                print(f"\n❌ Erro ao iniciar o Cloudflare: {e}")

        self.thread = threading.Thread(target=run)
        self.thread.daemon = True
        self.thread.start()
        
        # Opcional: espera um pouco para garantir que a URL seja capturada antes de seguir
        time.sleep(1)

    def finalizar(self):
        """Encerra o processo do túnel corretamente."""
        if self.processo:
            print("\n⏳ Encerrando túnel Cloudflare...")
            try:
                # Mata o grupo de processos (cloudflared e seus subprocessos)
                os.killpg(os.getpgid(self.processo.pid), signal.SIGTERM)
                self.processo.wait(timeout=5)
                print("🛑 Túnel fechado com sucesso.")
            except Exception as e:
                print(f"⚠️ Erro ao fechar o túnel: {e}")
            finally:
                self.processo = None