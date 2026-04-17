-- Sistema de Soporte Técnico
-- Equipo: Abraham Garza

CREATE DATABASE IF NOT EXISTS soporte_db;
USE soporte_db;

-- Tabla 1: Técnicos
CREATE TABLE IF NOT EXISTS tecnicos (
    id_tecnico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(50),
    disponible BOOLEAN DEFAULT TRUE
);

-- Tabla 2: Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- Tabla 3: Tickets (Relaciona Clientes y Técnicos)
CREATE TABLE IF NOT EXISTS tickets (
    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    prioridad ENUM('Baja', 'Media', 'Alta') DEFAULT 'Media',
    estado ENUM('Abierto', 'En progreso', 'Resuelto') DEFAULT 'Abierto',
    id_cliente INT,
    id_tecnico INT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_tecnico) REFERENCES tecnicos(id_tecnico)
);

-- Datos iniciales para que la consulta no salga vacía
INSERT INTO tecnicos (nombre, especialidad) VALUES ('Abraham Garza', 'Redes'), ('Soporte Admin', 'Hardware');
INSERT INTO clientes (nombre, email) VALUES ('Juan Perez', 'juan@correo.com');
