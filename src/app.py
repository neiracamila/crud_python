from flask import Flask, redirect    # incluimos todo lo necesario para el uso de flask
from flask import render_template, request, redirect # incluimos para el renderizado de template 
from flaskext.mysql import MySQL  
from datetime import datetime

app=Flask(__name__)       # creamos la aplicacion 
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'empleados'

mysql.init_app(app)

@app.route('/')     # para el ruteo de index.html cuando  escriba / en el servidor
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM empleados;"
    cursor.execute(sql)

    empleados = cursor.fetchall()
    
    conn.commit()

    return render_template('empleados/index.html', empleados = empleados)   # renderizo la pagina index.html
    

@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    
    now = datetime.now()
    print(now)
    tiempo = now.strftime("%Y%H%M%S")
    print(tiempo)
    
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, _foto.filename)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/') 


if __name__=='__main__':        # para que python p  ueda interpretar  como (correr flask) empezar a correr la aplicacion
    app.run(debug=True)         # ejecuta la aplicacion en modo debug

