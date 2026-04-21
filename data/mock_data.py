# data/mock_data.py
# NOTA: Todos los datos de prueba estan aqui
# Para agregar mas recetas o ingredientes, modificar estas listas

recetas = [
    {
        "id": 1,
        "nombre": "Detergente Liquido Neutro",
        "categoria": "Limpieza",
        "rendimiento": 1000,
        "ingredientes": [
            {"nombre": "Acido Sulfonico", "gramos": 150},
            {"nombre": "Hidroxido de Sodio", "gramos": 50},
            {"nombre": "Agua Destilada", "gramos": 800}
        ]
    },
    {
        "id": 2,
        "nombre": "Desinfectante con Cloro",
        "categoria": "Desinfeccion",
        "rendimiento": 1000,
        "ingredientes": [
            {"nombre": "Hipoclorito de Sodio", "gramos": 200},
            {"nombre": "Agua Destilada", "gramos": 800}
        ]
    },
    {
        "id": 3,
        "nombre": "Limpiador Multiusos",
        "categoria": "Multiusos",
        "rendimiento": 1000,
        "ingredientes": [
            {"nombre": "Alcohol Etilico", "gramos": 300},
            {"nombre": "Amoniaco", "gramos": 100},
            {"nombre": "Agua Destilada", "gramos": 600}
        ]
    }
]

inventario = [
    {"id": 1, "nombre": "Acido Sulfonico", "cantidad": 5000, "stock_minimo": 1000, "unidad": "kg"},
    {"id": 2, "nombre": "Hidroxido de Sodio", "cantidad": 2000, "stock_minimo": 500, "unidad": "kg"},
    {"id": 3, "nombre": "Agua Destilada", "cantidad": 10000, "stock_minimo": 2000, "unidad": "L"},
    {"id": 4, "nombre": "Hipoclorito de Sodio", "cantidad": 800, "stock_minimo": 1000, "unidad": "L"},
    {"id": 5, "nombre": "Alcohol Etilico", "cantidad": 3000, "stock_minimo": 800, "unidad": "L"},
    {"id": 6, "nombre": "Amoniaco", "cantidad": 400, "stock_minimo": 500, "unidad": "L"}
]

ordenes_produccion = [
    {
        "id": 1,
        "receta_id": 1,
        "receta_nombre": "Detergente Liquido Neutro",
        "cantidad_producir": 500,
        "estado": "Completada",
        "fecha": "2026-04-10",
        "trazabilidad": {"lote_produccion": "LP-2024-001"}
    },
    {
        "id": 2,
        "receta_id": 2,
        "receta_nombre": "Desinfectante con Cloro",
        "cantidad_producir": 1000,
        "estado": "Pendiente",
        "fecha": "2026-04-12",
        "trazabilidad": None
    }
]

# data/mock_data.py - solo la parte de usuarios actualizada

usuarios = [
    {"username": "admin", "password": "admin123", "rol": "Administrador"},
    {"username": "jefe", "password": "jefe123", "rol": "Jefe de Produccion"},
    {"username": "operario", "password": "operario123", "rol": "Operario"},
    {"username": "gerente", "password": "gerente123", "rol": "Gerente"},
    {"username": "inventario", "password": "inv123", "rol": "Responsable de Inventario"}
]
# NOTA: Matriz de incompatibilidad quimica para el patron STRATEGY
# Si dos quimicos estan en la misma receta, se bloquea automaticamente
INCOMPATIBILIDADES = [
    ("Alcohol Etilico", "Hipoclorito de Sodio"),
    ("Amoniaco", "Acido Clorhidrico"),
]