# init_db.py
# NOTA: Script para inicializar la base de datos con datos iniciales

from app import app, db
from db import Usuario, Receta, Ingrediente, RecetaIngrediente, OrdenProduccion
from data.mock_data import recetas, inventario, ordenes_produccion, usuarios

def inicializar_bd():
    """Crea la BD y carga los datos iniciales"""
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("[BD] Tablas creadas")
        
        # Cargar usuarios
        if Usuario.query.first() is None:
            for user in usuarios:
                nuevo_usuario = Usuario(
                    username=user['username'],
                    password=user['password'],
                    rol=user['rol']
                )
                db.session.add(nuevo_usuario)
            db.session.commit()
            print(f"[BD] {len(usuarios)} usuarios cargados")
        
        # Cargar ingredientes del inventario
        if Ingrediente.query.first() is None:
            for item in inventario:
                nuevo_ingrediente = Ingrediente(
                    nombre=item['nombre'],
                    cantidad=item['cantidad'],
                    stock_minimo=item['stock_minimo'],
                    unidad=item['unidad']
                )
                db.session.add(nuevo_ingrediente)
            db.session.commit()
            print(f"[BD] {len(inventario)} ingredientes cargados")
        
        # Cargar recetas
        if Receta.query.first() is None:
            for receta in recetas:
                nueva_receta = Receta(
                    nombre=receta['nombre'],
                    categoria=receta['categoria'],
                    rendimiento=receta['rendimiento']
                )
                db.session.add(nueva_receta)
                db.session.flush()  # Obtener el ID
                
                # Cargar ingredientes de la receta
                for ing in receta['ingredientes']:
                    ingrediente = Ingrediente.query.filter_by(nombre=ing['nombre']).first()
                    if ingrediente:
                        receta_ing = RecetaIngrediente(
                            receta_id=nueva_receta.id,
                            ingrediente_id=ingrediente.id,
                            gramos=ing['gramos']
                        )
                        db.session.add(receta_ing)
            
            db.session.commit()
            print(f"[BD] {len(recetas)} recetas cargadas con ingredientes")
        
        # Cargar órdenes de producción
        if OrdenProduccion.query.first() is None:
            for orden in ordenes_produccion:
                nueva_orden = OrdenProduccion(
                    receta_id=orden['receta_id'],
                    cantidad_producir=orden['cantidad_producir'],
                    estado=orden['estado'],
                    lote_produccion=orden['trazabilidad'].get('lote_produccion') if orden['trazabilidad'] else None
                )
                db.session.add(nueva_orden)
            db.session.commit()
            print(f"[BD] {len(ordenes_produccion)} órdenes de producción cargadas")
        
        print("[BD] ✅ Base de datos inicializada correctamente")

if __name__ == '__main__':
    inicializar_bd()
