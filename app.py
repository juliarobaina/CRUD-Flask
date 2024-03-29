from flask import Flask, render_template,request,redirect,url_for
from flask_mysqldb import MySQL

#render_template: renderiza páginas html. OBS: Jinja2 que é possível criar os templates e usar python dentro do arquivo html. Não altera a URL.
#request: receber requisições do usuário
#redirect e url_for: redirecionamento, url_for determina pra onde redirecionar utilizando o nome da função, altera a URL, status HTTP por padrão 302
#from flask_mysqldb import MySQL: utilizar MySQL como Banco de Dados

app = Flask(__name__)#Flask(__name__,template_folder='templates',static_folder='static') está com o valor padrão, por isso não precisa explicitar templates e static se for com esses valores
#name:aplicação principal, não foi importado como módulo
#template_folder: defini o diretório que está os templates
#static_folder: defini o diretório que está os arquivos estáticos, como css e js.

#configuração para conectar BD
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"]  = ""
app.config["MYSQL_DB"] = "flaskClientes2"
#abrir conexão
mysql = MySQL(app)

"""
@decorator são métodos que alteram o comportamento de outras funções.
"""

@app.route("/")
def index():
    return render_template("index.html")

#Função para descobrir se o cpf digitado pelo usuário já existe no BD
def cpfRepetido(dados,cpf):
    #cpfRepetido com valor 0 cpf do usuário não existe no BD. cpfRepetido 1 cpf já existe
    cpfRepetido = 0
    #Verificando CPF's do BD com o do usuário
    for dataBD in dados:
        if cpf in dataBD: #Se CPF's são iguais
            cpfRepetido = 1
            break
    return cpfRepetido

@app.route("/cadastro/")
def cadastro():
    return render_template("cadastro.html",status = "none")
    

@app.route("/cadastrarCliente",  methods = ["GET","POST"])#URL dinâmicas
def cadastrarCliente():
    
    if request.method == 'POST':#se veio por post
        #receber dados do formulário
        nome = request.form['nome']
        idade = request.form['idade']
        cpf = request.form['cpf']

        if nome and idade and cpf:
            #para fazer consultas
            cur = mysql.connection.cursor()

            #consultar no BD
            cur.execute("SELECT * FROM clientes")
            #obter os dados em uma lista de tuplas
            dados = cur.fetchall()
            
            #Caso exista CPF repetido
            if cpfRepetido(dados,cpf):
                return redirect(url_for("cadastro"))


            #inserir no BD
            cur.execute("INSERT INTO clientes (nome,idade,cpf) VALUES (%s,%s,%s)",(nome,idade,cpf))
            #confirmar os comandos no banco
            mysql.connection.commit()
            #fechar conexão do BD
            cur.close()

            return redirect(url_for("cadastro"))

        else:
            return redirect(url_for("cadastro"))
            
    else: #veio por GET
        return redirect(url_for("cadastro"))
       
   
@app.route("/remover")
def remover():
    #para fazer consultas
    cur = mysql.connection.cursor()
    #consultar no BD
    cur.execute("SELECT * FROM clientes")
    #obter os dados em uma lista de tuplas
    dados = cur.fetchall()
    #confirmar os comandos no banco
    mysql.connection.commit()
    #fechar conexão do BD
    cur.close()

    return render_template("remover.html", dados = dados)

#pegar id da URL
@app.route("/removerCliente/<idCliente>")
def removerCliente(idCliente):
      
    #para fazer consultas
    cur = mysql.connection.cursor()
    #excluir o cliente
    cur.execute("DELETE FROM clientes WHERE id = %s"%idCliente)
    #confirmar os comandos no banco
    mysql.connection.commit()
    #fechar conexão do BD
    cur.close()

    return redirect(url_for('remover'))

@app.route("/alterar")
def alterar():
    #para fazer consultas
    cur = mysql.connection.cursor()
    #consultar no BD
    cur.execute("SELECT * FROM clientes")
    #obter os dados em uma lista de tuplas
    dados = cur.fetchall()
    #confirmar os comandos no banco
    mysql.connection.commit()
    #fechar conexão do BD
    cur.close()

    return render_template("alterar.html", dados = dados)


@app.route("/formularioAlterarCliente/<idCliente>")
def formAlterarCliente(idCliente = None):

    if idCliente:
        #para fazer consultas
        cur = mysql.connection.cursor()
        #consultar no BD
        cur.execute("SELECT * FROM clientes WHERE id = %s"%idCliente)
        #obter os dados em uma lista de tuplas
        dados = cur.fetchall()
        #confirmar os comandos no banco
        mysql.connection.commit()
        #fechar conexão do BD
        cur.close()

        return render_template("formAlterarCliente.html", dados = dados)
    else:
       return redirect(url_for('alterar')) 

#pegar id da URL
@app.route("/alterarCliente", methods = ["POST"])
def alterarCliente():
   
    if request.method == 'POST':
       
        idCliente = request.form['id']
        nome = request.form['nome']
        idade = request.form['idade']
        cpf = request.form['cpf']
       
        if nome and idade and cpf:

            #para fazer consultas
            cur = mysql.connection.cursor()            
            #alterar o cliente
            sql = "UPDATE clientes SET nome = %s, idade = %s, cpf = %s WHERE id = %s"
            val = (nome,idade, cpf, idCliente)
            cur.execute(sql, val)
            #confirmar os comandos no banco
            mysql.connection.commit()
            #fechar conexão do BD
            cur.close()
        

    return redirect(url_for('alterar'))

    

if __name__ == '__main__':
    app.run(debug=True)
