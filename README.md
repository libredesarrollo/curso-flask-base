# Proyecto Flask: Módulo de Administración

Este proyecto forma parte del curso de desarrollo con Flask. En este módulo nos enfocamos en la creación de un sistema de administración avanzado (Dashboard) para nuestra aplicación. 

## Características principales
- Implementación de un panel de administrador potente.
- Gestión avanzada de modelos y bases de datos.
- Manejo de roles y permisos con Flask-User, limitando accesos y delegando permisos.
- Diseños personalizados y estructuración técnica con extensiones de Flask (Flask-Admin y Flask-Migrate).

## Requerimientos y ejecución
1. Crea un entorno virtual: `python3 -m venv venv`
2. Actívalo: `source venv/bin/activate` (Mac/Linux) o `venv\Scripts\activate` (Windows)
3. Instala las dependencias y bibliotecas especificadas en la lección.
4. Ejecuta tus scripts de migración e inicializa la aplicación.

# Proyecto Flask: Módulo de Facturación

Este proyecto es parte del sistema construido durante el curso de desarrollo con Flask. El módulo `invoice` (Facturación) está desarrollado como un *Blueprint* aislado que se encarga de manejar el flujo de transacciones, y facturas para usuarios regulares.

## Características principales
- Buscador asíncrono de productos con JavaScript (`fetch`) y SQLAlchemy (`like`).
- API de consumo local que devuelve información en formato JSON utilizando propiedades personalizadas.
- Lógica de relación entre Base de Datos (Uno a Muchos) para gestionar *Ventas* (Sells) y *Productos Acatados* (SellProducts).
- Envío de formularios manuales (recopilando selecciones) recolectando datos del cliente vía objeto nativo `FormData`.
- Renderizado y descarga de comprobantes en PDF de manera fácil gracias a librerías de conversión HTML a PDF automáticas (con uso de `pdfkit`).

## Instalación y ejecución
1. Configura tu entorno virtual y tu base de datos del proyecto base de manera habitual.
2. Asegúrate de instalar y configurar la herramienta de sistema operativo CLI subyacente para PDF llamada `wkhtmltopdf`.
3. Recuerda incluir tu archivo `models.py` del Blueprint dentro del controlador para que `Flask-Migrate` reconozca e inicie la base de datos relacional.
4. ¡Lanza el proyecto!

## Más información
Puedes encontrar todos los detalles completos, la teoría profunda de los temas propuestos aquí así como los videos explicativos consultando el curso principal:
[Curso de Flask en Desarrollo Libre](https://www.desarrollolibre.net/blog/flask/curso-flask)

