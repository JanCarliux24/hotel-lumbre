-- Lumbre Hotel & Spa: modelo relacional normalizado (PostgreSQL)
CREATE TABLE rol (
  id_rol      SMALLINT PRIMARY KEY,
  nombre      VARCHAR(20) NOT NULL UNIQUE,
  nivel       SMALLINT NOT NULL CHECK (nivel BETWEEN 0 AND 3)
);
CREATE TABLE usuario (
  id_usuario     VARCHAR(128) PRIMARY KEY,
  correo         VARCHAR(254) NOT NULL UNIQUE,
  nombre         VARCHAR(80)  NOT NULL CHECK (char_length(nombre) >= 2),
  telefono       VARCHAR(22),
  id_rol         SMALLINT NOT NULL DEFAULT 0 REFERENCES rol(id_rol),
  idioma         CHAR(2)  NOT NULL DEFAULT 'ES' CHECK (idioma IN ('ES','EN','PT','FR')),
  moneda         CHAR(3)  NOT NULL DEFAULT 'EUR' CHECK (moneda IN ('EUR','USD','MXN','GBP','BRL','COP')),
  tema           VARCHAR(6) NOT NULL DEFAULT 'LIGHT' CHECK (tema IN ('LIGHT','DARK','SYSTEM')),
  bloqueado      BOOLEAN NOT NULL DEFAULT FALSE,
  fecha_alta     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ultimo_acceso  TIMESTAMP
);
CREATE TABLE tipo_habitacion (
  id_tipo           VARCHAR(12) PRIMARY KEY,
  nombre            VARCHAR(40) NOT NULL,
  descripcion       VARCHAR(200),
  superficie_m2     SMALLINT CHECK (superficie_m2 > 0),
  capacidad         SMALLINT NOT NULL CHECK (capacidad BETWEEN 1 AND 6),
  precio_noche_eur  NUMERIC(7,2) NOT NULL CHECK (precio_noche_eur BETWEEN 30 AND 5000),
  disponible        BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE amenidad (
  id_amenidad SMALLINT PRIMARY KEY,
  nombre      VARCHAR(40) NOT NULL UNIQUE
);
CREATE TABLE tipo_habitacion_amenidad (
  id_tipo     VARCHAR(12) REFERENCES tipo_habitacion(id_tipo) ON DELETE CASCADE,
  id_amenidad SMALLINT    REFERENCES amenidad(id_amenidad) ON DELETE CASCADE,
  PRIMARY KEY (id_tipo, id_amenidad)
);
CREATE TABLE promocion (
  codigo      VARCHAR(20) PRIMARY KEY CHECK (codigo ~ '^[A-Z0-9]{4,20}$'),
  porcentaje  SMALLINT NOT NULL CHECK (porcentaje BETWEEN 5 AND 50),
  activa      BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE reserva (
  referencia         CHAR(10) PRIMARY KEY CHECK (referencia ~ '^LMB-[A-Z2-9]{6}$'),
  id_usuario         VARCHAR(128) REFERENCES usuario(id_usuario) ON DELETE SET NULL,
  id_tipo            VARCHAR(12) NOT NULL REFERENCES tipo_habitacion(id_tipo),
  codigo_promocion   VARCHAR(20) REFERENCES promocion(codigo),
  nombre_huesped     VARCHAR(80)  NOT NULL,
  correo_contacto    VARCHAR(254) NOT NULL,
  telefono_contacto  VARCHAR(22),
  fecha_llegada      DATE NOT NULL,
  fecha_salida       DATE NOT NULL,
  adultos            SMALLINT NOT NULL CHECK (adultos BETWEEN 1 AND 6),
  ninos              SMALLINT NOT NULL DEFAULT 0 CHECK (ninos BETWEEN 0 AND 4),
  total_eur          NUMERIC(10,2) NOT NULL CHECK (total_eur > 0),
  estado             VARCHAR(12) NOT NULL DEFAULT 'CONFIRMED' CHECK (estado IN ('CONFIRMED','CHECKED_IN','CANCELLED')),
  notas              VARCHAR(500),
  fecha_creacion     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (fecha_salida > fecha_llegada),
  CHECK (fecha_salida - fecha_llegada <= 30)
);
CREATE TABLE extra (
  id_extra      VARCHAR(16) PRIMARY KEY,
  nombre        VARCHAR(40) NOT NULL,
  precio_eur    NUMERIC(6,2) NOT NULL CHECK (precio_eur >= 0),
  unidad_cobro  VARCHAR(20) NOT NULL CHECK (unidad_cobro IN ('PERSONA_NOCHE','ADULTO','ESTANCIA','NOCHE'))
);
CREATE TABLE reserva_extra (
  referencia   CHAR(10)    REFERENCES reserva(referencia) ON DELETE CASCADE,
  id_extra     VARCHAR(16) REFERENCES extra(id_extra),
  importe_eur  NUMERIC(8,2) NOT NULL CHECK (importe_eur >= 0),
  PRIMARY KEY (referencia, id_extra)
);
CREATE TABLE parametro (
  clave                VARCHAR(40) PRIMARY KEY,
  valor                VARCHAR(160) NOT NULL,
  descripcion          VARCHAR(200),
  id_usuario_modifica  VARCHAR(128) REFERENCES usuario(id_usuario) ON DELETE SET NULL,
  fecha_modificacion   TIMESTAMP
);
CREATE TABLE auditoria (
  id_auditoria  BIGSERIAL PRIMARY KEY,
  id_usuario    VARCHAR(128) NOT NULL REFERENCES usuario(id_usuario),
  fecha_hora    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  accion        VARCHAR(60) NOT NULL,
  objetivo      VARCHAR(120) NOT NULL
);
CREATE INDEX idx_reserva_usuario ON reserva(id_usuario);
CREATE INDEX idx_reserva_fechas  ON reserva(fecha_llegada, fecha_salida);
CREATE INDEX idx_auditoria_fecha ON auditoria(fecha_hora DESC);
