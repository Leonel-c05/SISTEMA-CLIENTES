from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import date

app = Flask(__name__)

# =========================================
# CONEXION MYSQL
# =========================================

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sistema_tecnico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================================
# MODELO CLIENTES
# =========================================

class Cliente(db.Model):

    __tablename__ = 'clientes'

    id_cliente = db.Column(db.Integer, primary_key=True)

    cedula = db.Column(db.String(15))
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    correo = db.Column(db.String(100))

# =========================================
# MODELO EQUIPOS
# =========================================

class Equipo(db.Model):

    __tablename__ = 'equipos'

    id_equipo = db.Column(db.Integer, primary_key=True)

    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey('clientes.id_cliente')
    )

    tipo_equipo = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    numero_serie = db.Column(db.String(100))
    observaciones = db.Column(db.Text)
    estado = db.Column(db.String(30))

    # RELACION CON CLIENTES
    cliente = db.relationship(
        'Cliente',
        backref='equipos'
    )

# =========================================
# MODELO INVENTARIO
# =========================================

class Inventario(db.Model):

    __tablename__ = 'inventario'

    id_producto = db.Column(db.Integer, primary_key=True)

    nombre_producto = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    stock = db.Column(db.Integer)
    precio = db.Column(db.Float)
    categoria = db.Column(db.String(100))
    fecha_registro = db.Column(db.Date)

# =========================================
# MODELO USUARIOS
# =========================================

class Usuario(db.Model):

    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100))

    usuario = db.Column(db.String(100))

    correo = db.Column(db.String(100))

    password = db.Column(db.String(255))

    rol = db.Column(db.String(50))

    fecha_creacion = db.Column(db.Date)
# =========================================
# RUTA INICIO
# =========================================

@app.route('/')
def inicio():

    return render_template('index.html')

# =========================================
# LISTAR CLIENTES
# =========================================

@app.route('/clientes')
def clientes():

    lista_clientes = Cliente.query.all()

    return render_template(
        'clientes/lista_clientes.html',
        clientes=lista_clientes
    )

# =========================================
# CREAR CLIENTE
# =========================================

@app.route('/clientes/crear', methods=['GET', 'POST'])
def crear_cliente():

    if request.method == 'POST':

        nuevo_cliente = Cliente(

            cedula=request.form['cedula'],
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            telefono=request.form['telefono'],
            direccion=request.form['direccion'],
            correo=request.form['correo']

        )

        db.session.add(nuevo_cliente)
        db.session.commit()

        return redirect('/clientes')

    return render_template('clientes/crear_cliente.html')

# =========================================
# EDITAR CLIENTE
# =========================================

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':

        cliente.cedula = request.form['cedula']
        cliente.nombre = request.form['nombre']
        cliente.apellido = request.form['apellido']
        cliente.telefono = request.form['telefono']
        cliente.direccion = request.form['direccion']
        cliente.correo = request.form['correo']

        db.session.commit()

        return redirect('/clientes')

    return render_template(
        'clientes/editar_cliente.html',
        cliente=cliente
    )

# =========================================
# ELIMINAR CLIENTE
# =========================================

@app.route('/clientes/eliminar/<int:id>')
def eliminar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return redirect('/clientes')

# =========================================
# LISTAR EQUIPOS
# =========================================

@app.route('/equipos')
def equipos():

    lista_equipos = Equipo.query.all()

    return render_template(
        'equipos/lista_equipos.html',
        equipos=lista_equipos
    )

# =========================================
# CREAR EQUIPO
# =========================================

@app.route('/equipos/crear', methods=['GET', 'POST'])
def crear_equipo():

    clientes = Cliente.query.all()

    if request.method == 'POST':

        nuevo_equipo = Equipo(

            id_cliente=request.form['id_cliente'],
            tipo_equipo=request.form['tipo_equipo'],
            marca=request.form['marca'],
            modelo=request.form['modelo'],
            numero_serie=request.form['numero_serie'],
            observaciones=request.form['observaciones'],
            estado=request.form['estado']

        )

        db.session.add(nuevo_equipo)
        db.session.commit()

        return redirect('/equipos')

    return render_template(
        'equipos/crear_equipo.html',
        clientes=clientes
    )

# =========================================
# EDITAR EQUIPO
# =========================================

@app.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):

    equipo = Equipo.query.get_or_404(id)

    clientes = Cliente.query.all()

    if request.method == 'POST':

        equipo.id_cliente = request.form['id_cliente']
        equipo.tipo_equipo = request.form['tipo_equipo']
        equipo.marca = request.form['marca']
        equipo.modelo = request.form['modelo']
        equipo.numero_serie = request.form['numero_serie']
        equipo.observaciones = request.form['observaciones']
        equipo.estado = request.form['estado']

        db.session.commit()

        return redirect('/equipos')

    return render_template(
        'equipos/editar_equipo.html',
        equipo=equipo,
        clientes=clientes
    )

# =========================================
# ELIMINAR EQUIPO
# =========================================

@app.route('/equipos/eliminar/<int:id>')
def eliminar_equipo(id):

    equipo = Equipo.query.get_or_404(id)

    db.session.delete(equipo)
    db.session.commit()

    return redirect('/equipos')

# =========================================
# INVENTARIO (CATEGORÍAS)
# =========================================

@app.route('/inventario')
def inventario():

    categorias_fijas = [
        "Procesador",
        "Tarjeta Gráfica",
        "Memoria RAM",
        "Almacenamiento",
        "Tarjeta Madre",
        "Fuente de Poder",
        "Periféricos",
        "Accesorios",
        "Pantallas",
        "Otros"
    ]

    categorias = []

    for nombre in categorias_fijas:

        total = Inventario.query.filter_by(
            categoria=nombre
        ).count()

        categorias.append({
            "categoria": nombre,
            "total": total
        })

    return render_template(
        "inventario/lista_inventario.html",
        categorias=categorias
    )

# =========================================
# PRODUCTOS DE UNA CATEGORÍA
# =========================================

@app.route('/inventario/categoria/<categoria>')
def productos_categoria(categoria):

    productos = Inventario.query.filter_by(
        categoria=categoria
    ).order_by(
        Inventario.marca,
        Inventario.nombre_producto
    ).all()

    total_productos = len(productos)

    stock_bajo = sum(1 for p in productos if p.stock <= 3)

    valor_total = sum(p.stock * p.precio for p in productos)

    return render_template(
        'inventario/productos_categoria.html',
        categoria=categoria,
        productos=productos,
        total_productos=total_productos,
        stock_bajo=stock_bajo,
        valor_total=valor_total
    )

# =========================================
# CREAR PRODUCTO
# =========================================

@app.route('/inventario/crear', methods=['GET', 'POST'])
def crear_producto():

    categoria = request.args.get('categoria')

    if request.method == 'POST':

        nuevo_producto = Inventario(

            nombre_producto=request.form['nombre_producto'],
            marca=request.form['marca'],
            descripcion=request.form['descripcion'],
            stock=int(request.form['stock']),
            precio=float(request.form['precio']),
            categoria=request.form['categoria'],
            fecha_registro=date.today()

        )

        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(f"/inventario/categoria/{request.form['categoria']}")

    return render_template(
        'inventario/crear_producto.html',
        categoria=categoria
    )

# =========================================
# EDITAR PRODUCTO
# =========================================

@app.route('/inventario/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    producto = Inventario.query.get_or_404(id)

    if request.method == 'POST':

        producto.nombre_producto = request.form['nombre_producto']
        producto.marca = request.form['marca']
        producto.descripcion = request.form['descripcion']
        producto.stock = int(request.form['stock'])
        producto.precio = float(request.form['precio'])
        producto.categoria = request.form['categoria']

        db.session.commit()

        return redirect(f"/inventario/categoria/{producto.categoria}")

    return render_template(
        'inventario/editar_producto.html',
        producto=producto
    )

# =========================================
# LISTAR USUARIOS
# =========================================

@app.route('/usuarios')
def usuarios():

    lista_usuarios = Usuario.query.all()

    return render_template(
        'usuarios/lista_usuarios.html',
        usuarios=lista_usuarios
    )


# =========================================
# CREAR USUARIO
# =========================================

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():

    if request.method == 'POST':

        nuevo_usuario = Usuario(

            nombre=request.form['nombre'],
            usuario=request.form['usuario'],
            correo=request.form['correo'],
            password=request.form['password'],
            rol=request.form['rol'],
            fecha_creacion=date.today()

        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect('/usuarios')

    return render_template('usuarios/crear_usuario.html')

# =========================================
# EDITAR USUARIO
# =========================================

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':

        usuario.nombre = request.form['nombre']
        usuario.usuario = request.form['usuario']
        usuario.correo = request.form['correo']
        usuario.password = request.form['password']
        usuario.rol = request.form['rol']

        db.session.commit()

        return redirect('/usuarios')

    return render_template(
        'usuarios/editar_usuario.html',
        usuario=usuario
    )


# =========================================
# ELIMINAR USUARIO
# =========================================

@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return redirect('/usuarios')
# =========================================

if __name__ == '__main__':
    app.run(debug=True)