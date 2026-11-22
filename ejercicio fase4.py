# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA
# Estudiante: Michael Stwear Baena Marin
# Cedula: 1214715704
# Curso: Programacion (213023) - Fase 4
# Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas (Software FJ)
# Principios POO: Abstraccion, Encapsulacion, Herencia, Polimorfismo, Sobrecarga y Excepciones

# Importacion de librerias basicas de Python
from abc import ABC, abstractmethod
from datetime import datetime



# EXCEPCIONES PERSONALIZADAS

# Excepcion base del sistema para agrupar todos los errores controlados
class ErrorSistemaFJ(Exception):
    pass

# Error para datos que no cumplen con el formato o rango valido
class DatoInvalidoError(ErrorSistemaFJ):
    pass

# Error cuando falta un dato obligatorio para crear un objeto
class ParametroFaltanteError(ErrorSistemaFJ):
    pass

# Error cuando se intenta reservar un servicio ocupado o inactivo
class ServicioNoDisponibleError(ErrorSistemaFJ):
    pass

# Error cuando se intenta ejecutar una accion invalida segun el estado actual
class OperacionNoPermitidaError(ErrorSistemaFJ):
    pass

# Error cuando un calculo financiero arroja valores incoherentes
class CalculoInconsistenteError(ErrorSistemaFJ):
    pass

# Error general de reservas usado para encadenar fallos internos
class ReservaError(ErrorSistemaFJ):
    pass



# GESTOR DE LOGS EN ARCHIVO DE TEXTO


# Clase encargada de guardar eventos y errores en un archivo local
class GestorLogs:
    def __init__(self, nombre_archivo="logs_software_fj.txt"):
        self.__nombre_archivo = nombre_archivo

    # Metodo que escribe cada evento con fecha, hora y nivel
    def registrar(self, nivel, mensaje, error=None):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{fecha}] [{nivel}] {mensaje}"
        if error is not None:
            linea += f" | Excepcion: {type(error).__name__}: {error}"
            if error.__cause__ is not None:
                linea += f" | Causa original: {type(error.__cause__).__name__}: {error.__cause__}"
        try:
            with open(self.__nombre_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea + "\n")
        except OSError as e:
            print(f"No se pudo escribir en el archivo de logs: {e}")



# CLASE ABSTRACTA BASE DEL SISTEMA


# Clase abstracta que representa cualquier entidad principal de Software FJ
class Entidad(ABC):
    def __init__(self, id_entidad):
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El ID de la entidad es obligatorio.")
        self.__id_entidad = str(id_entidad).strip()

    @property
    def id_entidad(self):
        return self.__id_entidad

    # Metodo abstracto para validar los datos propios de cada entidad
    @abstractmethod
    def validar(self):
        pass

    # Metodo abstracto para devolver una descripcion corta del objeto
    @abstractmethod
    def obtener_resumen(self):
        pass



# CLASE CLIENTE CON ENCAPSULACION Y VALIDACIONES


# Clase que modela a los clientes y protege sus datos personales
class Cliente(Entidad):
    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono
        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # Validacion estricta de campos obligatorios y formato de contacto
    def validar(self):
        if not self.__nombre or not str(self.__nombre).strip():
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacio.")
        if not self.__correo or not str(self.__correo).strip():
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        if "@" not in self.__correo or "." not in self.__correo:
            raise DatoInvalidoError(f"Correo invalido: '{self.__correo}'.")
        tel = str(self.__telefono).strip()
        if not tel:
            raise ParametroFaltanteError("El telefono del cliente es obligatorio.")
        if not tel.isdigit() or len(tel) < 7:
            raise DatoInvalidoError(f"Telefono invalido: '{tel}'. Debe tener al menos 7 digitos.")

    def obtener_resumen(self):
        return f"Cliente [{self.id_entidad}] {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"



# CLASE ABSTRACTA SERVICIO Y CLASES ESPECIALIZADAS


# Clase abstracta base para los servicios ofrecidos por Software FJ
class Servicio(Entidad):
    def __init__(self, id_servicio, nombre, tarifa_base):
        super().__init__(id_servicio)
        self.__nombre = nombre
        self.__tarifa_base = tarifa_base
        self.__disponible = True
        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa_base(self):
        return self.__tarifa_base

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, estado):
        if not isinstance(estado, bool):
            raise DatoInvalidoError("La disponibilidad debe ser True o False.")
        self.__disponible = estado

    # Validacion general del servicio y llamada a validacion especifica
    def validar(self):
        if not self.__nombre or not str(self.__nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        try:
            self.__tarifa_base = float(self.__tarifa_base)
        except (TypeError, ValueError) as e:
            raise DatoInvalidoError("La tarifa base debe ser un numero valido.") from e
        if self.__tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor a cero.")
        self.validar_parametros()

    # Metodo sobrecargado mediante parametros opcionales para calcular costos
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, recargo=0.0):
        try:
            duracion = float(duracion)
            impuesto = float(impuesto)
            descuento = float(descuento)
            recargo = float(recargo)
        except (TypeError, ValueError) as e:
            raise DatoInvalidoError("Los parametros de calculo deben ser numericos.") from e

        if duracion <= 0:
            raise DatoInvalidoError("La duracion del servicio debe ser mayor a cero.")
        if descuento < 0 or descuento > 100:
            raise CalculoInconsistenteError("El porcentaje de descuento debe estar entre 0 y 100.")
        if impuesto < 0 or recargo < 0:
            raise CalculoInconsistenteError("El impuesto y el recargo no pueden ser negativos.")

        subtotal = (self.__tarifa_base * duracion) + recargo
        valor_descuento = subtotal * (descuento / 100)
        base_gravable = subtotal - valor_descuento
        total = base_gravable * (1 + impuesto)

        if total < 0:
            raise CalculoInconsistenteError("El costo final no puede ser negativo.")
        return round(total, 2)

    @abstractmethod
    def validar_parametros(self):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def obtener_resumen(self):
        estado = "Disponible" if self.__disponible else "Ocupado"
        return f"{self.describir_servicio()} | Tarifa: ${self.__tarifa_base:,.2f} | Estado: {estado}"


# Servicio especializado 1: Reserva de salas
class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_base, capacidad, con_proyector=False):
        self.__capacidad = capacidad
        self.__con_proyector = con_proyector
        super().__init__(id_servicio, nombre, tarifa_base)

    def validar_parametros(self):
        if not isinstance(self.__capacidad, int) or self.__capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero mayor a cero.")

    # Sobreescritura: suma recargo fijo si el cliente solicita proyector
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, recargo=0.0):
        extra_proyector = 25000.0 if self.__con_proyector else 0.0
        return super().calcular_costo(duracion, impuesto, descuento, recargo + extra_proyector)

    def describir_servicio(self):
        proy = "con proyector" if self.__con_proyector else "sin proyector"
        return f"Sala [{self.id_entidad}] {self.nombre} (Capacidad: {self.__capacidad}, {proy})"


# Servicio especializado 2: Alquiler de equipos
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_base, cantidad_equipos, con_seguro=False):
        self.__cantidad_equipos = cantidad_equipos
        self.__con_seguro = con_seguro
        super().__init__(id_servicio, nombre, tarifa_base)

    def validar_parametros(self):
        if not isinstance(self.__cantidad_equipos, int) or self.__cantidad_equipos <= 0:
            raise DatoInvalidoError("La cantidad de equipos debe ser un entero mayor a cero.")

    # Sobreescritura: multiplica por cantidad de equipos y agrega seguro si aplica
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, recargo=0.0):
        extra_equipos = self.tarifa_base * duracion * (self.__cantidad_equipos - 1)
        seguro = (self.tarifa_base * duracion * self.__cantidad_equipos) * 0.10 if self.__con_seguro else 0.0
        return super().calcular_costo(duracion, impuesto, descuento, recargo + extra_equipos + seguro)

    def describir_servicio(self):
        seg = "con seguro" if self.__con_seguro else "sin seguro"
        return f"Alquiler [{self.id_entidad}] {self.nombre} (Equipos: {self.__cantidad_equipos}, {seg})"


# Servicio especializado 3: Asesorias especializadas
class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_base, especialidad, modalidad="Virtual"):
        self.__especialidad = especialidad
        self.__modalidad = modalidad
        super().__init__(id_servicio, nombre, tarifa_base)

    def validar_parametros(self):
        if not self.__especialidad or not str(self.__especialidad).strip():
            raise ParametroFaltanteError("La especialidad de la asesoria es obligatoria.")
        if self.__modalidad not in ("Virtual", "Presencial"):
            raise DatoInvalidoError("La modalidad debe ser 'Virtual' o 'Presencial'.")

    # Sobreescritura: agrega recargo de desplazamiento si es presencial
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, recargo=0.0):
        extra_presencial = 30000.0 if self.__modalidad == "Presencial" else 0.0
        return super().calcular_costo(duracion, impuesto, descuento, recargo + extra_presencial)

    def describir_servicio(self):
        return f"Asesoria [{self.id_entidad}] {self.nombre} (Area: {self.__especialidad}, {self.__modalidad})"



# CLASE RESERVA


# Clase que integra cliente, servicio, duracion y ciclo de vida de la reserva
class Reserva(Entidad):
    def __init__(self, id_reserva, cliente, servicio, duracion):
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__costo_total = 0.0
        super().__init__(id_reserva)
        self.validar()

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    # Validacion de integridad de la reserva
    def validar(self):
        if not isinstance(self.__cliente, Cliente):
            raise DatoInvalidoError("Debe asignar un objeto Cliente valido.")
        if not isinstance(self.__servicio, Servicio):
            raise DatoInvalidoError("Debe asignar un objeto Servicio valido.")
        if not isinstance(self.__duracion, (int, float)) or self.__duracion <= 0:
            raise DatoInvalidoError("La duracion de la reserva debe ser mayor a cero.")
        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.__servicio.nombre}' no esta disponible.")

    # Confirma la reserva y bloquea el servicio
    def confirmar(self):
        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado '{self.__estado}'.")
        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.__servicio.nombre}' ya fue ocupado.")
        self.__estado = "Confirmada"
        self.__servicio.disponible = False

    # Cancela la reserva y libera el servicio si estaba confirmado
    def cancelar(self):
        if self.__estado in ("Cancelada", "Procesada"):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva en estado '{self.__estado}'.")
        if self.__estado == "Confirmada":
            self.__servicio.disponible = True
        self.__estado = "Cancelada"

    # Procesa el pago usando polimorfismo y encadenamiento de excepciones
    def procesar(self, impuesto=0.19, descuento=0.0, recargo=0.0):
        if self.__estado != "Confirmada":
            raise OperacionNoPermitidaError("Solo se pueden procesar reservas en estado 'Confirmada'.")
        try:
            self.__costo_total = self.__servicio.calcular_costo(self.__duracion, impuesto, descuento, recargo)
        except ErrorSistemaFJ as e:
            raise ReservaError(f"Error al procesar el cobro de la reserva {self.id_entidad}.") from e
        self.__estado = "Procesada"
        return self.__costo_total

    def obtener_resumen(self):
        return (
            f"Reserva [{self.id_entidad}] | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Horas: {self.__duracion} | "
            f"Estado: {self.__estado} | Total: ${self.__costo_total:,.2f}"
        )



# GESTOR PRINCIPAL DEL SISTEMA 

# Clase coordinadora que maneja las listas en memoria y el control de errores
class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logs = GestorLogs()

    # Usa bloque try/except/else para registrar clientes
    def registrar_cliente(self, id_cliente, nombre, correo, telefono):
        try:
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorSistemaFJ as e:
            self.logs.registrar("ERROR", f"Fallo registro de cliente {id_cliente}", e)
            print(f"[ERROR] Cliente {id_cliente} rechazado: {e}")
            return None
        else:
            self.clientes.append(nuevo_cliente)
            self.logs.registrar("INFO", f"Cliente registrado: {nuevo_cliente.obtener_resumen()}")
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    # Usa bloque try/except/finally para registrar servicios
    def registrar_servicio(self, servicio_clase, *args, **kwargs):
        nuevo_servicio = None
        try:
            nuevo_servicio = servicio_clase(*args, **kwargs)
            self.servicios.append(nuevo_servicio)
            self.logs.registrar("INFO", f"Servicio creado: {nuevo_servicio.obtener_resumen()}")
            print(f"[OK] {nuevo_servicio.obtener_resumen()}")
        except ErrorSistemaFJ as e:
            self.logs.registrar("ERROR", f"Fallo creacion de servicio {servicio_clase.__name__}", e)
            print(f"[ERROR] No se pudo crear {servicio_clase.__name__}: {e}")
        finally:
            print(f"   -> Total servicios activos en memoria: {len(self.servicios)}")
        return nuevo_servicio

    # Crea una reserva y encadena excepciones si falla la validacion
    def crear_reserva(self, id_reserva, cliente, servicio, duracion):
        try:
            try:
                nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion)
            except ErrorSistemaFJ as e:
                raise ReservaError(f"No se pudo crear la reserva {id_reserva}.") from e
            self.reservas.append(nueva_reserva)
            self.logs.registrar("INFO", f"Reserva creada: {nueva_reserva.obtener_resumen()}")
            print(f"[OK] {nueva_reserva.obtener_resumen()}")
            return nueva_reserva
        except ReservaError as e:
            self.logs.registrar("ERROR", f"Fallo en creacion de reserva {id_reserva}", e)
            print(f"[ERROR] {e} | Motivo: {e.__cause__}")
            return None

    # Confirma, cancela o procesa una reserva protegiendo la ejecucion
    def ejecutar_accion_reserva(self, reserva, accion, **kwargs):
        try:
            if reserva is None:
                raise ParametroFaltanteError("No existe una reserva valida para operar.")
            if accion == "confirmar":
                reserva.confirmar()
            elif accion == "cancelar":
                reserva.cancelar()
            elif accion == "procesar":
                reserva.procesar(**kwargs)
            else:
                raise OperacionNoPermitidaError(f"Accion desconocida: {accion}")
        except ErrorSistemaFJ as e:
            self.logs.registrar("ERROR", f"Fallo al {accion} reserva", e)
            detalle = f" | Causa: {e.__cause__}" if e.__cause__ else ""
            print(f"[ERROR] No se pudo {accion}: {e}{detalle}")
        else:
            self.logs.registrar("INFO", f"Accion '{accion}' exitosa: {reserva.obtener_resumen()}")
            print(f"[OK] Accion '{accion}' aplicada -> {reserva.obtener_resumen()}")



# SIMULACION DE OPERACIONES COMPLETAS (MINIMO 10 REQUERIDAS)


def ejecutar_simulacion():
    print("=" * 75)
    print("SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print("Fecha de ejecucion:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 75)

    sistema = SistemaSoftwareFJ()

    print("\n---  1: Registro valido de cliente ---")
    c1 = sistema.registrar_cliente("CC 123456", "Jacob Baena", "Jacob@hotmail.com", "3104230000")

    print("\n---  2: Registro valido de cliente ---")
    c2 = sistema.registrar_cliente("CC 132654", "Michael Baena", " mb01@hotmail.com", "3059876543")

    print("\n---  3: Registro invalido de cliente ---")
    sistema.registrar_cliente("CC 023145", "Camilo Marin", "camiloMB.com", "3125554433")

    print("\n---  4: Registro invalido de cliente ---")
    sistema.registrar_cliente("CC 258963", "", "fernando123@correo.com", "3172223344")

    print("\n---  5: Creacion valida de servicio (Reserva de Sala) ---")
    s1 = sistema.registrar_servicio(ReservaSala, "Sala001", "Sala Reuniones", 8000, 1, True)

    print("\n---  6: Creacion valida de servicio (Alquiler de Equipo) ---")
    s2 = sistema.registrar_servicio(AlquilerEquipo, "equipo001", "Portatil Macbook", 5000, 2, True)

    print("\n---  7: Creacion valida de servicio (Asesoria) ---")
    s3 = sistema.registrar_servicio(AsesoriaEspecializada, "asesoria001", "Polaris PH", 100000, "estructural", "Presencial")

    print("\n---  8: Creacion invalida de servicio (tarifa negativa) ---")
    sistema.registrar_servicio(ReservaSala, "Sala001", "Sala Reuniones", -8000, 1, False)

    print("\n---  9: Reserva exitosa de sala, confirmacion y procesamiento ---")
    r1 = sistema.crear_reserva("RSala001", c1, s1, 3)
    sistema.ejecutar_accion_reserva(r1, "confirmar")
    sistema.ejecutar_accion_reserva(r1, "procesar", impuesto=0.19, descuento=30.0)

    print("\n---  10: Reserva fallida (servicio ya ocupado) ---")
    sistema.crear_reserva("RSala001", c2, s1, 2)

    print("\n---  11: Error de calculo inconsistente (descuento mayor a 100%) ---")
    r4 = sistema.crear_reserva("Requipo001", c1, s2, 5)
    sistema.ejecutar_accion_reserva(r4, "confirmar")
    sistema.ejecutar_accion_reserva(r4, "procesar", impuesto=0.19, descuento=150.0)

    # Resumen final para comprobar que el sistema termino estable
    print("\n" + "=" * 75)
    print("RESUMEN FINAL DE EJECUCION (SIN INTERRUPCIONES)")
    print(f"Clientes validos registrados: {len(sistema.clientes)}")
    print(f"Servicios validos registrados: {len(sistema.servicios)}")
    print(f"Reservas creadas en memoria: {len(sistema.reservas)}")
    print("Registro detallado guardado en: logs_software_fj.txt")
    print("=" * 75)


if __name__ == "__main__":
    ejecutar_simulacion()