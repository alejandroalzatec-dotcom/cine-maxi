
# Manual de Usuario

## Introducción
Este manual describe cómo usar el sistema del **Cinema Universitario** desde Google Colab o localmente.

## Requisitos
- Python 3.10+ (para ejecución local).
- Google Colab (para ejecución en la nube).

## Flujo de uso
1. **Registrar Usuario**: ingresa nombre, apellido, documento (3–15 dígitos) y vínculo permitido.
2. **Crear Reserva**: elige función del fin de semana, selecciona un asiento en la matriz 11×11 (O/X).
3. **Cancelar Reserva**: selecciona la reserva activa a cancelar; el asiento vuelve a "O".
4. **Consultar funciones**: visualiza día, hora, película, sala y sillas disponibles para el próximo fin de semana.
5. **Administrador**: ingresa usuario/clave y consulta reportes (totales, pagos, promedio diario, usuarios, mayor/menor reservas) y exporta CSV.

## Exportación
Se generan `usuarios.csv`, `reservas.csv` y `ventas.csv`.
