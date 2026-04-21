# db.py
# NOTA: Modelos SQLAlchemy para la base de datos SQLite

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ============================================
# MODELO: USUARIOS
# ============================================
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), nullable=False)  # Administrador, Jefe de Produccion, Operario
    
    def __repr__(self):
        return f'<Usuario {self.username}>'


# ============================================
# MODELO: INGREDIENTES
# ============================================
class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)  # Cantidad en stock
    stock_minimo = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(20), nullable=False)  # kg, L, etc
    
    # Relaciones
    receta_ingredientes = db.relationship('RecetaIngrediente', backref='ingrediente', lazy=True)
    
    def __repr__(self):
        return f'<Ingrediente {self.nombre}>'


# ============================================
# MODELO: RECETAS
# ============================================
class Receta(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Limpieza, Desinfeccion, etc
    rendimiento = db.Column(db.Float, nullable=False)  # Cantidad final en ml o kg
    
    # Relaciones
    ingredientes = db.relationship('RecetaIngrediente', backref='receta', lazy=True, cascade='all, delete-orphan')
    ordenes = db.relationship('OrdenProduccion', backref='receta', lazy=True)
    
    def __repr__(self):
        return f'<Receta {self.nombre}>'


# ============================================
# MODELO: RECETA_INGREDIENTE (Tabla intermedia)
# ============================================
class RecetaIngrediente(db.Model):
    __tablename__ = 'receta_ingrediente'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    gramos = db.Column(db.Float, nullable=False)  # Cantidad usada en la receta
    
    def __repr__(self):
        return f'<RecetaIngrediente receta={self.receta_id}, ingrediente={self.ingrediente_id}>'


# ============================================
# MODELO: ORDENES DE PRODUCCION
# ============================================
class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    cantidad_producir = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')  # Pendiente, En Proceso, Completada
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    lote_produccion = db.Column(db.String(50), nullable=True)  # LP-2024-001, etc
    
    def __repr__(self):
        return f'<OrdenProduccion {self.id} - {self.estado}>'
