
# Plan de Proyecto

## Cronograma (Mermaid Gantt)
```mermaid
gantt
    title Cinema UdeA - Cronograma
    dateFormat  YYYY-MM-DD
    section Inicio
    Levantamiento y visión         :active, 2025-09-01, 7d
    section Diseño
    Requisitos y arquitectura      : 2025-09-08, 10d
    Modelado (POO)                 : 2025-09-18, 7d
    section Implementación
    Desarrollo iterativo           : 2025-09-25, 21d
    Pruebas y ajustes              : 2025-10-16, 10d
    section Entrega
    Entrega 1 (1–7)                :milestone, 2025-10-20, 0d
    Documentación completa         : 2025-10-21, 14d
    Sustentaciones (sem 15–16)     :milestone, 2025-11-25, 0d
```

> Las fechas son referenciales; ajusta según tu calendario real de 2025-2.

## Presupuesto (en horas de práctica)
- Equipo: **3 estudiantes** × **50 horas** cada uno = **150 horas**.
- Valor de práctica: **1 SMLV** (no se paga dinero, se reconoce en tiempo de formación).

## Riesgos y mitigación
- Cambios en el listado de películas → parametrización en `configurar_funciones_ejemplo()`.
- Fallos por entradas inválidas → validaciones y mensajes claros.
