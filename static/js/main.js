// JavaScript auxiliar para interactividad
console.log('ProQuim Sistema de Gestión - Frontend Python');

// Función global para alertas (demo)
window.verTrazabilidad = function(lote, materias) {
    alert(`Trazabilidad del Lote:\nLote de producción: ${lote}\nLotes de materia prima: ${materias.join(', ')}`);
};

// Validación de stock (simulada)
window.validarStock = function() {
    alert("Validación de stock: Demo - Stock suficiente para producción");
};

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Resaltar alertas de stock bajo en la tabla
    const stockBajos = document.querySelectorAll('.stock-bajo');
    if(stockBajos.length > 0) {
        console.log(`⚠️ ${stockBajos.length} materiales con stock crítico`);
    }
});