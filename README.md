# ProQuim - Mi proyecto de gestion

## Que es esto

Es un sistema que hicimos para gestionar recetas, inventario y ordenes de produccion. Lo hicimos para la materia de Diseño de Sistemas de Informacion. Tiene validacion quimica y alertas de stock.

## Como se corre

1. Tener Python instalado
2. Instalar Flask: pip install flask
3. Ejecutar: python app.py
4. Abrir http://127.0.0.1:5000

## Login

Cualquier usuario y contraseña funciona. No valida nada porque es demo. Hay un selector de rol.

## Que tiene

- Recetas tecnicas con ingredientes y gramajes
- Validacion de compatibilidad quimica (no mezclar alcohol con cloro)
- Ordenes de produccion
- Inventario con stock minimo y alertas
- Trazabilidad de lotes
- Reportes basicos

## Patrones que usamos

- Singleton: para la base de datos (una sola instancia)
- Factory: para crear reportes
- Observer: para las alertas de stock bajo
- Strategy: para cambiar el tipo de validacion quimica
- Decorator: para agregar exportacion a PDF/Excel a los reportes

## Estructura

- app.py - el servidor con las rutas
- patrones.py - todos los patrones de diseño
- data/mock_data.py - datos de prueba
- templates/ - los html
- static/css/ - estilos
- static/js/ - javascript basico

## Cosas que no alcance

- Base de datos real (todo es en memoria)
- Login verdadero
- Graficos bonitos
- Exportar PDF/Excel de verdad (solo simula)

## Notas

Esto fue un prototipo para la materia. Si se cierra el servidor se pierden los datos porque no hay base de datos real.

Hecho por: Grupo 6
Fecha: Abril 2026