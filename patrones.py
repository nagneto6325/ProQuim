# PROQUIM - PATRONES DE DISENO
# NOTA PARA MI: Todos los patrones estan aqui para que sea mas facil

from data.mock_data import INCOMPATIBILIDADES
from abc import ABC, abstractmethod

# PATRON SINGLETON - Creacional
# NOTA: Solo una instancia de la base de datos en toda la app

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("[Singleton] Creando instancia UNICA")
            cls._instance = super().__new__(cls)
            cls._instance._inicializado = False
        return cls._instance
    
    def __init__(self):
        if not self._inicializado:
            from data.mock_data import recetas, inventario, ordenes_produccion, usuarios
            self.recetas = recetas
            self.inventario = inventario
            self.ordenes = ordenes_produccion
            self.usuarios = usuarios
            self._inicializado = True


# PATRON FACTORY METHOD - Creacional

class Reporte(ABC):
    def __init__(self, datos):
        self.datos = datos
    @abstractmethod
    def generar(self): pass
    @abstractmethod
    def get_nombre(self): pass

class ReporteProduccion(Reporte):
    def generar(self):
        ordenes = self.datos.get("ordenes", [])
        total = len(ordenes)
        completadas = len([o for o in ordenes if o.get("estado") == "Completada"])
        return {"titulo": "Produccion", "total": total, "completadas": completadas, 
                "pendientes": total - completadas, "eficiencia": (completadas/total*100) if total>0 else 0}
    def get_nombre(self): return "Produccion"

class ReporteInventario(Reporte):
    def generar(self):
        inv = self.datos.get("inventario", [])
        criticos = [i for i in inv if i.get("cantidad",0) < i.get("stock_minimo",0)]
        return {"titulo": "Inventario", "total_items": len(inv), "items_criticos": len(criticos)}
    def get_nombre(self): return "Inventario"

class ReporteFactory:
    @staticmethod
    def crear(tipo, datos):
        if tipo == "produccion": return ReporteProduccion(datos)
        if tipo == "inventario": return ReporteInventario(datos)
        raise ValueError(f"Tipo no soportado: {tipo}")


# PATRON OBSERVER - Comportamiento

class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento, datos): pass

class AlertasStock(Observador):
    def actualizar(self, evento, datos):
        if evento == "stock_bajo":
            print(f"[Observer] ALERTA: {datos['nombre']} tiene stock bajo ({datos['cantidad']})")
            return f"⚠️ {datos['nombre']}: reabastecer"

class LoggerSistema(Observador):
    def actualizar(self, evento, datos):
        print(f"[Observer] LOG: {evento} - {datos}")
        return None

class InventarioObservable:
    def __init__(self):
        self._observadores = []
    def agregar(self, obs): self._observadores.append(obs)
    def notificar(self, evento, datos):
        for obs in self._observadores:
            obs.actualizar(evento, datos)
    def verificar(self, item):
        if item["cantidad"] < item["stock_minimo"]:
            self.notificar("stock_bajo", {"nombre": item["nombre"], "cantidad": item["cantidad"]})


# PATRON STRATEGY - Comportamiento

class EstrategiaValidacion(ABC):
    @abstractmethod
    def validar(self, ingredientes): pass

class ValidacionBasica(EstrategiaValidacion):
    def validar(self, ingredientes):
        nombres = [i["nombre"] for i in ingredientes]
        for ing1, ing2 in INCOMPATIBILIDADES:
            if ing1 in nombres and ing2 in nombres:
                return {"compatible": False, "mensaje": f"INCOMPATIBLE: {ing1} con {ing2}"}
        return {"compatible": True, "mensaje": "Compatible"}

class ValidacionGramaje(EstrategiaValidacion):
    def validar(self, ingredientes):
        res = ValidacionBasica().validar(ingredientes)
        if not res["compatible"]: return res
        total = sum(i["gramos"] for i in ingredientes)
        if total != 1000:
            return {"compatible": False, "mensaje": f"Gramaje incorrecto: {total}g (deben ser 1000g)"}
        return {"compatible": True, "mensaje": "Gramaje correcto"}

class ValidacionCompleta(EstrategiaValidacion):
    def validar(self, ingredientes):
        res = ValidacionBasica().validar(ingredientes)
        if not res["compatible"]: return res
        activos = [i for i in ingredientes if i["gramos"] > 100]
        if len(activos) > 3:
            return {"compatible": False, "mensaje": "Demasiados quimicos activos (max 3)"}
        agua = next((i["gramos"] for i in ingredientes if i["nombre"] == "Agua Destilada"), 0)
        otros = sum(i["gramos"] for i in ingredientes if i["nombre"] != "Agua Destilada")
        if otros > agua:
            return {"compatible": False, "mensaje": "Proporcion peligrosa: mas quimicos que agua"}
        return {"compatible": True, "mensaje": "Validacion completa OK"}

class ValidadorQuimico:
    def __init__(self, estrategia=None):
        self._estrategia = estrategia or ValidacionBasica()
    def set_estrategia(self, estrategia): self._estrategia = estrategia
    def validar(self, ingredientes): return self._estrategia.validar(ingredientes)


# PATRON DECORATOR - Estructural

class ReporteBase(ABC):
    @abstractmethod
    def generar(self): pass
    @abstractmethod
    def get_datos(self): pass

class ReporteSimple(ReporteBase):
    def __init__(self, datos): self.datos = datos
    def generar(self): return self.datos
    def get_datos(self): return self.datos

class DecoradorReporte(ReporteBase):
    def __init__(self, reporte): self._reporte = reporte
    def generar(self): return self._reporte.generar()
    def get_datos(self): return self._reporte.get_datos()

class ExportablePDF(DecoradorReporte):
    def exportar_pdf(self):
        datos = self._reporte.get_datos()
        return f"PDF generado: {datos.get('titulo', 'Reporte')}.pdf"
    def generar(self):
        r = self._reporte.generar()
        r["exportable_pdf"] = True
        return r

class ExportableExcel(DecoradorReporte):
    def exportar_excel(self):
        datos = self._reporte.get_datos()
        return f"Excel generado: {datos.get('titulo', 'Reporte')}.xlsx"
    def generar(self):
        r = self._reporte.generar()
        r["exportable_excel"] = True
        return r

def crear_reporte_con_exportaciones(datos, pdf=True, excel=True):
    r = ReporteSimple(datos)
    if pdf: r = ExportablePDF(r)
    if excel: r = ExportableExcel(r)
    return r