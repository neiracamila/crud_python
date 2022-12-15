from flask import Flask, redirect    # incluimos todo lo necesario para el uso de flask
from flask import render_template, request, redirect # incluimos para el renderizado de template 
from flaskext.mysql import MySQL  
from datetime import datetime
import os


app=Flask(__name__)       # creamos la aplicacion 
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'empleados'
mysql.init_app(app)

CARPETA= os.path.join('/uploads')    # referencia a la carpeta de fotos
app.config['CARPETA']=CARPETA    

@app.route('/')     # para el ruteo de index.html cuando  escriba / en el servidor
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM empleados;"
    cursor.execute(sql)
    empleados = cursor.fetchall()
    conn.commit()

    return render_template('empleados/index.html', empleados = empleados)   # renderizo la pagina index.html    

@app.route('/destroy/<int:id>')
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['post'])
def update():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    id=request.form['txtId']

    sql='UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s'
    datos=(_nombre, _correo, id)

    conn = mysql.connect()
    cursor=conn.cursor()
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save('./uploads/'+nuevoNombreFoto)
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute('UPDATE empleados SET foto=%s WHERE id=%s', (nuevoNombreFoto, id))
        conn.commit()
    return redirect('/')


    # cursor.execute(sql, datos)
    # conn.commit()

    # return redirect('/')

@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)
   
        sql = "INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s);"
        datos = (_nombre, _correo,nuevoNombreFoto)

        # sql = "SELECT * FROM empleados;"
        # cursor.execute(sql)
        # empleados = cursor.fetchall()

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()

    return render_template('empleados/index.html') 




if __name__=='__main__':        # para que python p  ueda interpretar  como (correr flask) empezar a correr la aplicacion
    app.run(debug=True)         # ejecuta la aplicacion en modo debug

