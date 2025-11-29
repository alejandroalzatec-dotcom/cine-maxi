
# -*- coding: utf-8 -*-
# Cinema Universitario (Nombre) - Consola Python

import csv
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

VINCULOS_PRECIOS: Dict[str, int] = {
    "Estudiantes": 7500,
    "Docentes": 10000,
    "Administrativos": 8500,
    "Oficiales internos": 7000,
    "Publico externo": 15000,
}

def validar_nombre_apellido(texto: str, campo: str) -> List[str]:
    errores = []
    if len(texto.strip()) < 3:
        errores.append(f"{campo} no puede tener menos de 3 letras.")
    if any(ch.isdigit() for ch in texto):
        errores.append(f"{campo} no puede contener números.")
    return errores


def validar_documento(doc: str) -> List[str]:
    errores = []
    if not doc.isdigit():
        errores.append("Documento solo permite números.")
    if len(doc) < 3 or len(doc) > 15:
        errores.append("Documento debe tener entre 3 y 15 dígitos.")
    return errores


def validar_vinculo(vinculo: str) -> List[str]:
    errores = []
    if vinculo not in VINCULOS_PRECIOS:
        errores.append(
            "Tipo de vínculo inválido. Opciones: " + ", ".join(VINCULOS_PRECIOS.keys())
        )
    return errores

@dataclass
class Usuario:
    nombre: str
    apellido: str
    documento: str
    vinculo: str
    reservas: List["Reserva"] = field(default_factory=list)

@dataclass
class Pelicula:
    titulo: str
    duracion_min: int = 120
    clasificacion: str = "A"

class MapaAsientos:
    def __init__(self, filas: int = 11, columnas: int = 11):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [["O" for _ in range(columnas)] for _ in range(filas)]
    def disponible(self, fila: int, col: int) -> bool:
        return 1 <= fila <= self.filas and 1 <= col <= self.columnas and self.mapa[fila-1][col-1] == "O"
    def reservar(self, fila: int, col: int) -> bool:
        if self.disponible(fila, col):
            self.mapa[fila-1][col-1] = "X"
            return True
        return False
    def cancelar(self, fila: int, col: int) -> bool:
        if 1 <= fila <= self.filas and 1 <= col <= self.columnas and self.mapa[fila-1][col-1] == "X":
            self.mapa[fila-1][col-1] = "O"
            return True
        return False
    def disponibles_count(self) -> int:
        return sum(1 for r in self.mapa for c in r if c == "O")
    def imprimir(self):
        print("
Estado de asientos (O=Disponible, X=Reservado):")
        header = "   " + " ".join([f"{c:>2}" for c in range(1, self.columnas+1)])
        print(header)
        for i, fila in enumerate(self.mapa, start=1):
            print(f"{i:>2} " + " ".join([f"{s:>2}" for s in fila]))
        print(f"
Disponibles: {self.disponibles_count()} / {self.filas * self.columnas}")

@dataclass
class Funcion:
    pelicula: Pelicula
    fecha_hora: datetime
    sala: str
    asientos: MapaAsientos = field(default_factory=MapaAsientos)

@dataclass
class Reserva:
    usuario: Usuario
    funcion: Funcion
    fila: int
    col: int
    precio: int
    activa: bool = True
    fecha_reserva: datetime = field(default_factory=datetime.now)
    def factura_texto(self) -> str:
        fecha_str = self.fecha_reserva.strftime("%Y-%m-%d %H:%M")
        func_str = self.funcion.fecha_hora.strftime("%Y-%m-%d %H:%M")
        return (
            f"----- FACTURA CINEMA UNIVERSITARIO -----
"
            f"Fecha factura: {fecha_str}
"
            f"Cliente: {self.usuario.nombre} {self.usuario.apellido}
"
            f"Documento: {self.usuario.documento}
"
            f"Vínculo: {self.usuario.vinculo}
"
            f"Pelicula: {self.funcion.pelicula.titulo}
"
            f"Función: {func_str} | Sala: {self.funcion.sala}
"
            f"Asiento: Fila {self.fila}, Columna {self.col}
"
            f"Valor: ${self.precio}
"
            f"Estado: {'ACTIVA' if self.activa else 'CANCELADA'}
"
            f"----------------------------------------"
        )

class CinemaSystem:
    def __init__(self):
        self.usuarios: Dict[str, Usuario] = {}
        self.funciones: List[Funcion] = []
        self.reservas: List[Reserva] = []
        self.admins: Dict[str, str] = {"admin": "admin123"}
    def registrar_usuario(self) -> None:
        print("
== Registrar Usuario ==")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        documento = input("Documento: ").strip()
        print("Tipos de vínculo:", ", ".join(VINCULOS_PRECIOS.keys()))
        vinculo = input("Vínculo: ").strip()
        errores = []
        errores += validar_nombre_apellido(nombre, "Nombre")
        errores += validar_nombre_apellido(apellido, "Apellido")
        errores += validar_documento(documento)
        errores += validar_vinculo(vinculo)
        if errores:
            print("
Se encontraron errores:")
            for e in errores:
                print(f"- {e}")
            return
        if documento in self.usuarios:
            print("Ya existe un usuario con ese documento.")
            return
        u = Usuario(nombre, apellido, documento, vinculo)
        self.usuarios[documento] = u
        print("Usuario registrado exitosamente.")
    def crear_reserva(self) -> None:
        print("
== Crear Reserva ==")
        doc = input("Documento del usuario: ").strip()
        usuario = self.usuarios.get(doc)
        if not usuario:
            print("El usuario no está registrado. Primero registre el usuario.")
            return
        funciones = self.funciones_fin_de_semana()
        if not funciones:
            print("No hay funciones programadas para el próximo fin de semana.")
            return
        print("
Funciones del fin de semana:")
        for idx, f in enumerate(funciones, start=1):
            fecha_str = f.fecha_hora.strftime("%A %Y-%m-%d %H:%M")
            print(f"[{idx}] {fecha_str} | {f.pelicula.titulo} | Sala {f.sala} | Sillas disponibles: {f.asientos.disponibles_count()}")
        try:
            i = int(input("Seleccione la función [número]: ").strip())
            if i < 1 or i > len(funciones):
                print("Selección inválida.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
        funcion = funciones[i-1]
        funcion.asientos.imprimir()
        try:
            fila = int(input("Fila (1-11): ").strip())
            col = int(input("Columna (1-11): ").strip())
        except ValueError:
            print("Entrada inválida de asiento.")
            return
        if not funcion.asientos.disponible(fila, col):
            print("El asiento no está disponible.")
            return
        precio = VINCULOS_PRECIOS[usuario.vinculo]
        ok = funcion.asientos.reservar(fila, col)
        if not ok:
            print("No fue posible reservar el asiento.")
            return
        reserva = Reserva(usuario=usuario, funcion=funcion, fila=fila, col=col, precio=precio)
        self.reservas.append(reserva)
        usuario.reservas.append(reserva)
        print("
Reserva creada correctamente. Se actualizó el mapa de asientos:")
        funcion.asientos.imprimir()
        print("
Factura:")
        print(reserva.factura_texto())
    def cancelar_reserva(self) -> None:
        print("
== Cancelar Reserva ==")
        doc = input("Documento del usuario: ").strip()
        usuario = self.usuarios.get(doc)
        if not usuario:
            print("El usuario no existe.")
            return
        activas = [r for r in usuario.reservas if r.activa]
        if not activas:
            print("El usuario no tiene reservas activas. ¿Desea crear una? (s/n)")
            if input().strip().lower() == "s":
                self.crear_reserva()
            return
        print("
Reservas activas:")
        for idx, r in enumerate(activas, start=1):
            fstr = r.funcion.fecha_hora.strftime("%Y-%m-%d %H:%M")
            print(f"[{idx}] {r.funcion.pelicula.titulo} | {fstr} | Sala {r.funcion.sala} | Asiento (F{r.fila},C{r.col}) | ${r.precio}")
        try:
            i = int(input("Seleccione la reserva a cancelar [número]: ").strip())
            if i < 1 or i > len(activas):
                print("Selección inválida.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
        rsv = activas[i-1]
        ok = rsv.funcion.asientos.cancelar(rsv.fila, rsv.col)
        if not ok:
            print("No se pudo cancelar (ya estaba disponible).")
            return
        rsv.activa = False
        print("Reserva cancelada. Estado del asiento actualizado:")
        rsv.funcion.asientos.imprimir()
    def funciones_fin_de_semana(self) -> List[Funcion]:
        prox_sabado, prox_domingo = self._proximo_fin_de_semana()
        return [f for f in self.funciones if prox_sabado.date() <= f.fecha_hora.date() <= prox_domingo.date()]
    def listar_funciones_fin_de_semana(self) -> None:
        print("
== Consultar funciones del fin de semana ==")
        funciones = self.funciones_fin_de_semana()
        if not funciones:
            print("No hay funciones programadas para el próximo fin de semana.")
            return
        for f in sorted(funciones, key=lambda x: (x.fecha_hora, x.pelicula.titulo)):
            fecha_str = f.fecha_hora.strftime("%A %Y-%m-%d %H:%M")
            print(f"{fecha_str} | {f.pelicula.titulo} | Sala {f.sala} | Sillas disponibles: {f.asientos.disponibles_count()}")
    def login_admin(self) -> bool:
        print("
== Módulo Administrador ==")
        usr = input("Usuario admin: ").strip()
        pwd = input("Clave: ").strip()
        if self.admins.get(usr) == pwd:
            print("Acceso concedido.")
            return True
        print("Credenciales inválidas.")
        return False
    def submenu_admin(self) -> None:
        if not self.login_admin():
            return
        while True:
            print("
--- Submenú Administración ---")
            print("1) Total de reservas registradas")
            print("2) Total de tiquetes vendidos")
            print("3) Total de reservas realizadas (activas)")
            print("4) Total pago realizado")
            print("5) Promedio por venta diario del cine")
            print("6) Lista de usuarios")
            print("7) Usuario con mayor y menor cantidad de reservas")
            print("8) Exportar CSV (usuarios, reservas, ventas)")
            print("9) Volver")
            op = input("Seleccione opción: ").strip()
            if op == "1":
                print(f"Total reservas registradas: {len(self.reservas)}")
            elif op == "2":
                vendidos = sum(1 for r in self.reservas if r.activa)
                print(f"Total de tiquetes vendidos: {vendidos}")
            elif op == "3":
                realizadas = sum(1 for r in self.reservas if r.activa)
                print(f"Total de reservas realizadas (activas): {realizadas}")
            elif op == "4":
                total_pago = sum(r.precio for r in self.reservas if r.activa)
                print(f"Total pago realizado: ${total_pago}")
            elif op == "5":
                print(f"Promedio por venta diario: ${self.promedio_venta_diario():.2f}")
            elif op == "6":
                self.listar_usuarios()
            elif op == "7":
                self.mayor_menor_reservas()
            elif op == "8":
                self.exportar_csv()
            elif op == "9":
                break
            else:
                print("Opción inválida.")
    def promedio_venta_diario(self) -> float:
        ventas_por_dia: Dict[str, int] = {}
        for r in self.reservas:
            if r.activa:
                dia = r.fecha_reserva.strftime("%Y-%m-%d")
                ventas_por_dia.setdefault(dia, 0)
                ventas_por_dia[dia] += r.precio
        if not ventas_por_dia:
            return 0.0
        return sum(ventas_por_dia.values()) / len(ventas_por_dia)
    def listar_usuarios(self) -> None:
        if not self.usuarios:
            print("No hay usuarios registrados.")
            return
        print("
--- Usuarios ---")
        for u in self.usuarios.values():
            print(f"{u.nombre} {u.apellido} | Doc: {u.documento} | Vínculo: {u.vinculo} | Reservas: {sum(1 for r in u.reservas if r.activa)} activas / {len(u.reservas)} totales")
    def mayor_menor_reservas(self) -> None:
        if not self.usuarios:
            print("No hay usuarios.")
            return
        orden = sorted(self.usuarios.values(), key=lambda u: len(u.reservas), reverse=True)
        mayor = orden[0]
        menor = orden[-1]
        print(f"Mayor reservas: {mayor.nombre} {mayor.apellido} | {len(mayor.reservas)}")
        print(f"Menor reservas: {menor.nombre} {menor.apellido} | {len(menor.reservas)}")
    def exportar_csv(self) -> None:
        os.makedirs("datos", exist_ok=True)
        with open(os.path.join("datos", "usuarios.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["documento", "nombre", "apellido", "vinculo"])
            for u in self.usuarios.values():
                w.writerow([u.documento, u.nombre, u.apellido, u.vinculo])
        with open(os.path.join("datos", "reservas.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["documento", "pelicula", "fecha_funcion", "sala", "fila", "col", "precio", "activa", "fecha_reserva"])
            for r in self.reservas:
                w.writerow([r.usuario.documento, r.funcion.pelicula.titulo, r.funcion.fecha_hora.strftime("%Y-%m-%d %H:%M"), r.funcion.sala, r.fila, r.col, r.precio, "SI" if r.activa else "NO", r.fecha_reserva.strftime("%Y-%m-%d %H:%M")])
        with open(os.path.join("datos", "ventas.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["fecha", "documento", "pelicula", "monto"])
            for r in self.reservas:
                if r.activa:
                    w.writerow([r.fecha_reserva.strftime("%Y-%m-%d"), r.usuario.documento, r.funcion.pelicula.titulo, r.precio])
        print("CSV exportados en la carpeta 'datos/'.")
    def _proximo_fin_de_semana(self) -> Tuple[datetime, datetime]:
        hoy = datetime.now()
        dias_hasta_sabado = (5 - hoy.weekday()) % 7
        dias_hasta_domingo = (6 - hoy.weekday()) % 7
        prox_sabado = (hoy + timedelta(days=dias_hasta_sabado)).replace(hour=0, minute=0, second=0, microsecond=0)
        prox_domingo = (hoy + timedelta(days=dias_hasta_domingo)).replace(hour=23, minute=59, second=59, microsecond=0)
        return prox_sabado, prox_domingo
    def agregar_funcion(self, pelicula_titulo: str, fecha_hora: datetime, sala: str = "A") -> None:
        pel = Pelicula(pelicula_titulo)
        func = Funcion(pelicula=pel, fecha_hora=fecha_hora, sala=sala)
        self.funciones.append(func)
    def configurar_funciones_ejemplo(self) -> None:
        sab, dom = self._proximo_fin_de_semana()
        self.agregar_funcion("Ciencia de Datos", sab.replace(hour=15, minute=0), "A")
        self.agregar_funcion("Algoritmos en Acción", sab.replace(hour=19, minute=30), "B")
        self.agregar_funcion("Ingeniería y Sociedad", dom.replace(hour=14, minute=0), "A")
        self.agregar_funcion("Robótica UdeA", dom.replace(hour=18, minute=30), "C")

def mostrar_menu_principal():
    print("
===== Cinema Universitario (Nombre) =====")
    print("1) Registrar Usuario")
    print("2) Crear Reserva")
    print("3) Cancelar Reserva")
    print("4) Consultar funciones del fin de semana")
    print("5) Administrador")
    print("6) Exportar CSV")
    print("7) Salir")

def main():
    sistema = CinemaSystem()
    sistema.configurar_funciones_ejemplo()
    while True:
        mostrar_menu_principal()
        op = input("Seleccione una opción: ").strip()
        if op == "1":
            sistema.registrar_usuario()
        elif op == "2":
            sistema.crear_reserva()
        elif op == "3":
            sistema.cancelar_reserva()
        elif op == "4":
            sistema.listar_funciones_fin_de_semana()
        elif op == "5":
            sistema.submenu_admin()
        elif op == "6":
            sistema.exportar_csv()
        elif op == "7":
            print("Gracias por usar el Cinema Universitario. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida, intente nuevamente.")

if __name__ == "__main__":
    main()
