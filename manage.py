import sqlite3

class Manage:
    def __init__(self, db_name="agro.db"):
        self.db_name = db_name
        self.criar_tabela()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def criar_tabela(self):
        conn = self.conectar()
        # Adicionada a coluna 'dispositivo'
        conn.execute('''CREATE TABLE IF NOT EXISTS registros 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            dispositivo TEXT, talhao TEXT, atividade TEXT, quantidade TEXT, data_hora TEXT, obs TEXT)''')
        conn.close()

    def inserir(self, d):
        try:
            conn = self.conectar()
            conn.execute("INSERT INTO registros (dispositivo, talhao, atividade, quantidade, data_hora, obs) VALUES (?,?,?,?,?,?)",
                        (d['dispositivo'], d['talhao'], d['atividade'], d['quantidade'], d['dataHora'], d['observacoes']))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False

    def ler(self):
        conn = self.conectar()
        res = conn.execute("SELECT * FROM registros ORDER BY id DESC").fetchall()
        conn.close()
        return res