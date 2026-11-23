import tkinter as tk
from tkinter import messagebox
import sqlite3

# ligar a base de dados
ligacao = sqlite3.connect("agenda.db")
cursor = ligacao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS utilizadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
ligacao.commit()

def criar_conta():
    user = caixa_user.get()
    pw = caixa_pass.get()

    if user == "" or pw == "":
        messagebox.showwarning("AVISO", "FALTA PREENCHER CAMPOS!")
        return

    if len(pw) < 6:
        messagebox.showwarning("AVISO", "A PASSWORD DEVE TER PELOS MENOS 6 LETRAS OU NÚMEROS.")
        return

    try:
        cursor.execute("INSERT INTO utilizadores (username, password) VALUES (?, ?)", (user, pw))
        ligacao.commit()
        messagebox.showinfo("BOA", "CONTA CRIADA! JÁ PODE ENTRAR.")
        
        caixa_user.delete(0, tk.END)
        caixa_pass.delete(0, tk.END)
    except:
        messagebox.showerror("ERRO", "ESSE NOME JÁ ESTÁ A SER USADO.")

def entrar():
    user = caixa_user.get()
    pw = caixa_pass.get()

    if user == "" or pw == "":
        messagebox.showwarning("AVISO", "PREENCHE TUDO PRIMEIRO!")
        return

    cursor.execute("SELECT * FROM utilizadores WHERE username = ? AND password = ?", (user, pw))
    resultado = cursor.fetchone()

    if resultado:
        janela.destroy()
        janela_principal(user)
    else:
        messagebox.showerror("ERRO", "DADOS INCORRETOS, TENTA OUTRA VEZ.")

def ver_pass():
    if caixa_pass.cget("show") == "*":
        caixa_pass.config(show="")
        btn_ver.config(text="ESCONDER")
    else:
        caixa_pass.config(show="*")
        btn_ver.config(text="MOSTRAR")

def janela_principal(nome):
    app = tk.Tk()
    app.title("MINHA AGENDA")
    app.geometry("500x400")

    lbl1 = tk.Label(app, text="OLÁ " + nome, font=("Arial", 18, "bold"))
    lbl1.pack(pady=30)

    # parte que ainda falta acabar
    lbl2 = tk.Label(app, text="(AQUI VAI FICAR A LISTA DE TAREFAS - AINDA POR FAZER)", fg="gray")
    lbl2.pack(pady=20)

    btn_adicionar = tk.Button(app, text="ADICIONAR TAREFA", state="disabled")
    btn_adicionar.pack(pady=10)

    btn_sair = tk.Button(app, text="SAIR", command=app.destroy)
    btn_sair.pack(pady=40)

    app.mainloop()

# --- janela inicial ---
janela = tk.Tk()
janela.title("LOGIN")
janela.geometry("350x400")

titulo = tk.Label(janela, text="AGENDA", font=("Arial", 20, "bold"))
titulo.pack(pady=20)

tk.Label(janela, text="UTILIZADOR:").pack()
caixa_user = tk.Entry(janela, width=25)
caixa_user.pack(pady=5)

tk.Label(janela, text="PASSWORD:").pack(pady=(10, 0))
caixa_pass = tk.Entry(janela, width=25, show="*")
caixa_pass.pack(pady=5)

btn_ver = tk.Button(janela, text="MOSTRAR", command=ver_pass)
btn_ver.pack(pady=5)

btn_entrar = tk.Button(janela, text="ENTRAR", width=20, bg="black", fg="white", command=entrar)
btn_entrar.pack(pady=20)

btn_registar = tk.Button(janela, text="CRIAR CONTA NOVA", command=criar_conta)
btn_registar.pack()

janela.mainloop()
ligacao.close()
