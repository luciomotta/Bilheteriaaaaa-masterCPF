import sqlite3
import tkinter
def Consulta_app():
    #Criando Janela:
    import tkinter as tk
    janela = tkinter.Tk()
    janela.title('Consulta Cliente ALIBABA')
    janela.attributes('-fullscreen', True)
    janela.configure(bg='black')
    janela.mainloop()


    def Consulta_Cliente():
        conexao = sqlite3.connect('clientes.db')
        c = conexao.cursor()

        #Inserir dados na tabela:
        c.execute('''SELECT * FROM  cliente''')


        # Commit as mudanças:
        conexao.commit()

        # Fechar o banco de dados:
        conexao.close()

Consulta_app()


