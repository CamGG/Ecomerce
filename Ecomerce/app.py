import os
from typing_extensions import Required
from flask import Flask , redirect , render_template, request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/ecomerce.db'


db = SQLAlchemy(app)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Integer)

class Deseo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    precio = db.Column(db.String(200))
    caracteristica = db.Column(db.String(500))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    apellido = db.Column(db.String(200))
    correo = db.Column(db.String(200))
    cotrasena = db.Column(db.password(200))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    apellido = db.Column(db.String(200))
    correo = db.Column(db.String(200))
    cotrasena = db.Column(db.password(200))

class Super(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    apellido = db.Column(db.String(200))
    correo = db.Column(db.String(200))
    cotrasena = db.Column(db.password(200))

@app.route('/',methods=['GET'])
def get_home():
    return render_template('index.html')
    
@app.route('/contacts',methods=['GET'])
def get_contactos():
    return render_template('contactos.html')

@app.route('/preguntas',methods=['GET'])
def get_preguntas():
    return render_template('p_Frecuentes.html')
    
@app.route('/singnup',methods=['GET'])
def get_singnup():
    return render_template('registro_Persona.html')
    
#logins
@app.route('/login',methods=['GET'])
def get_login():
    contra = request.args.get("password")
    enc = hashlib.sha256(contra.encode())
    key = enc.hexdigest()  
    return render_template('logins/login_Persona.html')

@app.route('/loginAd',methods=['GET'])
def get_loginad():
    contra2 = request.args.get("passAdmin")
    enc = hashlib.sha256(contra2.encode())
    key = enc.hexdigest()
    return render_template('logins/login_Administrador.html')

@app.route('/loginSu',methods=['GET'])
def get_loginsu():
    contra3 = request.args.get("passSup")
    enc = hashlib.sha256(contra3.encode())
    key = enc.hexdigest()
    return render_template('logins/login_Super.html')

#productos
@app.route('/productosIn',methods=['GET'])
def get_productosin():
    return render_template('productos/productos_invitado.html')

@app.route('/productslog',methods=['GET'])
def get_prodlog():
    return render_template('productos/productos_login.html')

@app.route('/productsadmin',methods=['GET'])
def get_prodadmin():
    return render_template('productos/productos_admin.html')

@app.route('/productssuper',methods=['GET'])
def get_prodsuper():
    return render_template('productos/productos_super.html')

@app.route('/detalleproductolog',methods=['GET'])
def get_detprodlog():
    calificaciones = Calificacion.query.all()
    total_calificaciones = Calificacion.query.count()
    comentarios = Comentario.query.all()
    return render_template('productos/detalle_Productos_login.html', comentarios = comentarios, calificaciones = calificaciones, total_calificaciones = total_calificaciones)

@app.route('/detalleproductoadmin',methods=['GET'])
def get_detproddadmin():
    return render_template('productos/detalle_Productos_admin.html')

@app.route('/detalleproductosuper',methods=['GET'])
def get_detprodsuper():
    return render_template('productos/detalle_Productos_super.html')

#menus
@app.route('/menuadmin',methods=['GET'])
def get_menuadmin():
    return render_template('menus/menu_admin.html')

@app.route('/menusuper',methods=['GET'])
def get_menusuper():
    return render_template('menus/menu_super.html')

@app.route('/menulogin',methods=['GET'])
def get_menulogin():
    return render_template('menus/menu_login.html')

@app.route('/contactslog',methods=['GET'])
def get_contactoslog():
    return render_template('menus/contactos_login.html')

@app.route('/contactssuper',methods=['GET'])
def get_contactossuper():
    return render_template('menus/contactos_super.html')

@app.route('/preguntaslog',methods=['GET'])
def get_preguntaslog():
    return render_template('menus/p_Frecuentes_login.html')

@app.route('/preguntassuper',methods=['GET'])
def get_preguntassuper():
    return render_template('menus/p_Frecuentes_super.html')

#mi_cuenta
@app.route('/milog',methods=['GET'])
def get_micuentalog():
    return render_template('mi_cuenta/mi_Cuenta_login.html')

@app.route('/miadmin',methods=['GET'])
def get_micuentaadmin():
    return render_template('mi_cuenta/mi_Cuenta_admin.html')

@app.route('/misuper',methods=['GET'])
def get_micuentasuper():
    return render_template('mi_cuenta/mi_Cuenta_super.html')

#comentarios login
@app.route('/comentar')
def comentar():
    comentarios = Comentario.query.all()
    return render_template('gestor_Comentarios/agregar_Comentario.html', comentarios = comentarios)

@app.route('/create_comentario', methods=['POST'])
def create_comentario():
    new_comentario = Comentario(content=request.form['content'])
    db.session.add(new_comentario)
    db.session.commit()
    return redirect('detalleproductolog')

#calificar login
@app.route('/calificar')
def calificar():
    calificaciones = Calificacion.query.all()
    total_calificaciones = Calificacion.query.count()
    return render_template('gestor_Calificaciones/agregar_Calificacion.html', calificaciones = calificaciones, total_calificaciones = total_calificaciones)

@app.route('/create_calificacion', methods=['POST'])
def create_calificacion():
    new_calificacion = Calificacion(content=request.form['content'])
    db.session.add(new_calificacion)
    db.session.commit()
    return redirect('detalleproductolog')

#desear login
@app.route('/desear')
def desear():
    deseos = Deseo.query.all()
    return render_template('gestor_Deseos/listar_Deseo.html', deseos = deseos)

@app.route('/create_deseo', methods=['POST'])
def create_deseo():
    new_deseo = Deseo(content=request.form['content'])
    db.session.add(new_deseo)
    db.session.commit()
    return redirect('detalleproductolog')

#comentarios super
@app.route('/comentar_super')
def comentar_super():
    comentarios = Comentario.query.all()
    return render_template('gestor_Comentarios/agregar_Comentario.html', comentarios = comentarios)

@app.route('/create_comentario_super', methods=['POST'])
def create_comentario_super():
    new_comentario = Comentario(content=request.form['content'])
    db.session.add(new_comentario)
    db.session.commit()
    return redirect('detalleproductosuper')

@app.route('/editar_comentario_super/<int: id>', methods=['GET', 'POST'])
def editar_comentario_super(id):
    comentario = Comentario.query.get_or_404(id)
    comentariobj = Comentario(content=request.form['content'])
    if request.method == 'POST':
        if comentariobj.validate_on_submit():
            comentariobj.populate_obj(comentario)
    db.session.commit()
    return redirect('detalleproductosuper', comentariobj = comentario)

@app.route('/eliminar_comentario/<int: id>')
def eliminar_comentario_super(id):
    comentario = Comentario.query.get_or_404(id)
    comentariobj = Comentario(content=request.form['content'])
    db.session.delete(comentario)
    db.session.commit()
    return redirect('detalleproductosuper')

#calificar admin
@app.route('/calificar_super')
def calificar_super():
    calificaciones = Calificacion.query.all()
    total_calificaciones = Calificacion.query.count()
    return render_template('gestor_Calificaciones/agregar_Calificacion.html', calificaciones = calificaciones, total_calificaciones = total_calificaciones)

@app.route('/create_calificacion_super', methods=['POST'])
def create_calificacion_super():
    new_calificacion = Calificacion(content=request.form['content'])
    db.session.add(new_calificacion)
    db.session.commit()
    return redirect('detalleproductosuper')

@app.route('/eliminar_calificar/<int: id>')
def eliminar_calificar_super(id):
    calificacion = Calificacion.query.get_or_404(id)
    db.session.delete(calificacion)
    db.session.commit()
    return redirect('detalleproductosuper')

#desear super
@app.route('/desear_super')
def desear_super():
    deseos = Deseo.query.all()
    return render_template('gestor_Deseos/listar_Deseo.html', deseos = deseos)

@app.route('/create_deseo_super', methods=['POST'])
def create_deseo_super():
    new_deseo = Deseo(content=request.form['content'])
    db.session.add(new_deseo)
    db.session.commit()
    return redirect('detalleproductosuper')

@app.route('/editar_deseo_super/<int: id>', methods=['GET', 'POST'])
def editar_deseo_super(id):
    deseo = Deseo.query.get_or_404(id)
    deseobj = Deseo(content=request.form['content'])
    if request.method == 'POST':
        if deseobj.validate_on_submit():
            deseobj.populate_obj(deseo)
    db.session.commit()
    return redirect('detalleproductosuper', deseobj = deseo)

@app.route('/eliminar_deseo/<int: id>')
def eliminar_deseo_super(id):
    deseo = Deseo.query.get_or_404(id)
    db.session.delete(deseo)
    db.session.commit()
    return redirect('detalleproductosuper')

#productos super_admin
@app.route('/producto')
def producto():
    productos = producto.query.all()
    return render_template('gestor_Productos/listar_Producto.html', productos=productos)

@app.route('/create_producto', methods=['POST'])
def create_producto():
    new_producto = producto(content=request.form['nombre', 'precio', 'caracteristicas'])
    db.session.add(new_producto)
    db.session.commit()
    return redirect('producto')

@app.route('/editar_producto/<int: id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    productobj = Producto(content=request.form['nombre', 'precio', 'caracteristicas'])
    if request.method == 'POST':
        if productobj.validate_on_submit():
            productobj.populate_obj(producto)
    db.session.commit()
    return redirect('producto', productobj = producto)

@app.route('/eliminar_producto/<int: id>')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect('producto')
      
#productos super_admin
@app.route('/producto')
def producto():
    productos = producto.query.all()
    return render_template('gestor_Productos/listar_Producto.html', productos=productos)

@app.route('/create_producto', methods=['POST'])
def create_producto():
    new_producto = producto(content=request.form['nombre', 'precio', 'caracteristicas'])
    db.session.add(new_producto)
    db.session.commit()
    return redirect('producto')

@app.route('/editar_producto/<int: id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    productobj = Producto(content=request.form['nombre', 'precio', 'caracteristicas'])
    if request.method == 'POST':
        if productobj.validate_on_submit():
            productobj.populate_obj(producto)
    db.session.commit()
    return redirect('producto', productobj = producto)

@app.route('/eliminar_producto/<int: id>')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect('producto')

#productos super_admin
@app.route('/producto')
def producto():
    productos = producto.query.all()
    return render_template('gestor_Productos/listar_Producto.html', productos=productos)

@app.route('/create_producto', methods=['POST'])
def create_producto():
    new_producto = producto(content=request.form['nombre', 'precio', 'caracteristicas'])
    db.session.add(new_producto)
    db.session.commit()
    return redirect('producto')

@app.route('/editar_producto/<int: id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    productobj = Producto(content=request.form['nombre', 'precio', 'caracteristicas'])
    if request.method == 'POST':
        if productobj.validate_on_submit():
            productobj.populate_obj(producto)
    db.session.commit()
    return redirect('producto', productobj = producto)

@app.route('/eliminar_producto/<int: id>')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect('producto')

#usuario
@app.route('/persona')
def usuario():
    usuarios = Usuario.query.all()
    return render_template('gestor_Personas/listar_Persona.html', usuarios=usuarios)

@app.route('/registro', methods=['POST'])
def create_usuario():
    new_usuario = usuario(content=request.form['nombre', 'apellido', 'correo', 'contrasena'])
    db.session.add(new_usuario)
    db.session.commit()
    return redirect('login')

@app.route('/editar_persona/<int: id>', methods=['GET', 'POST'])
def editar_persona(id):
    usuario = Usuario.query.get_or_404(id)
    usuariobj = Usuario(content=request.form['nombre', 'apellido', 'correo', 'contrasena'])
    if request.method == 'POST':
        if usuariobj.validate_on_submit():
            usuariobj.populate_obj(usuario)
    db.session.commit()
    return redirect('persona', usuarioobj = usuario)

@app.route('/eliminar_persona/<int: id>')
def eliminar_persona(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect('usuario')

@app.route('/signup',methods=['POST'])
def signup():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    usuario = Usuario(nombre=nombre,apellido=apellido, correo=correo, contrasena=contrasena)
    db.session.add(usuario)
    db.session.commit()
    usuario = Usuario.query.filter_by(correo=correo).first()
    login_super(usuario)
    return redirect('login')

#admin
@app.route('/login_admin',methods=['POST'])
def login_admin():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    admin = Admin.query.filter_by(correo=correo, contrasena=contrasena).first()
    login_admin(admin)
    return redirect('menusuper')

#super
@app.route('/login_super',methods=['POST'])
def login_super():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    super = Super.query.filter_by(correo=correo, contrasena=contrasena).first()
    login_super(super)
    return redirect('menusuper')

@app.route('/logout',methods=['GET'])
def logout():
    logout()
    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)