
# 🎬 Cinema Universitario (Nombre)

![logo](assets/logo.png)

Sistema de consola en **Python** para gestionar el **Cinema Universitario**: registro de usuarios, reservas/cancelaciones (visualización de asientos **O/X**), impresión de **facturas**, consulta de **funciones del fin de semana**, **módulo administrador** con reportes y **exportación a CSV**.

## 1. Integrantes
- (Nombre 1) – Programa: (Programa), habilidades: (…)
- (Nombre 2) – Programa: (Programa), habilidades: (…)
- (Nombre 3) – Programa: (Programa), habilidades: (…)

## 2. Vínculos académicos y descripción
Describe aquí para cada integrante el programa al cual pertenece y sus fortalezas.

## 3. Nombre del proyecto y detalles
**Nombre sugerido:** *Cinema UdeA – Caldas* (puedes cambiarlo). Breve descripción del proyecto y objetivo.

## 4. Licencia del software
Este repositorio usa **MIT License** por ser software; si tu docente requiere **Creative Commons** (indicado en el enunciado), documenta la elección en `doc/licencia.md`.

## 5. Reporte de visión
Consulta `doc/vision.md`.

## 6. Especificación de requisitos
Consulta `requisitos/funcionales.md` y `requisitos/no_funcionales.md`.

## 7. Plan de proyecto
Consulta `gestion/plan_proyecto.md` (incluye diagrama de Gantt y presupuesto en horas/SMLV).

## 8. Plan de versionado
Consulta `gestion/versionado.md`.

## 9. Algoritmo (código)
Código fuente dentro de `src/`:
- `Cinema_UdeA.ipynb` (Google Colab)
- `cinema_udea.py` (script Python ejecutable en local)

## 10. Manual de usuario
Consulta `doc/manual_usuario.md`.

## 11. GitHub
Sube este repositorio con credenciales **UdeA** y vincula a tus compañeros como colaboradores.

## 12. Sustentaciones
Semanas 15–16: todo el equipo debe tener el software **disponible y ejecutable**.

## 13. Fechas y Documentos
- **Entrega 1**: puntos 1 a 7 (Semana 8)
- **Entrega 2**: todo lo descrito (Semana 16)

---

### ▶️ Cómo ejecutar
**Opción A – Google Colab**
1. Abre Google Colab.
2. Subir `src/Cinema_UdeA.ipynb`.
3. Ejecuta todas las celdas y usa el menú en consola.

**Opción B – Local (Python 3.10+)**
```bash
python src/cinema_udea.py
```

### Exportación CSV
El sistema genera `datos/usuarios.csv`, `datos/reservas.csv`, `datos/ventas.csv`.

### Credenciales Admin (por defecto)
Usuario: `admin` • Clave: `admin123` (modifica en `cinema_udea.py`).

