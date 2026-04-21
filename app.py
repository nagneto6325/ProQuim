# app.py
# NOTA: Este es el servidor principal. Para iniciar: python app.py
# Las rutas controlan que ve cada usuario
# IMPORTANTE: El login es falso - cualquier usuario entra sin verificar contraseña

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from data.mock_data import recetas, inventario, ordenes_produccion, usuarios
from patrones import (
    DatabaseConnection, ReporteFactory, InventarioObservable, 
    AlertasStock, LoggerSistema, ValidadorQuimico, 
    ValidacionBasica, ValidacionGramaje, ValidacionCompleta,
    crear_reporte_con_exportaciones
)

app = Flask(__name__)
app.secret_key = "proquim_secret_key_2026"
# NOTA: Cambiar esta clave en produccion

# PATRON SINGLETON - Base de datos unica
db = DatabaseConnection()

# PATRON OBSERVER - Sistema de alertas
observable = InventarioObservable()
observable.agregar(AlertasStock())
observable.agregar(LoggerSistema())

# PATRON STRATEGY - Validador quimico (se puede cambiar en tiempo real)
validador = ValidadorQuimico(ValidacionBasica())


# ============================================
# RUTA DE LOGIN (SIN VERIFICACION REAL)
# ============================================
# NOTA: Este login NO valida contraseña. Cualquier usuario entra.
# Solo para demostracion de patrones de diseno

@app.route('/')
def index():
    # Redirige al login por defecto
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # IMPORTANTE: NO verifico nada - cualquier usuario entra
        username = request.form.get('username', 'demo')
        rol = request.form.get('rol', 'Administrador')
        
        # Guardo en sesion (opcional, para mostrar el nombre)
        session['user'] = username
        session['rol'] = rol
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # NOTA: Si no hay sesion, igual entra (pero mostramos demo)
    user = session.get('user', 'Demo')
    rol = session.get('rol', 'Administrador')
    
    # PATRON OBSERVER - Verificar stock al cargar dashboard
    for item in inventario:
        observable.verificar(item)
    
    alertas = len([i for i in inventario if i['cantidad'] < i['stock_minimo']])
    
    return render_template('dashboard.html', 
                         user=user,
                         rol=rol,
                         total_recetas=len(recetas),
                         ordenes_activas=len([o for o in ordenes_produccion if o['estado'] == 'Pendiente']),
                         alertas_stock=alertas)

@app.route('/recetas')
def recetas_page():
    # Muestra todas las recetas tecnicas
    return render_template('recetas.html', recetas=recetas)

@app.route('/validar_receta', methods=['POST'])
def validar_receta():
    # PATRON STRATEGY - Valida compatibilidad quimica
    data = request.get_json()
    ingredientes = data.get('ingredientes', [])
    resultado = validador.validar(ingredientes)
    return jsonify(resultado)

@app.route('/cambiar_validacion', methods=['POST'])
def cambiar_validacion():
    # NOTA: Permite cambiar la estrategia de validacion en tiempo real
    data = request.get_json()
    tipo = data.get('tipo', 'basica')
    if tipo == 'gramaje':
        validador.set_estrategia(ValidacionGramaje())
    elif tipo == 'completa':
        validador.set_estrategia(ValidacionCompleta())
    else:
        validador.set_estrategia(ValidacionBasica())
    return jsonify({"mensaje": f"Estrategia cambiada a: {tipo}"})

@app.route('/ordenes')
def ordenes_page():
    # Muestra las ordenes de produccion
    return render_template('ordenes_produccion.html', ordenes=ordenes_produccion, recetas=recetas)

@app.route('/crear_orden', methods=['POST'])
def crear_orden():
    # NOTA: Crea una nueva orden y la agrega a la lista
    data = request.get_json()
    receta_id = data.get('receta_id')
    cantidad = data.get('cantidad')
    
    receta = next((r for r in recetas if r['id'] == receta_id), None)
    if not receta:
        return jsonify({"error": "Receta no encontrada"}), 404
    
    nueva_orden = {
        "id": len(ordenes_produccion) + 1,
        "receta_id": receta_id,
        "receta_nombre": receta['nombre'],
        "cantidad_producir": cantidad,
        "estado": "Pendiente",
        "fecha": "2026-04-19",
        "trazabilidad": None
    }
    ordenes_produccion.append(nueva_orden)
    
    return jsonify({"mensaje": f"Orden creada: {receta['nombre']} - {cantidad}kg", "orden": nueva_orden})

@app.route('/inventario')
def inventario_page():
    # PATRON OBSERVER - Verificar stock al cargar inventario
    for item in inventario:
        observable.verificar(item)
    return render_template('inventario.html', inventario=inventario)

@app.route('/actualizar_stock', methods=['POST'])
def actualizar_stock():
    # NOTA: Actualiza cantidad de un material y dispara alertas si es necesario
    data = request.get_json()
    item_id = data.get('id')
    nueva_cantidad = data.get('cantidad')
    
    for item in inventario:
        if item['id'] == item_id:
            item['cantidad'] = nueva_cantidad
            observable.verificar(item)  # Observer: dispara alerta si bajo stock
            return jsonify({"mensaje": f"Stock actualizado: {item['nombre']} = {nueva_cantidad} {item['unidad']}"})
    
    return jsonify({"error": "Item no encontrado"}), 404

@app.route('/reportes')
def reportes_page():
    # PATRON FACTORY METHOD + PATRON DECORATOR
    # Factory crea el reporte base, Decorator agrega exportaciones
    total = len(ordenes_produccion)
    completadas = len([o for o in ordenes_produccion if o['estado'] == 'Completada'])
    eficiencia = (completadas / total * 100) if total > 0 else 0
    
    factory = ReporteFactory()
    reporte = factory.crear("produccion", {"ordenes": ordenes_produccion})
    datos_reporte = reporte.generar()
    
    # PATRON DECORATOR - Agrega exportacion a PDF y Excel
    reporte_con_export = crear_reporte_con_exportaciones(datos_reporte, pdf=True, excel=True)
    reporte_final = reporte_con_export.generar()
    
    return render_template('reportes.html', 
                         total_ordenes=total,
                         ordenes_completadas=completadas,
                         eficiencia=round(eficiencia, 1),
                         reporte=reporte_final)

@app.route('/exportar_pdf')
def exportar_pdf():
    # NOTA: Exporta el reporte a PDF (simulado)
    datos = {"titulo": "Reporte Produccion", "total": len(ordenes_produccion)}
    reporte = crear_reporte_con_exportaciones(datos, pdf=True, excel=False)
    if hasattr(reporte, 'exportar_pdf'):
        return jsonify({"mensaje": reporte.exportar_pdf()})
    return jsonify({"mensaje": "Error"})

@app.route('/exportar_excel')
def exportar_excel():
    # NOTA: Exporta el reporte a Excel (simulado)
    datos = {"titulo": "Reporte Produccion", "total": len(ordenes_produccion)}
    reporte = crear_reporte_con_exportaciones(datos, pdf=False, excel=True)
    if hasattr(reporte, 'exportar_excel'):
        return jsonify({"mensaje": reporte.exportar_excel()})
    return jsonify({"mensaje": "Error"})

@app.route('/configuracion')
def configuracion_page():
    # NOTA: Asegurarse de que usuarios existe y se pasa correctamente
    from data.mock_data import usuarios
    return render_template('configuracion.html', usuarios=usuarios, rol=session.get('rol', 'Administrador'))

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    # NOTA: Agrega un nuevo usuario a la lista
    data = request.get_json()
    nuevo_usuario = {
        "username": data.get('username'),
        "password": data.get('password'),
        "rol": data.get('rol')
    }
    usuarios.append(nuevo_usuario)
    return jsonify({"mensaje": f"Usuario creado: {nuevo_usuario['username']}"})

@app.route('/logout')
def logout():
    # NOTA: Cierra la sesion y borra los datos del usuario
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    # NOTA: debug=True solo para desarrollo. En produccion poner debug=False
    print("\n" + "="*60)
    print("PROQUIM - Sistema de Gestion de Produccion")
    print("="*60)
    print("Singleton - Base de datos unica")
    print("Factory Method - Creacion de reportes")
    print("Observer - Alertas de inventario")
    print("Strategy - Validacion quimica")
    print("Decorator - Exportacion de reportes")
    print("="*60)
    print("IMPORTANTE: LOGIN FALSO - CUALQUIER USUARIO ENTRA")
    print("Servidor: http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(debug=True)