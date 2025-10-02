import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from appBD import AppDB

class TelaPrincipal:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Backlog de Jogos")

        self.root.geometry("1020x400")

    #Componentes da Interface grafica

        #criacao de uma variavel id_jogos para busca
        self.entIDjogo = tk.Entry(root)
        self.entIDjogo.grid_remove()

        #Parte para adicionar o Titulo do game
        self.lblTitulo = tk.Label(root, text='Titulo')
        self.lblTitulo.grid(row = 0, column = 0)
        self.entTitulo = tk.Entry(root)
        self.entTitulo.grid(row=0, column=1)
        
        #Parte para dicionar a Prioridade com ComboBox
        self.lblPrioridade = tk.Label(root, text='Prioridade')
        self.lblPrioridade.grid(row=1, column=0)
        self.boxPrioridade = ttk.Combobox(root)
        self.boxPrioridade.grid(row=1, column=1)
        self.boxPrioridade['values'] = self.db.apoio_selecao('prioridades')

        #Parte para dicionar a Status com ComboBox
        self.lblStatus = tk.Label(root, text='Status')
        self.lblStatus.grid(row=1, column=2)  
        self.boxStatus = ttk.Combobox(root)
        self.boxStatus.grid(row=1, column=3)
        self.boxStatus['values'] = self.db.apoio_selecao('status')

        #Parte para adicinar o Genero com ComboBox
        self.lbtGenero = tk.Label(root, text='Genero')
        self.lbtGenero.grid(row=0, column=2)
        self.boxGenero = ttk.Combobox(root)
        self.boxGenero.grid(row=0, column=3)
        self.boxGenero['values'] = self.db.apoio_selecao('generos')

        #Parte para dicionar a Plataforma com ComboBox
        self.lblPlataforma = tk.Label(root, text=('Plataforma'))
        self.lblPlataforma.grid(row=0, column=4)
        self.boxPlataforma = ttk.Combobox(root)
        self.boxPlataforma.grid(row=0, column=5)
        self.boxPlataforma['values'] = self.db.apoio_selecao('plataformas')

    #Visualizacao de todos os games cadastrados
        #Define quais as informacoes irao aparecer no interface
        self.treeView = ttk.Treeview(root, columns=("id_jogo", "titulo", "prioridade", "status", "genero", "plataforma"), show="headings")
        
        #Informacoes que irao apararecer para o Usuario
        self.treeView.column("id_jogo", width=0, stretch=tk.NO)
        self.treeView.heading("id_jogo", text="")
        self.treeView.heading("titulo", text="Titulo")
        self.treeView.heading("prioridade", text="Prioridade")
        self.treeView.heading("status", text="Status")
        self.treeView.heading("genero", text="Genero")
        self.treeView.heading("plataforma", text="Plataforma")
        
        #Define onde vai aparecer as informacoes
        self.treeView.grid(row=6, column=0, columnspan=6)
        self.treeView.bind('<ButtonRelease-1>', self.apresentarTodosJogos)

    #Partes dedicada aos botoes Adicionar, Editar, Deletar
        self.btInserir = tk.Button(root, text="Adicionar", command=self.fInserirGame)
        self.btInserir.grid(row=4, column=0)
        self.btAtualizar = tk.Button(root, text="Editar", command=self.fEditarGame)
        self.btAtualizar.grid(row=4, column=2)
        self.btDeletar = tk.Button(root, text="Excluir", command=self.fDeletarGame)
        self.btDeletar.grid(row=4, column=4)                

        self.carregarDadosIniciais()

    #Funcao para adicionar um novo game
    def fInserirGame(self):
        #pegar a entrada do Usuario
        titulo = self.entTitulo.get()
        genero = self.boxGenero.get()
        plataforma = self.boxPlataforma.get()
        status = self.boxStatus.get()
        prioridade = self.boxPrioridade.get()

        #pegar os IDs no banco
        id_prioridade = self.db.get_id_by_name('prioridades', prioridade)
        id_status = self.db.get_id_by_name('status', status)
        id_genero = self.db.get_id_by_name('generos', genero)
        id_plataforma = self.db.get_id_by_name('plataformas', plataforma)
    
        if not all([titulo, id_genero, id_plataforma, id_status, id_prioridade]):
            messagebox.showerror("ERRO DE ENTRADA", "Preencha todos os campos")
            return
        
        self.db.inserir_jogos(titulo, id_genero, id_plataforma, id_status, id_prioridade)

        self.fLimparTela()
        self.carregarDadosIniciais()
            
    #Funcao para editar um game 
    def fEditarGame(self):
        idjogo = self.entIDjogo.get()
        titulo = self.entTitulo.get()
        genero = self.boxGenero.get()
        plataforma = self.boxPlataforma.get()
        status = self.boxStatus.get()
        prioridade = self.boxPrioridade.get()  

        id_genero = self.db.get_id_by_name('generos', genero)
        id_plataforma = self.db.get_id_by_name('plataformas', plataforma)
        id_status = self.db.get_id_by_name('status', status)
        id_prioridade = self.db.get_id_by_name('prioridades', prioridade)

        if not all([idjogo, titulo, id_genero, id_plataforma, id_status, id_prioridade]):
            messagebox.showerror("ERRO DE ENTRADA", "Preencha todos os campos")
            return
        
        self.db.update_jogo(idjogo, titulo, id_genero, id_plataforma, id_status, id_prioridade)

        self.fLimparTela()
        self.carregarDadosIniciais()

    #Funcao para deletar Games
    def fDeletarGame(self):
        id_jogo = self.entIDjogo.get()

        if not id_jogo:
            messagebox.showerror("ERRO", "Selecione um jogo para excluir")
            return
    
        self.db.deletar_jogo(id_jogo)
        self.fLimparTela()
        self.carregarDadosIniciais()
    
    #Funcao para limpar a tela
    def fLimparTela(self):
        self.entTitulo.delete(0, tk.END)
        self.boxGenero.set('')
        self.boxPlataforma.set('')
        self.boxStatus.set('')
        self.boxPrioridade.set('')

    #Funcao que mostra os games ja cadastrados
    def apresentarTodosJogos(self, event=None):
        selecao = self.treeView.selection()

        if not selecao:
            return

        item = selecao[0]
        informacoes = self.treeView.item(item, 'values')

        self.entIDjogo.delete(0, tk.END)
        self.entIDjogo.insert(0, informacoes[0])

        self.entTitulo.delete(0, tk.END)
        self.entTitulo.insert(0, informacoes[1])
        
        self.boxPrioridade.set(informacoes[2])
        self.boxStatus.set(informacoes[3])
        self.boxGenero.set(informacoes[4])
        self.boxPlataforma.set(informacoes[5])
        
    #Funcao para carregar todos os dados
    def carregarDadosIniciais(self):
        for item in self.treeView.get_children():
            self.treeView.delete(item)

        jogos = self.db.selecionar_jogos()
        for jogo in jogos:
            self.treeView.insert('', 'end', values=jogo)
    

root = tk.Tk()
app_db = AppDB()
appgui = TelaPrincipal(root, app_db)
root.mainloop()