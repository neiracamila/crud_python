from flask import Flask, render_template, request, redirect # incluimos para el renderizado de template 
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

UPLOADS = os.path.join('uploads')    # referencia a la carpeta de fotos
app.config['UPLOADS']= UPLOADS    

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
    sql='DELETE FROM empleados WHERE id=%s;'
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, id)
    conn.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    sql='SELECT * FROM empleados WHERE id=%s;'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['post'])
def update():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    id=request.form['txtId']

    datos=(_nombre, _correo, id)

    conn = mysql.connect()
    cursor=conn.cursor()
    
    if _foto.filename != '':    
        now=datetime.now()
        tiempo=now.strftime("%Y%H%M%S")
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save('src/uploads/'+nuevoNombreFoto)
        
    sql= 'SELECT foto FROM empleados WHERE id=%s;'    
    cursor.execute(sql, id)

    nombreFoto=cursor.fetchone()[0]

    os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))

    sql='UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;'
    cursor.execute(sql,id)
    conn.commit()

    return redirect('/')


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
        _foto.save('src/uploads/' + nuevoNombreFoto)
   
        sql = "INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s);"
        datos = (_nombre, _correo,nuevoNombreFoto)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()

    return redirect('/') 


if __name__=='__main__':        # para que python p  ueda interpretar  como (correr flask) empezar a correr la aplicacion
    app.run(debug=True)         # ejecuta la aplicacion en modo debug

