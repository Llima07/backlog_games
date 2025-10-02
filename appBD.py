import sqlite3
from sqlite3 import Error

#Classe do app
class AppDB:
    def __init__(self):
        self.conexao = None
        self.cursor = None 
        self.conectar_db()
    
    def conectar_db(self):
        self.conexao = sqlite3.connect('backlog_jogos.db')
        self.conexao.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conexao.cursor()
        print('Conexao bem sucedida!')

    #Funcao para selecionar e mostrar todos os jogos
    def selecionar_jogos(self):

        try:
            self.cursor.execute("""
                SELECT 
                    j.id_jogo,
                    j.titulo,
                    r.prioridade,
                    s.status,
                    g.genero,
                    p.plataforma
                FROM jogos j
                JOIN prioridades r  ON j.prioridade = r.id_prioridade
                JOIN generos g       ON j.genero = g.id_genero
                JOIN plataformas p  ON j.plataforma = p.id_plataforma
                JOIN status s       ON j.status = s.id_status
                ORDER BY r.id_prioridade ASC""")
            jogos = self.cursor.fetchall()
            return jogos
        
        except Error as e:
            print(f'ERRO AO MOSTRAR JOGOS\nerro: {e}')

    #Funcao para Inserir novos Jogos
    def inserir_jogos(self, titulo, id_genero, id_plataforma, id_status, id_prioridade):
        try:
            self.cursor.execute(""" 
                INSERT INTO jogos (titulo, genero, plataforma, status, prioridade)
                        VALUES(?, ?, ?, ?, ?)""",(titulo, id_genero, id_plataforma, id_status, id_prioridade))

            self.conexao.commit()
            print('Adicionado com sucesso')
        except Error as e:
            print(f'ERRO AO INSERIR JOGOS\nerro: {e}')

    #Funcao para realizar updates nos jogos ja existentes
    def update_jogo(self, id_jogo, titulo, id_genero, id_plataforma, id_status, id_prioridade):
        try:
            self.cursor.execute("""
                UPDATE jogos SET 
                        titulo = ?, 
                        genero = ?, 
                        plataforma = ?, 
                        status =?, 
                        prioridade =?
                    WHERE id_jogo = ?""", (titulo, id_genero, id_plataforma, id_status, id_prioridade, id_jogo))

            self.conexao.commit()
            print("Atualizado com sucesso.")

        except Error as e:
            print(f'ERRO AO ATUALIZAR JOGOS\nerro: {e}')
    
    #Funcao para deletar algum game
    def deletar_jogo(self, id_jogo):
        try:
            self.cursor.execute("""
                DELETE FROM jogos
                    WHERE id_jogo = ?""", (id_jogo,))

            self.conexao.commit()
            print('Deletado com sucesso')
        
        except Error as e:
            print(f'ERRO AO DELETAR JOGOS\nerro: {e}')

    def get_id_by_name(self, tabela, item): 
        mapeamento_colunas = { 
            'generos' : 'genero',
            'plataformas' : 'plataforma',
            'status' : 'status',
            'prioridades' : 'prioridade'
        }

        nome_coluna = mapeamento_colunas.get(tabela, tabela[:-1])
        id_coluna = f'id_{nome_coluna}'
        comando_selecao = f"SELECT {id_coluna} FROM {tabela} WHERE {nome_coluna} = ?"

        try:
            self.cursor.execute(comando_selecao, (item,))
            resultado = self.cursor.fetchone() 
            # Retorna o ID (o primeiro elemento da tupla)
            return resultado[0] if resultado else None
        
        except Error as e:
            self.conexao.rollback()
            print(f"Erro ao buscar ID na tabela {tabela}: {e}")
            return None
    
    def apoio_selecao(self, tabela):
        mapeamento_colunas = {
            'prioridades': 'prioridade',
            'status': 'status',
            'generos': 'genero',
            'plataformas': 'plataforma'
        }

        nome_coluna = mapeamento_colunas.get(tabela, tabela[:-1])

        comando = f"SELECT {nome_coluna} FROM {tabela} ORDER BY {nome_coluna}"

        try:
            self.cursor.execute(comando)
            resultados = self.cursor.fetchall()
            nomes = [item[0] for item in resultados]
            return nomes
        except Error as e:
            self.conexao.rollback()
            print(f"Erro ao buscar nomes da tabela {tabela}: {e}")
            return []     
        
if __name__ == '__main__':
    app_bd = AppDB