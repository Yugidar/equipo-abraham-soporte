Proyecto: Sistema de Soporte Técnico (Tickets)

Alumno: Abraham Garza

Materia: Diseño y Arquitectura de Software

Fecha: Abril 2026
¿Qué problema resuelve?

Quería hacer una aplicación sencilla para un sistema de tickets donde los clientes puedan reportar problemas técnicos. El sistema permite registrar el título del problema y la prioridad, y separar el registro del ticket de la notificación al área técnica. Use microservicios para que el proceso pesado de avisar a los técnicos no bloquee al cliente cuando está registrando su reporte.

Estructura de la Base de Datos
Tabla	Descripción	Relación
clientes	Guarda los datos maestros de los usuarios.	Se relaciona con tickets (1 a muchos).
tecnicos	Lista del personal disponible para atender fallas.	Se relaciona con tickets (1 a muchos).
tickets	Es la tabla principal que une al cliente con el problema.	Tiene llaves foráneas hacia clientes y tecnicos.

Rutas de la API
Método	Ruta	Qué hace
GET    	/	     Muestra la interfaz principal con el formulario.
POST	/abrir_ticket	Registra el ticket en la base de datos y llama al Servicio B.
GET	    /tickets	Consulta y devuelve todos los tickets guardados en formato JSON.
POST	/asignar	Permite asignar un técnico a un ticket específico.
GET    	/tecnicos	Lista todos los técnicos que están disponibles actualmente.

¿Cuál es la tarea pesada y por qué bloquea el sistema?
La tarea pesada está en el Servicio B, osea en las notificaciones. Ahí puse un time.sleep(7) que simula el tiempo que tardaría el sistema en enviar correos o alertas a todo el equipo de soporte. En un monolito, el usuario tendría que esperar esos 7 segundos frente a una pantalla blanca antes de saber si su ticket se guardó. Con microservicios, el Servicio A guarda el dato en milisegundos y deja que el Servicio B trabaje por su cuenta.


Cómo levantar el proyecto
Bash

# 1. Clonar el repositorio
git clone https://github.com/Yugidar/equipo-abraham-soporte.git

# 2. Crear las tablas en RDS
# Es necesario entrar a MySQL y pegar el archivo schema.sql para crear clientes, tecnicos y tickets.
mysql -h TU_ENDPOINT_RDS -u admin -p < schema.sql

# 3. Levantar con Docker Compose
# Usamos estas variables para evitar errores de versionamiento de Buildx en AWS
DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 docker-compose up --build -d

# 4. Abrir en navegador
http://54.166.208.65:5000

Decisiones técnicas

Lo más difícil fue configurar la comunicación entre los contenedores. Al principio el Servicio A me decía que el Servicio B estaba en mantenimiento aunque estuviera encendido, y descubrí que era por el timeout; el Servicio A era tan rápido que no esperaba los 7 segundos del B. También tuve problemas con las llaves foráneas (error 1452), y fue por que no se puede registrar un ticket si el ID del cliente no existe primero en la tabla de clientes.

Diseñé las tablas así para mantener la integridad: si borras un cliente, no deberían quedar tickets "volando". Para los errores se uso try/except y me aseguré de cerrar siempre las conexiones con finally para no saturar la RDS de Amazon.
Puntos Extra — Arquitectura de Microservicios

    Criterio 1: El Servicio A solo gestiona la UI y la BD. El Servicio B solo hace la tarea pesada con el time.sleep.

    Criterio 2: Se comunican internamente usando http://servicio_b:5001.

    Criterio 3: El puerto 5001 no está abierto en el Security Group de AWS ni en el ports del compose, así que el Servicio B es privado.

    Criterio 4: Si apago el Servicio B con docker stop, la aplicación sigue funcionando y permite registrar tickets, demostrando resiliencia.

Checklist de Autoevaluación

    [x] Repositorio con estructura correcta.

    [x] Mínimo 3 tablas relacionadas en RDS.

    [x] 5 rutas funcionales y una de ellas es de consulta (GET).

    [x] Uso de variables de entorno para credenciales.

    [x] Manejo de errores y consultas parametrizadas (%s).
