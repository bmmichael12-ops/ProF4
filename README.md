# ProF4
Fase 4 - Componente practico - practicas simuladas



## Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado de manera individual para el curso Programación (213023) - Fase 4  
Universidad Nacional Abierta y a Distancia.

**Estudiante:** Michael Stwear Baena Marin  
**Cédula:** 1214715704  

## Descripción

Aplicación de consola en Python creada para administrar los siguientes datos: clientes, servicios y reservas de la empresa **Software FJ**. Todo el manejo de datos se realiza en memoria usando objetos y listas sin depender de bases de datos externas. Genera un archivo externo al ejecutar el programa que es un registro de eventos y errores (`logs_software_fj.txt`).

El objetivo principal del proyecto es mantener la aplicación estable frente a datos incorrectos, operaciones inválidas o fallos en los cálculos sin que la ejecución se detenga.


## Programación Orientada a Objetos (POO)
* **Abstracción:** las Clases base abstractas `Entidad` y `Servicio` implementadas con el módulo `abc`.
* **Encapsulación:** los Atributos privados con acceso controlado mediante decoradores `@property` y validaciones internas en `Cliente`, `Servicio` y `Reserva`.
* **Herencia y Polimorfismo:** Tres tipos de servicios heredan de `Servicio` (`ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`). Cada uno sobrescribe `validar_parametros()`, `describir_servicio()` y `calcular_costo()` con reglas de negocio propias.
* **Sobrecarga de métodos:** El método `calcular_costo()` acepta parámetros opcionales (`impuesto`, `descuento`, `recargo`) para adaptarse a distintos escenarios de facturación.

## Manejo avanzado de excepciones
* **Jerarquía de excepciones personalizadas:** `ErrorSistemaFJ` como base para `DatoInvalidoError`, `ParametroFaltanteError`, `ServicioNoDisponibleError`, `OperacionNoPermitidaError`, `CalculoInconsistenteError` y `ReservaError`.
* **Estructuras de control:** Uso de bloques `try/except`, `try/except/else` y `try/except/finally` a lo largo del flujo de registro y reservas.
* **Encadenamiento de excepciones:** Uso de `raise ... from e` para conservar el error original al propagar fallos en la creación o el procesamiento de reservas.
* **Registro de logs:** La clase `GestorLogs` guarda automáticamente la fecha, hora, nivel (`INFO` o `ERROR`), mensaje y causa de cada evento en `logs_software_fj.txt`.

## Requisitos

* Python 3.8 o superior.
* No requiere librerías externas.

## Cómo ejecutar el proyecto

   git clone <https://github.com/bmmichael12-ops/ProF4.git>
   