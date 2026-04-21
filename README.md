# ProQuim - Mi proyecto de gestion

## Que es esto

Es un sistema que hicimos para gestionar recetas, inventario y ordenes de produccion. Lo hicimos para la materia de Diseño de Sistemas de Informacion. Tiene validacion quimica y alertas de stock.

## Como se corre

1. Tener Python instalado
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual: `.\venv\Scripts\Activate.ps1` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Inicializar la base de datos: `python init_db.py` (primera vez)
6. Ejecutar: `python app.py`
7. Abrir http://127.0.0.1:5000

## Base de datos

Ahora usamos **SQLite** con Flask-SQLAlchemy. La BD se guarda en `proquim.db`.

**Para resetear la BD:** Borra el archivo `proquim.db` y ejecuta `python init_db.py`

### Modelos de datos:
- `Usuario` - usuarios del sistema
- `Ingrediente` - materiales del inventario
- `Receta` - recetas técnicas
- `RecetaIngrediente` - relación muchos-a-muchos
- `OrdenProduccion` - órdenes de trabajo

## Login

Cualquier usuario y contraseña funciona. No valida nada porque es demo. Hay un selector de rol.

## Que tiene

- Recetas tecnicas con ingredientes y gramajes
- Validacion de compatibilidad quimica (no mezclar alcohol con cloro)
- Ordenes de produccion
- Inventario con stock minimo y alertas
- Trazabilidad de lotes
- Reportes basicos
- **Base de datos persistente en SQLite**

## Patrones que usamos

- Singleton: para la base de datos (una sola instancia)
- Factory: para crear reportes
- Observer: para las alertas de stock bajo
- Strategy: para cambiar el tipo de validacion quimica
- Decorator: para agregar exportacion a PDF/Excel a los reportes

## Estructura

- `app.py` - el servidor con las rutas
- `db.py` - modelos SQLAlchemy
- `init_db.py` - script para inicializar la BD
- `patrones.py` - todos los patrones de diseño
- `data/mock_data.py` - datos iniciales
- `templates/` - los html
- `static/css/` - estilos
- `static/js/` - javascript basico

## Cosas que no alcance

- Login verdadero
- Graficos bonitos
- Exportar PDF/Excel de verdad (solo simula)

## Notas

Esto fue un prototipo para la materia. Si se cierra el servidor se pierden los datos porque no hay base de datos real.

Hecho por: Grupo 6
Fecha: Abril 2026