from tkinter import *
from tkinter import ttk, Entry
import sqlite3
import json
import requests
from time import * # Da um tempo p\ carregar
from keysymdef import keysymdef


root = Tk()

class funcs():

    #def exibe(self): Trqtamento de erro
        #messagebox.showinfo('Python Progressivo', 'Seu nome é: ' + self.entrada.get())

    def limpar_tela(self):
        self.entry_ID.delete(0, END)
        self.entry_cliente.delete(0, END)
        self.entry_CPF.delete(0, END)
        self.entry_data.delete(0, END)
        self.select_lista()
    def conectar_bd(self):
    # #Criando o Banco de Dados:
        self.conexao = sqlite3.connect('clientes.db')
    # # Criando o cursor:
        self.c = self.conexao.cursor(), print("Conectado ao Banco de Dados!")
    def desconectar_bd(self):
        # #Fechar o banco de dados:
        self.conexao.close()
    def montarTabela(self):
        self.conectar_bd()
        # # Criando a tabela:
        self.conexao.execute("""CREATE TABLE IF NOT EXISTS clientes 
        (
        	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        	nome TEXT NOT NULL,
        	cpf	VARCHAR(11) NOT NULL,
        	data DATE NOT NULL
        );
        """)

        print('Tabela criada com sucesso.')

        # #Commit as mudanças:
        self.conexao.commit()
        self.desconectar_bd()
    def variaveis(self):
        self.ID = self.entry_ID.get()
        self.nome = self.entry_cliente.get()
        self.cpf = self.entry_CPF.get()
        self.data_nasc = self.entry_data.get()
    def add_clientes(self):
        self.variaveis()
        self.conectar_bd()

        # inserindo dados na tabela

        self.conexao.execute("""
           INSERT INTO clientes (nome, cpf, data)
           VALUES (?,?,?)
           """, (self.nome, self.cpf, self.data_nasc))

        # Commit as mudanças:
        self.conexao.commit()

        self.desconectar_bd()

        self.select_lista()
        self.limpar_tela()

        print('Dados inseridos com sucesso.')
        # Fechar o banco de dados:
        self.conexao.close()
    def select_lista(self):

        self.listabd1.delete(*self.listabd1.get_children())
        self.conectar_bd()
        lista = self.conexao.execute("""SELECT id, nome, cpf, data FROM clientes ORDER BY id ASC;""")
        # ASC ou DESC, os dados da tabela serão retornados em ordem ascendente, que é o valor padrão.

        for i in lista:
            self.listabd1.insert("", END, values=i)
        self.desconectar_bd()
    def onDoubleClick(self, event):
        self.limpar_tela()
        self.listabd1.selection()


        for n in self.listabd1.selection():
            col0, col1, col2, col3, col4 = self.listabd1.item(n, 'values')
            self.entry_ID.insert(END, col1)
            self.entry_cliente.insert(END, col2)
            self.entry_CPF.insert(END, col3)
            self.entry_data.insert(END, col4)

        self.select_lista()

    def deleta_cliente(self):
        self.variaveis()
        self.conectar_bd()
        self.conexao.execute("""DELETE FROM clientes WHERE id = ? """, (self.ID)) # ERROOOOOOOOOOOOOOOOOOO
        self.conexao.commit()
        self.desconectar_bd()
        self.limpar_tela()
        self.select_lista()
    def buscar_cliente(self):
        self.conectar_bd()
        self.listabd1.delete(*self.listabd1.get_children())

        self.entry_cliente.insert(END, '%')
        nome = self.entry_cliente.get()
        self.conexao.execute(
            """
            SELECT id, nome, cpf FROM clientes
            WHERE nome LIKE '%s ORDER BY nome ASC'
            """ % nome)
        buscarNomelf1 = self.conexao.fetchall()
        for i in buscarNomelf1:
            self.listabd1.insert("", END, values=i)

        self.select_lista()
        self.limpar_tela()
        self.desconectar_bd()



    def consulta_CPF(self):



        print("Consultand9o")

        self.variaveis()
        token = ""
        cpf = self.cpf
        data_nascimento = self.data_nasc
        url = "https://www.sintegraws.com.br/api/v1/execute-api.php"

        querystring = {"token": {token}, "cpf": {cpf}, "data-nascimento": {data_nascimento},
                       "plugin": "CPF".format()}

        response = requests.request("GET", url, params=querystring)
        global resp #Variavel Global p\ Ser rodada na label !!
        resp = json.loads(response.text)
        #DIVIDINDO AS requisições por ID
        cpf_nome = resp['nome']
        cpf_cpf = resp['cpf']
        cpf_data = resp['data_nascimento']
        cpf_situacao = resp['situacao_cadastral']
        cpf_data_ins = resp['data_inscricao']
        cpf_genero = resp['genero']
        cpf_uf = resp['uf']
        cpf_obito = resp['ano_obito']
        #Criar Uma Label p\ cada ID
        self.lb_Resultado['text'] = 'Nome: '+cpf_nome


        print(resp)
        return resp
        '''{'code': '0', 'status': 'OK', 'message': 'Pesquisa realizada com sucesso.', 'cpf': '056.938.331-51', 'nome': 'LUCIO FLAVIO DA MOTTA SILVA', 'data_nascimento': '24/06/2003', 'situacao_cadastral': 'Regular', 'data_inscricao': '03/01/2012', 'genero': 'M', 'uf': ['DF', 'GO', 'MS', 'TO'], 'digito_verificador': '00', 'comprovante': 'D570.FCC9.272F.6FCB', 'ano_obito': '', 'version': '1'}
'''

    def consultar_saldo(self):
        print("Consultandooooo")


        token = ""

        url = "https://www.sintegraws.com.br/api/v1/consulta-saldo.php"

        querystring = {"token": {token}}

        response = requests.request("GET", url, params=querystring)

        #print(response.text)

        #return response.text #Retornar o txt p\ armazenar em outras variaves

        resp = json.loads(response.text)



        print(resp['qtd_consultas_disponiveis'])
        return resp['qtd_consultas_disponiveis']


class aplication(funcs): #dizer p\ classe que pode usar as funções da class funcs

    def __init__(self):
        self.entry_cliente = Entry(root)
        self.entry_cpf = Entry(root)

        self.root = root
        self.Tela()
        self.frame_da_tela()#Chamar na aplicação
        self.widget_frame()
        self.widget_frame_02()
        self.lista_frame1()
        self.montarTabela()
        self.select_lista()
        self.add_clientes()
        self.Menus()

        root.mainloop()

    def Tela(self):
        self.root.title('system Bilheteria')
        self.root.configure(background= '#fff4b8')
        self.root.geometry("780x550")
        self.root.resizable(True, True)
        self.root.maxsize(width= 1650, height= 1650)

    def frame_da_tela(self):
        self.frame_1 = Frame(self.root, bd= 4, bg='#EEE8AA' )#bd\bg colocar uma borda com cor
    #Abordagem p\ aparecer algo na tela place pack e o gris
        self.frame_1.place(relx=0.02, rely=0.01, relwidth=0.5, relheight=0.97)#Funciona de 0\1 de esquerda p\ direita

        self.frame_2 = Frame(self.root, bd=4, bg='#fff4b8')  # bd\bg colocar uma borda com cor
    # Abordagem p\ aparecer algo na tela place pack e o gris
        self.frame_2.place(relx=0.54, rely=0.01, relwidth=1, relheight=1)  # Funciona de 0\1 de esquerda p\ direita

    def widget_frame(self):
    #Botão Limpar
        self.bt_limpar = Button(self.frame_1, text= 'Limpar', bg='Black', fg='white', font = ('verdana', 8, 'bold'),
                                command = self.limpar_tela)
        self.bt_limpar.place(relx=0.015, rely=0.5, relwidth=0.23, relheight=0.06)
    # Botão Pesquisar
        self.bt_pesquisar = Button(self.frame_1, text='Pesquisar', bg='Black', fg='white', font=('verdana', 8, 'bold'),
                                   command = '')
        self.bt_pesquisar.place(relx=0.75, rely=0.5, relwidth=0.23, relheight=0.06)

    # Botão ADD Cliente
        self.bt_cliente = Button(self.frame_1, text='ADD Cliente', bg='Black', fg='white', font=('verdana', 8, 'bold'),
                                 command=self.add_clientes)
        self.bt_cliente.place(relx=0.68, rely=0.05, relwidth=0.23, relheight=0.06)

    # Botão Apagar
        self.bt_apagar = Button(self.frame_1, text='Apagar', bg='Black', fg='white', font=('verdana', 8, 'bold'),
                                command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.35, rely=0.5, relwidth=0.23, relheight=0.06)

    # Criando Label de entrada (NOME) / Dados
        self.lb_ID = Label(self.frame_1, text='ID:', bg='#EEE8AA', font=('verdana', 8, 'bold'),)
        self.lb_ID.place(relx=0.001, rely=0.00001)

        self.entry_ID = Entry(self.frame_1, font=('arial', 12))
        self.entry_ID.place(relx=0.001, rely=0.04, relwidth=0.5, relheight=0.04)

        self.lb_CPF = Label(self.frame_1, text='CPF:', bg='#EEE8AA', font=('verdana', 8, 'bold'),)
        self.lb_CPF.place(relx=0.001, rely=0.09)

        self.entry_CPF = Entry(self.frame_1, font=('arial', 12))
        self.entry_CPF.place(relx=0.001, rely=0.13, relwidth=0.5, relheight=0.04)

        self.lb_cliente = Label(self.frame_1, text='Nome Cliente:', bg='#EEE8AA', font=('verdana', 8, 'bold'), )
        self.lb_cliente.place(relx=0.001, rely=0.169)

        self.entry_cliente = Entry(self.frame_1, font=('arial', 12))
        self.entry_cliente.place(relx=0.001, rely=0.20, relwidth=0.5, relheight=0.04)

        self.lb_data = Label(self.frame_1, text='Data de Nascimento:', bg='#EEE8AA', font=('verdana', 8, 'bold'), )
        self.lb_data.place(relx=0.60, rely=0.169)


        self.entry_data = Entry(self.frame_1, justify=CENTER, font=('arial', 12))
        self.entry_data.place(relx=0.60, rely=0.20, relwidth=0.4, relheight=0.04)

    def widget_frame_02(self):
        # WIDGET da Qtd_Saldo
        result_saldo = self.consultar_saldo() #Pegando o return da função
        self.lb_qtd_saldo = Label(self.frame_2, text=result_saldo+'  Acessos ', bg='#fff4b8', font=('verdana', 16, 'bold'), )
        self.lb_qtd_saldo.place(relx=0.2, rely=0.0000009)

        #Widget do Ttitulo Saldo
        self.lb_Saldo = Label(self.frame_2, text='Saldo disponivel:', bg='#fff4b8', font=('verdana', 12, 'bold'), )
        self.lb_Saldo.place(relx=0.001, rely=0.009)

        #Botão CPF
        self.bt_consulta = Button(self.frame_2, text='Consultar CPF', bg='Black', fg='white', font=('verdana', 8, 'bold'),
                                   command=self.consulta_CPF)
        self.bt_consulta.place(relx=0.20, rely=0.1, relwidth=0.23, relheight=0.06)

        # Widget do Resultado
        result_consulta = self.consulta_CPF
        self.lb_Resultado = Label(self.frame_2, text=f'{result_consulta}', bg='#fff4b8', font=('verdana', 12, 'bold'), )
        self.lb_Resultado.place(relx=0.0001, rely=0.4)

    def lista_frame1(self):
        self.listabd1 = ttk.Treeview(self.frame_1, height=3, column=("col0", "col1", "col2", "col3", "col4"))
    #Nome das colunas criadas
        self.listabd1.heading("#0", text=" ")
        self.listabd1.heading("#1", text="ID")
        self.listabd1.heading("#2", text="Cliente")
        self.listabd1.heading("#3", text="CPF")
        self.listabd1.heading("#4", text="data")
    #tamanho das colunas
        self.listabd1.column("#0", width=0)
        self.listabd1.column("#1", width=20)
        self.listabd1.column("#2", width=150)
        self.listabd1.column("#3", width=120)
        self.listabd1.column("#4", width=70)
    #Escolher o local
        self.listabd1.place(relx=0.001, rely=0.57, relwidth=0.999, relheight=0.43)

        self.listabd1.bind("<Double-1>", self.onDoubleClick)
    #Barra de rolagem
        self.scroolista = Scrollbar(self.frame_1)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)
        menubar.add_cascade(label="Sobre", menu= filemenu2)

        filemenu.add_command(label="Sair", command= Quit)
        filemenu2.add_command(label="Criador \n @Lucioo_motta" )

        self.select_lista()

aplication()

#Se você quiser várias janelas, crie instâncias de Toplevel<-----