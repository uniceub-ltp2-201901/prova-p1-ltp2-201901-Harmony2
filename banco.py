#NOME: JOÃO GABRIEL CAVALCANTE E SILVA
#RA: 21804796
#TABLE professor: nome, datanasc, nomemae, titulacao
#TABLE disciplina: nome, curso, cargahoraria, professor

from flask import Flask
from flask import render_template
from flask import request
import mysql.connector


mdb = mysql.connector.connect(host="localhost", user="root", passwd="root")
db = mdb.cursor()
db.execute("USE faculdade")
db.execute("SELECT nome FROM disciplina WHERE professor = 'marcos'")
materias = db.fetchall()
print(materias)

app = Flask(__name__)

def getTeacher(professor):
    db.execute("SELECT * FROM professor WHERE nome = 'marcos'")
    itens = db.fetchall()
    professor = itens[0][0]
    data = itens[0][1]
    mae = itens[0][2]
    tit = itens[0][3]
    if tit == 1:
        titulo = "especializado"
    elif tit == 2:
        titulo = "mestre"
    elif tit == 3:
        titulo = "doutor"
    return professor, data, mae, titulo

def getMateria(professor):
    db.execute("SELECT nome FROM disciplina WHERE professor = '%s'"%professor)
    materias = db.fetchall()
    return materias


@app.route('/listarProfessores')
def listarProfessores():
    db.execute("SELECT nome FROM professor")
    professores = db.fetchall()
    return render_template("listarProfessores.html", professores=professores)

@app.route('/exibirProfessor/<professor>')
def landing_page(professor):
    itens = getTeacher(professor)
    materias = getMateria(professor)
    return render_template("exibirProfessor.html", itens=itens, materias=materias)

@app.route('/consulatarPorTitulacao')
def consultar():
    return render_template("consultarTitulacao.html")

@app.route("/restit", methods=["GET", "POST"])
def consultartit():
    if request.method == "POST":
        tit = request.form.get("tit")
        db.execute("SELECT nome FROM professor WHERE titulacao = %d"%int(tit))
        professores = db.fetchall()
        return render_template("consultarTitulacao.html", professores=professores)
    else:
        return render_template("consultarTitulacao.html", error="metodo errado")

@app.route("/consularApenasComputacao")
def apenascomp():
    db.execute("SELECT professor FROM disciplina WHERE curso = 'ciência da computação'")
    #db.execute("SELECT professor FROM disciplina WHERE curso = 'cic'")
    
    professores = db.fetchall()
    return render_template("apenasComputacao.html", professores=professores)

@app.route("/calcularSalarioProfessor/<professor>")
def calcular(professor):
    db.execute("SELECT cargahoraria FROM disciplina WHERE professor = '%s'"%professor)
    dados = db.fetchall()
    carga = 0
    for i in dados:
        carga += int(i[0])
    salario = carga*50
    return render_template("salario.html", professor=professor, carga=carga, salario=salario)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')