from flask import Flask, render_template,request,redirect,url_for
from flask_mysqldb import MySQL

#render_template: renderiza páginas html. OBS: Jinja2 que é possível criar os templates e usar python dentro do arquivo html
#request: receber requisições do usuário
#redirect e url_for: redirecionamento, url_for determina pra onde redirecionar
#from flask_mysqldb import MySQL: utilizar MySQL como Banco de Dados

app = Flask(__name__,template_folder='templates',static_folder='static')
#name:aplicação principal, não foi importado como módulo
#template_folder: defini o diretório que está os templates
#static_folder: defini o diretório que está os arquivos estáticos, como css e js.

#configuração para conectar BD
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"]  = ""
app.config["MYSQL_DB"] = "flaskClientes"
#abrir conexão
mysql = MySQL(app)

"""
@decorator são métodos que alteram o comportamento de outras funções.
Ex: um decorator para saber se o usuário está logado ou não. Se estiver logado
continua o fluxo do código, se não faz qualquer outra coisa.
"""

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/cadastro/")
@app.route("/cadastro/<cadastrarCliente>",  methods = ["GET","POST"])#URL dinâmicas
def cadastro(cadastrarCliente = None):
    
    if request.method == 'POST' and cadastrarCliente:#se veio por post e cadastrar não está vazio
        #receber dados do formulário
        nome = request.form['nome']
        idade = request.form['idade']
        cpf = request.form['cpf']
          
        #para fazer consultas
        cur = mysql.connection.cursor()
        #inserir no BD
        cur.execute("INSERT INTO clientes (nome,idade,cpf) VALUES (%s,%s,%s)",(nome,idade,cpf))
        #confirmar os comandos no banco
        mysql.connection.commit()
        #fechar conexão do BD
        cur.close()

        return render_template("cadastro.html", status = "block"), 201#criado com sucesso
       

    else: #veio por GET
        return render_template("cadastro.html",status = "none")
   
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

    return render_template("remover.html", dados = dados,status = "none")

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


if __name__ == '__main__':
    app.run(debug=True)


""" 
Outras anotações:
    erros mysql
    https://mysqlclient.readthedocs.io/MySQLdb.html
    MySQLdb._exceptions

    inserir no BD
    cur.execute("SELECT cpf FROM clientes WHERE cpf = %s",(cpf,))
    fetchdata = cur.fetchone()
    if cpf in fetchdata: #cpf está em fecthdata. fetchdata é uma tupla, poderia também ser acessado assim: fetchdata[0]
        print("São iguais: ")


    #outra forma de criar rotas
        def funcao():
        return "<p>2 forma rotas</p>"
    app.add_url_rule("/rota","nomeDaFuncao",nomeDaFuncao)
"""
