from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

app = Flask(__name__)
app.secret_key = "sistema_tecnico_2026"
serializer = URLSafeTimedSerializer(app.secret_key)
# =========================================
# CONFIGURACIÓN DE CORREO GMAIL
# =========================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'pruebatesis7@gmail.com'
app.config['MAIL_PASSWORD'] = 'mtcvngckpnbdzhzk'

mail = Mail(app)
# =========================================
# CONEXION MYSQL
# =========================================

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sistema_tecnico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# =========================================
# PROTEGER RUTAS
# =========================================

def login_requerido(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        if 'id_usuario' not in session:

            return redirect('/login')

        return f(*args, **kwargs)

    return decorated_function


# =========================================
# PROTEGER RUTAS DE ADMINISTRADOR
# =========================================

def admin_requerido(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        # Primero verificar que haya iniciado sesión

        if 'id_usuario' not in session:

            return redirect('/login')

        # Verificar que sea administrador

        if session.get('rol') != 'Administrador':

            flash(
                'No tienes permisos para acceder a esta sección.'
            )

            return redirect('/')

        return f(*args, **kwargs)

    return decorated_function
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

    nombre = db.Column(db.String(100), nullable=False)

    usuario = db.Column(db.String(100), unique=True, nullable=False)

    correo = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    rol = db.Column(db.String(50), nullable=False)

    fecha_creacion = db.Column(db.Date)

    def establecer_password(self, password):
        self.password = generate_password_hash(password)

    def verificar_password(self, password):
        return check_password_hash(self.password, password)
    
# =========================================
# MODELO SERVICIOS TÉCNICOS
# =========================================

class ServicioTecnico(db.Model):

    __tablename__ = 'servicios_tecnicos'

    id_servicio = db.Column(db.Integer, primary_key=True)

    id_equipo = db.Column(
        db.Integer,
        db.ForeignKey('equipos.id_equipo')
    )

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usuario')
    )

    falla_reportada = db.Column(db.Text)

    diagnostico = db.Column(db.Text)

    solucion = db.Column(db.Text)

    estado = db.Column(db.String(50))

    fecha_ingreso = db.Column(db.Date)

    fecha_entrega = db.Column(db.Date)

    costo = db.Column(db.Numeric(10,2))

    equipo = db.relationship(
        'Equipo',
        backref='servicios'
    )

    usuario = db.relationship(
        'Usuario',
        backref='servicios'
    )
# =========================================
# MODELO DETALLE SERVICIO
# =========================================

class DetalleServicio(db.Model):

    __tablename__ = 'detalle_servicio'

    id_detalle = db.Column(db.Integer, primary_key=True)

    id_servicio = db.Column(
        db.Integer,
        db.ForeignKey('servicios_tecnicos.id_servicio'),
        nullable=False
    )

    id_producto = db.Column(
        db.Integer,
        db.ForeignKey('inventario.id_producto'),
        nullable=False
    )

    cantidad = db.Column(db.Integer)

    subtotal = db.Column(db.Numeric(10,2))

    servicio = db.relationship(
        'ServicioTecnico',
        backref='detalles'
    )

    producto = db.relationship(
        'Inventario',
        backref='detalles'
    )
# =========================================
# RUTA INICIO
# =========================================

@app.route('/')
@login_requerido
def inicio():

    if 'id_usuario' not in session:
        return redirect('/login')

    return render_template('index.html')

# =========================================
# LISTAR CLIENTES
# =========================================

@app.route('/clientes')
@login_requerido
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
@login_requerido
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
@login_requerido
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
@login_requerido
def eliminar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return redirect('/clientes')

# =========================================
# LISTAR EQUIPOS
# =========================================

@app.route('/equipos')
@login_requerido
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
@login_requerido
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
@login_requerido
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
@login_requerido
def eliminar_equipo(id):

    equipo = Equipo.query.get_or_404(id)

    db.session.delete(equipo)
    db.session.commit()

    return redirect('/equipos')

# =========================================
# INVENTARIO (CATEGORÍAS)
# =========================================

@app.route('/inventario')
@login_requerido
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
@login_requerido
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
@login_requerido
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
@login_requerido
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
@admin_requerido
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
@admin_requerido
def crear_usuario():

    if request.method == 'POST':

        nuevo_usuario = Usuario(

            nombre=request.form['nombre'],

            usuario=request.form['usuario'],

            correo=request.form['correo'],

            rol=request.form['rol'],

            fecha_creacion=date.today()

        )

        # Guardar contraseña cifrada

        nuevo_usuario.establecer_password(
            request.form['password']
        )

        db.session.add(nuevo_usuario)

        db.session.commit()

        return redirect('/usuarios')

    return render_template(
        'usuarios/crear_usuario.html'
    )


# =========================================
# EDITAR USUARIO
# =========================================

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@admin_requerido
def editar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':

        usuario.nombre = request.form['nombre']

        usuario.usuario = request.form['usuario']

        usuario.correo = request.form['correo']

        usuario.rol = request.form['rol']

        # Solo cambiar contraseña si se escribió una nueva

        if request.form['password']:

            usuario.establecer_password(
                request.form['password']
            )

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
@admin_requerido
def eliminar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)

    db.session.commit()

    return redirect('/usuarios')
# =========================================
# RUTAS SERVICIOS TÉCNICOS
# =========================================

@app.route('/servicios')
@login_requerido
def servicios():

    servicios = ServicioTecnico.query.all()

    return render_template(
        'servicios/lista_servicios.html',
        servicios=servicios
    )
# =========================================
# CREAR SERVICIO TÉCNICO
# =========================================

@app.route('/servicios/crear', methods=['GET', 'POST'])
@login_requerido
def crear_servicio():

    equipos = Equipo.query.all()

    usuarios = Usuario.query.all()

    if request.method == 'POST':

        nuevo_servicio = ServicioTecnico(

            id_equipo=request.form['id_equipo'],

            id_usuario=request.form['id_usuario'],

            falla_reportada=request.form['falla_reportada'],

            diagnostico=request.form['diagnostico'],

            solucion=request.form['solucion'],

            estado=request.form['estado'],

            fecha_ingreso=request.form['fecha_ingreso'],

            fecha_entrega=request.form['fecha_entrega'],

            costo=request.form['costo']

        )

        db.session.add(nuevo_servicio)

        db.session.commit()

        return redirect('/servicios')

    return render_template(

        'servicios/crear_servicio.html',

        equipos=equipos,

        usuarios=usuarios

    )
# =========================================
# EDITAR SERVICIO TÉCNICO
# =========================================

@app.route('/servicios/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar_servicio(id):

    servicio = ServicioTecnico.query.get_or_404(id)

    equipos = Equipo.query.all()

    usuarios = Usuario.query.all()

    if request.method == 'POST':

        servicio.id_equipo = request.form['id_equipo']

        servicio.id_usuario = request.form['id_usuario']

        servicio.falla_reportada = request.form['falla_reportada']

        servicio.diagnostico = request.form['diagnostico']

        servicio.solucion = request.form['solucion']

        servicio.estado = request.form['estado']

        servicio.fecha_ingreso = request.form['fecha_ingreso']

        servicio.fecha_entrega = request.form['fecha_entrega']

        servicio.costo = request.form['costo']

        db.session.commit()

        return redirect('/servicios')

    return render_template(
        'servicios/editar_servicio.html',
        servicio=servicio,
        equipos=equipos,
        usuarios=usuarios
    )
# =========================================
# VER SERVICIO
# =========================================

@app.route('/servicios/ver/<int:id>')
@login_requerido
def ver_servicio(id):

    servicio = ServicioTecnico.query.get_or_404(id)

    detalles = DetalleServicio.query.filter_by(
        id_servicio=id
    ).all()

    total_productos = sum(
        float(detalle.subtotal)
        for detalle in detalles
    )

    total_pagar = float(servicio.costo) + total_productos

    return render_template(

        'servicios/ver_servicio.html',

        servicio=servicio,

        detalles=detalles,

        total_productos=total_productos,

        total_pagar=total_pagar

    )
# =========================================
# AGREGAR PRODUCTO A SERVICIO
# =========================================

@app.route('/servicios/<int:id>/agregar_producto', methods=['GET', 'POST'])
@login_requerido
def agregar_producto(id):

    servicio = ServicioTecnico.query.get_or_404(id)

    productos = Inventario.query.all()

    if request.method == 'POST':

        producto = Inventario.query.get(request.form['id_producto'])

        cantidad = int(request.form['cantidad'])

        if cantidad > producto.stock:

            return "Stock insuficiente"

        subtotal = cantidad * float(producto.precio)

        detalle = DetalleServicio(

            id_servicio=id,

            id_producto=producto.id_producto,

            cantidad=cantidad,

            subtotal=subtotal

        )

        producto.stock -= cantidad

        db.session.add(detalle)

        db.session.commit()

        return redirect(f'/servicios/ver/{id}')

    return render_template(

        'servicios/agregar_producto.html',

        servicio=servicio,

        productos=productos

    )
# =========================================
# LOGIN
# =========================================

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        usuario = Usuario.query.filter_by(
            usuario=request.form['usuario']
        ).first()

        if usuario and usuario.verificar_password(
            request.form['password']
        ):

            session['id_usuario'] = usuario.id_usuario
            session['nombre'] = usuario.nombre
            session['rol'] = usuario.rol

            return redirect('/')

        flash("Usuario o contraseña incorrectos.")

    return render_template('auth/login.html')

# =========================================
# CERRAR SESIÓN
# =========================================

@app.route('/logout')

def logout():

    session.clear()

    return redirect('/login')
# =========================================
# RECUPERAR CONTRASEÑA
# =========================================

@app.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():

    if request.method == 'POST':

        correo = request.form['correo'].strip().lower()

        usuario = Usuario.query.filter_by(
            correo=correo
        ).first()

        if not usuario or usuario.rol != 'Técnico':

            flash(
                "No se encontró una cuenta de Técnico asociada a ese correo."
            )

            return redirect('/recuperar-password')

        token = serializer.dumps(
            usuario.id_usuario,
            salt='recuperar-password'
        )

        enlace = url_for(
            'restablecer_password',
            token=token,
            _external=True
        )

        mensaje = Message(
            subject='Recuperación de contraseña - Sistema Técnico',
            sender=app.config['MAIL_USERNAME'],
            recipients=[usuario.correo]
        )

        mensaje.body = f"""Hola {usuario.nombre},

Se ha solicitado recuperar la contraseña de tu cuenta en el Sistema de Gestión de Servicio Técnico.

Para establecer una nueva contraseña, abre el siguiente enlace:

{enlace}

Este enlace será válido durante 15 minutos.

Si tú no solicitaste este cambio, puedes ignorar este correo.

Saludos,
Sistema de Gestión de Servicio Técnico
"""

        mail.send(mensaje)

        flash(
            "Si el correo está registrado, recibirás un enlace de recuperación."
        )

        return redirect('/login')

    return render_template(
        'auth/recuperar_password.html'
    )
# =========================================
# RESTABLECER CONTRASEÑA
# =========================================

@app.route('/restablecer-password/<token>', methods=['GET', 'POST'])
def restablecer_password(token):

    try:

        id_usuario = serializer.loads(
            token,
            salt='recuperar-password',
            max_age=900
        )

    except:

        flash(
            "El enlace de recuperación no es válido o ha expirado."
        )

        return redirect('/recuperar-password')

    usuario = Usuario.query.get_or_404(id_usuario)

    if usuario.rol != 'Técnico':

        flash(
            "No tienes permisos para realizar esta acción."
        )

        return redirect('/login')

    if request.method == 'POST':

        password = request.form['password']
        confirmar_password = request.form['confirmar_password']

        if password != confirmar_password:

            flash(
                "Las contraseñas no coinciden."
            )

            return redirect(
                url_for(
                    'restablecer_password',
                    token=token
                )
            )

        if len(password) < 8:

            flash(
                "La contraseña debe tener al menos 8 caracteres."
            )

            return redirect(
                url_for(
                    'restablecer_password',
                    token=token
                )
            )

        usuario.establecer_password(password)

        db.session.commit()

        flash(
            "Contraseña actualizada correctamente."
        )

        return redirect('/login')

    return render_template(
        'auth/restablecer_password.html'
    )
# =========================================
# DASHBOARD ADMINISTRATIVO
# =========================================

@app.route('/dashboard')
@admin_requerido
def dashboard():

    total_clientes = Cliente.query.count()

    total_equipos = Equipo.query.count()

    total_servicios = ServicioTecnico.query.count()

    servicios_pendientes = ServicioTecnico.query.filter(
        ServicioTecnico.estado != 'Entregado'
    ).count()

    total_productos = Inventario.query.count()

    productos_stock_bajo = Inventario.query.filter(
        Inventario.stock <= 3
    ).count()

    ingresos_servicios = db.session.query(
        db.func.coalesce(
            db.func.sum(ServicioTecnico.costo),
            0
        )
    ).scalar()

    ingresos_productos = db.session.query(
        db.func.coalesce(
            db.func.sum(DetalleServicio.subtotal),
            0
        )
    ).scalar()

    ingresos_totales = ingresos_servicios + ingresos_productos

    return render_template(
        'dashboard.html',

        total_clientes=total_clientes,

        total_equipos=total_equipos,

        total_servicios=total_servicios,

        servicios_pendientes=servicios_pendientes,

        total_productos=total_productos,

        productos_stock_bajo=productos_stock_bajo,

        ingresos_servicios=ingresos_servicios,

        ingresos_productos=ingresos_productos,

        ingresos_totales=ingresos_totales
    )
# =========================================
# REPORTES ADMINISTRATIVOS
# =========================================

@app.route('/reportes')
@admin_requerido
def reportes():

    total_clientes = Cliente.query.count()

    total_equipos = Equipo.query.count()

    total_servicios = ServicioTecnico.query.count()

    servicios_pendientes = ServicioTecnico.query.filter(
        ServicioTecnico.estado != 'Entregado'
    ).count()

    total_productos = Inventario.query.count()

    stock_bajo = Inventario.query.filter(
        Inventario.stock <= 3
    ).count()

    ingresos_servicios = db.session.query(
        func.coalesce(func.sum(ServicioTecnico.costo), 0)
    ).scalar()

    total_productos_utilizados = db.session.query(
        func.coalesce(func.sum(DetalleServicio.subtotal), 0)
    ).scalar()

    total_ingresos = (
        float(ingresos_servicios or 0) +
        float(total_productos_utilizados or 0)
    )

    return render_template(
        'reportes/reportes.html',

        total_clientes=total_clientes,
        total_equipos=total_equipos,
        total_servicios=total_servicios,
        servicios_pendientes=servicios_pendientes,
        total_productos=total_productos,
        stock_bajo=stock_bajo,

        ingresos_servicios=float(ingresos_servicios or 0),
        total_productos_utilizados=float(total_productos_utilizados or 0),
        total_ingresos=total_ingresos
    )
# =========================================
# GENERAR REPORTE PDF
# =========================================

@app.route('/reportes/pdf')
@admin_requerido
def reporte_pdf():

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elementos = []

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        'Titulo',
        parent=estilos['Title'],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=20
    )

    subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=estilos['Heading2'],
        fontSize=13,
        spaceBefore=15,
        spaceAfter=10
    )

    normal = estilos['Normal']

    # =========================================
    # TÍTULO
    # =========================================

    elementos.append(
        Paragraph(
            'REPORTE ADMINISTRATIVO',
            titulo
        )
    )

    elementos.append(
        Paragraph(
            'Sistema de Gestión de Servicio Técnico',
            normal
        )
    )

    elementos.append(Spacer(1, 20))

    # =========================================
    # CONSULTAS
    # =========================================

    total_clientes = Cliente.query.count()

    total_equipos = Equipo.query.count()

    total_servicios = ServicioTecnico.query.count()

    servicios_pendientes = ServicioTecnico.query.filter(
        ServicioTecnico.estado != 'Entregado'
    ).count()

    total_productos = Inventario.query.count()

    stock_bajo = Inventario.query.filter(
        Inventario.stock <= 3
    ).count()

    ingresos_servicios = db.session.query(
        func.coalesce(
            func.sum(ServicioTecnico.costo),
            0
        )
    ).scalar()

    ingresos_productos = db.session.query(
        func.coalesce(
            func.sum(DetalleServicio.subtotal),
            0
        )
    ).scalar()

    ingresos_totales = (
        float(ingresos_servicios or 0)
        +
        float(ingresos_productos or 0)
    )

    # =========================================
    # RESUMEN GENERAL
    # =========================================

    elementos.append(
        Paragraph(
            'Resumen General',
            subtitulo
        )
    )

    datos_resumen = [

        ['Concepto', 'Cantidad'],

        ['Clientes registrados', str(total_clientes)],

        ['Equipos registrados', str(total_equipos)],

        ['Servicios técnicos', str(total_servicios)],

        ['Servicios pendientes', str(servicios_pendientes)],

        ['Productos registrados', str(total_productos)],

        ['Productos con stock bajo', str(stock_bajo)]

    ]

    tabla_resumen = Table(
        datos_resumen,
        colWidths=[350, 120]
    )

    tabla_resumen.setStyle(
        TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),

            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

            ('ALIGN', (1, 1), (1, -1), 'CENTER'),

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('TOPPADDING', (0, 0), (-1, -1), 8),

            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)

        ])
    )

    elementos.append(tabla_resumen)

    # =========================================
    # INFORMACIÓN ECONÓMICA
    # =========================================

    elementos.append(
        Paragraph(
            'Información Económica',
            subtitulo
        )
    )

    datos_economicos = [

        ['Concepto', 'Valor'],

        [
            'Ingresos por servicios',
            f'${float(ingresos_servicios or 0):.2f}'
        ],

        [
            'Productos utilizados',
            f'${float(ingresos_productos or 0):.2f}'
        ],

        [
            'Ingresos totales',
            f'${ingresos_totales:.2f}'
        ]

    ]

    tabla_economica = Table(
        datos_economicos,
        colWidths=[350, 120]
    )

    tabla_economica.setStyle(
        TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),

            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),

            ('TOPPADDING', (0, 0), (-1, -1), 8),

            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)

        ])
    )

    elementos.append(tabla_economica)

    elementos.append(Spacer(1, 25))

    elementos.append(
        Paragraph(
            'Reporte generado desde el sistema de gestión de servicio técnico.',
            normal
        )
    )

    # =========================================
    # GENERAR PDF
    # =========================================

    pdf.build(elementos)

    buffer.seek(0)

    from flask import send_file

    return send_file(
        buffer,
        as_attachment=False,
        download_name='reporte_administrativo.pdf',
        mimetype='application/pdf'
    )
# =========================================
# RESPALDO DE BASE DE DATOS
# =========================================

@app.route('/respaldos')
@login_requerido
def respaldos():

    if session.get('rol') != 'Administrador':

        flash("No tienes permisos para acceder a esta sección.")

        return redirect('/')

    return render_template('respaldos.html')
# =========================================
# GENERAR RESPALDO
# =========================================

@app.route('/respaldos/generar')
@login_requerido
def generar_respaldo():

    if session.get('rol') != 'Administrador':

        flash("No tienes permisos para realizar esta acción.")

        return redirect('/')

    import subprocess
    from datetime import datetime
    from flask import send_file
    import os

    mysqldump = r'C:\xampp\mysql\bin\mysqldump.exe'

    carpeta = os.path.join(
        app.root_path,
        'respaldos'
    )

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    fecha = datetime.now().strftime(
        '%Y-%m-%d_%H-%M-%S'
    )

    nombre_archivo = (
        f'respaldo_sistema_tecnico_{fecha}.sql'
    )

    ruta_archivo = os.path.join(
        carpeta,
        nombre_archivo
    )

    comando = [
        mysqldump,
        '-u',
        'root',
        '--result-file=' + ruta_archivo,
        'sistema_tecnico'
    ]

    try:

        subprocess.run(
            comando,
            check=True
        )

    except Exception as e:

        flash(
            f'No se pudo generar el respaldo: {e}'
        )

        return redirect('/respaldos')

    return send_file(
        ruta_archivo,
        as_attachment=True,
        download_name=nombre_archivo
    )
# =========================================

if __name__ == '__main__':
    app.run(debug=True)