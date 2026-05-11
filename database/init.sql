-- ============================================================
-- EuroCoinCollector v4 — Database Schema + 50 Real €2 Coins
-- ============================================================

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS eurocoleccion CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE eurocoleccion;

-- -----------------------------------------------------------
-- TABLA: PAIS
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS pais (
    id_pais     INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL UNIQUE,
    codigo_iso  CHAR(2)      NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- TABLA: MONEDA
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS moneda (
    id_moneda       INT AUTO_INCREMENT PRIMARY KEY,
    id_pais         INT            NOT NULL,
    nombre          VARCHAR(255)   NOT NULL,
    anyo            INT            NOT NULL,
    imagen_url      VARCHAR(512)   NULL,
    tipo            ENUM('comun','conmemorativa') NOT NULL DEFAULT 'conmemorativa',
    precio_mercado  DECIMAL(6,2)   NULL,
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- TABLA: COLECCION
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS coleccion (
    id_coleccion  INT AUTO_INCREMENT PRIMARY KEY,
    id_moneda     INT       NOT NULL UNIQUE,
    cantidad      INT       NOT NULL DEFAULT 0,
    fecha         DATE      NULL,
    notas         TEXT      NULL,
    FOREIGN KEY (id_moneda) REFERENCES moneda(id_moneda) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- TABLA: LISTA_DESEOS
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS lista_deseos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    id_moneda   INT       NOT NULL UNIQUE,
    prioridad   ENUM('alta','media','baja') NOT NULL DEFAULT 'media',
    notas       TEXT      NULL,
    FOREIGN KEY (id_moneda) REFERENCES moneda(id_moneda) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- TABLA: INTERCAMBIO
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS intercambio (
    id_intercambio      INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario      VARCHAR(100)   NOT NULL,
    id_moneda_ofrecida  INT            NOT NULL,
    id_moneda_buscada   INT            NULL,
    descripcion         TEXT           NULL,
    contacto            VARCHAR(255)   NOT NULL,
    fecha_publicacion   DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado              ENUM('activo','cerrado') NOT NULL DEFAULT 'activo',
    FOREIGN KEY (id_moneda_ofrecida) REFERENCES moneda(id_moneda) ON DELETE CASCADE,
    FOREIGN KEY (id_moneda_buscada)  REFERENCES moneda(id_moneda) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- DATOS: 19 Países emisores
-- -----------------------------------------------------------
INSERT INTO pais (id_pais, nombre, codigo_iso) VALUES
(1, 'Alemania', 'DE'),
(2, 'España', 'ES'),
(3, 'Francia', 'FR'),
(4, 'Italia', 'IT'),
(5, 'Grecia', 'GR'),
(6, 'Portugal', 'PT'),
(7, 'Austria', 'AT'),
(8, 'Bélgica', 'BE'),
(9, 'Finlandia', 'FI'),
(10, 'Luxemburgo', 'LU'),
(11, 'Países Bajos', 'NL'),
(12, 'San Marino', 'SM'),
(13, 'Vaticano', 'VA'),
(14, 'Estonia', 'EE'),
(15, 'Lituania', 'LT'),
(16, 'Letonia', 'LV'),
(17, 'Eslovenia', 'SI'),
(18, 'Malta', 'MT'),
(19, 'Chipre', 'CY');

-- -----------------------------------------------------------
-- DATOS: 50 Monedas reales de 2€
-- -----------------------------------------------------------
INSERT INTO moneda (id_pais, nombre, anyo, imagen_url, tipo, precio_mercado) VALUES
(3, 'Astérix', 2019, 'img/coins/francia_2019_asterix_v2.jpg', 'conmemorativa', 18.50),
(1, 'Caída del Muro de Berlín', 2019, 'img/coins/alemania_2019_caida_del_muro_de_be.jpg', 'conmemorativa', 2.51),
(6, '500 Años de Fernão de Magalhães', 2019, 'img/coins/portugal_2019_500_anos_de_fernao_d.jpg', 'conmemorativa', 4.17),
(9, '100 Años de la Constitución', 2019, 'img/coins/finlandia_2019_100_anos_de_la_const.jpg', 'conmemorativa', 3.99),
(3, 'Juegos Olímpicos París 2024', 2024, 'img/coins/francia_2024_juegos_olimpicos_par.jpg', 'conmemorativa', 2.76),
(8, 'Presidencia del Consejo de la UE', 2024, 'img/coins/belgica_2024_presidencia_del_cons.jpg', 'conmemorativa', 2.52),
(1, 'Elbphilharmonie de Hamburgo', 2023, 'img/coins/alemania_2023_elbphilharmonie_de_h.jpg', 'conmemorativa', 3.18),
(7, '35º Aniversario del Programa Erasmus', 2022, 'img/coins/austria_2022_35º_aniversario_del_.jpg', 'conmemorativa', 4.50),
(9, '35º Aniversario del Programa Erasmus', 2022, 'img/coins/finlandia_2022_35º_aniversario_del_.jpg', 'conmemorativa', 4.50),
(6, 'Juegos Olímpicos Tokio', 2021, 'img/coins/portugal_2021_juegos_olimpicos_tok.jpg', 'conmemorativa', 4.49),
(2, 'Parque Nacional de Garajonay', 2022, 'img/coins/espana_2022_parque_nacional_de_g.jpg', 'conmemorativa', 3.34),
(4, 'Profesiones Sanitarias', 2021, 'img/coins/italia_2021_profesiones_sanitari.jpg', 'conmemorativa', 3.54),
(5, 'Batalla de las Termópilas', 2020, 'img/coins/grecia_2020_batalla_de_las_termo.jpg', 'conmemorativa', 3.43),
(10, 'Gran Duque Henri', 2020, 'img/coins/luxemburgo_2020_gran_duque_henri.jpg', 'conmemorativa', 2.88),
(14, 'Universidad de Tartu', 2019, 'img/coins/estonia_2019_universidad_de_tartu.jpg', 'conmemorativa', 3.85),
(15, 'Sutartinės', 2019, 'img/coins/lituania_2019_sutartines.jpg', 'conmemorativa', 3.08),
(16, 'Cultura de la Suerte', 2019, 'img/coins/letonia_2019_cultura_de_la_suerte.jpg', 'conmemorativa', 4.23),
(17, 'Universidad de Ljubljana', 2019, 'img/coins/eslovenia_2019_universidad_de_ljubl.jpg', 'conmemorativa', 3.03),
(18, 'Templo de Ta’ Hagrat', 2019, 'img/coins/malta_2019_templo_de_ta_hagrat.jpg', 'conmemorativa', 3.30),
(19, '30 Años del Instituto de Neurología', 2019, 'img/coins/chipre_2019_30_anos_del_institut.jpg', 'conmemorativa', 3.09),
(3, 'Simone Veil', 2018, 'img/coins/francia_2018_simone_veil.jpg', 'conmemorativa', 2.99),
(1, 'Renania del Norte-Westfalia', 2018, 'img/coins/alemania_2018_renania_del_norte-we.jpg', 'conmemorativa', 3.52),
(4, 'Ministerio de Salud', 2018, 'img/coins/italia_2018_ministerio_de_salud.jpg', 'conmemorativa', 4.44),
(5, 'Kallipateira', 2018, 'img/coins/grecia_2018_kallipateira.jpg', 'conmemorativa', 3.55),
(10, '150 Años de la Constitución', 2018, 'img/coins/luxemburgo_2018_150_anos_de_la_const.jpg', 'conmemorativa', 2.68),
(14, 'Independencia', 2018, 'img/coins/estonia_2018_independencia.jpg', 'conmemorativa', 4.47),
(15, 'Región de Aukštaitija', 2018, 'img/coins/lituania_2018_region_de_aukstaitij.jpg', 'conmemorativa', 4.24),
(16, 'Vacas Lecheras', 2018, 'img/coins/letonia_2018_vacas_lecheras.jpg', 'conmemorativa', 3.34),
(17, 'Día Mundial de las Abejas', 2018, 'img/coins/eslovenia_2018_dia_mundial_de_las_a.jpg', 'conmemorativa', 3.50),
(18, 'Templo Mnajdra', 2018, 'img/coins/malta_2018_templo_mnajdra.jpg', 'conmemorativa', 2.95),
(2, 'Santiago de Compostela', 2018, 'img/coins/espana_2018_santiago_de_composte.jpg', 'conmemorativa', 2.84),
(4, 'Ministerio de Educación', 2017, 'img/coins/italia_2017_ministerio_de_educac.jpg', 'conmemorativa', 3.14),
(5, 'Nikos Kazantzakis', 2017, 'img/coins/grecia_2017_nikos_kazantzakis.jpg', 'conmemorativa', 2.86),
(10, 'Gran Duque Henri', 2017, 'img/coins/luxemburgo_2017_gran_duque_henri.jpg', 'conmemorativa', 3.45),
(14, 'Independencia', 2017, 'img/coins/estonia_2017_independencia.jpg', 'conmemorativa', 2.83),
(15, 'Vilna', 2017, 'img/coins/lituania_2017_vilna.jpg', 'conmemorativa', 4.13),
(16, 'Latgalian', 2017, 'img/coins/letonia_2017_latgalian.jpg', 'conmemorativa', 2.53),
(17, 'Franc Rozman', 2017, 'img/coins/eslovenia_2017_franc_rozman.jpg', 'conmemorativa', 3.53),
(18, 'Paz', 2017, 'img/coins/malta_2017_paz.jpg', 'conmemorativa', 3.28),
(19, 'Pafos Capital Europea de la Cultura', 2017, 'img/coins/chipre_2017_pafos_capital_europe.jpg', 'conmemorativa', 3.61),
(2, 'Acueducto de Segovia', 2016, 'img/coins/espana_2016_acueducto_de_segovia.jpg', 'conmemorativa', 3.26),
(4, '550 Años de Donatello', 2016, 'img/coins/italia_2016_550_anos_de_donatell.jpg', 'conmemorativa', 3.19),
(5, 'Dimitri Mitropoulos', 2016, 'img/coins/grecia_2016_dimitri_mitropoulos.jpg', 'conmemorativa', 3.44),
(10, 'Gran Duque Jean', 2016, 'img/coins/luxemburgo_2016_gran_duque_jean.jpg', 'conmemorativa', 3.80),
(14, 'Animales en Peligro', 2016, 'img/coins/estonia_2016_animales_en_peligro.jpg', 'conmemorativa', 3.78),
(15, 'Cultura Báltica', 2016, 'img/coins/lituania_2016_cultura_baltica.jpg', 'conmemorativa', 2.74),
(16, 'Vidzeme', 2016, 'img/coins/letonia_2016_vidzeme.jpg', 'conmemorativa', 3.71),
(17, '25 Años de Independencia', 2016, 'img/coins/eslovenia_2016_25_anos_de_independe.jpg', 'conmemorativa', 4.04),
(18, 'Templo Ġgantija', 2016, 'img/coins/malta_2016_templo_ggantija.jpg', 'conmemorativa', 3.78),
(19, 'Instituto de Investigación Agrícola', 2016, 'img/coins/chipre_2016_instituto_de_investi.jpg', 'conmemorativa', 3.89);
