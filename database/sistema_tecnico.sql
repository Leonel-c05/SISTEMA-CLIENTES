-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-08-2026 a las 04:48:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sistema_tecnico`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `cedula` varchar(15) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `cedula`, `nombre`, `apellido`, `telefono`, `direccion`, `correo`, `fecha_registro`) VALUES
(1, '081111123', 'Leonel', 'Mendoza', '0991111112', 'Esmeraldas', 'l.mendoza@gmail.com', '2026-05-20 22:08:32'),
(2, '0803456123', 'Carlos', 'Mendoza', '0998456123', 'Av. Simón Plata Torres, Esmeraldas', 'carlos.mendoza@email.com', '2026-07-28 22:03:25'),
(3, '0923456789', 'Juan', 'Paredes', '099708566', 'Barrio Las Palmas, Esmeraldas', 'juan.pareddes@gmail.com', '2026-07-28 22:04:07'),
(4, '1712345678', 'Luis', 'Morales', '0987456120', 'Barrio Aire Libre, Esmeraldas', 'luis.morales@gmail.com', '2026-07-28 22:04:50'),
(5, '0801122334', 'Fernanda', 'Solis', '099847345', 'Propicia 1, Esmeraldas', 'fernanda.solis@gmail.com', '2026-07-28 22:05:53'),
(6, '1718765432', 'Diego', 'Diaz', '099763545', 'Av Olmedo y Juan Montalvo', 'd.diaz@gmail.com', '2026-07-28 22:06:39'),
(7, '0801000001', 'Carlos', 'Mendoza', '0987654321', 'Barrio Las Palmas', 'carlos.mendoza@gmail.com', '2026-08-07 02:36:18'),
(8, '0801000002', 'Andrea', 'Zambrano', '0991234567', 'Av. Libertad', 'andrea.zambrano@gmail.com', '2026-08-07 02:36:18'),
(9, '0801000003', 'Miguel', 'Caicedo', '0969876543', 'Calle Sucre', 'miguel.caicedo@gmail.com', '2026-08-07 02:36:18'),
(10, '0801000004', 'Daniela', 'Preciado', '0984561237', 'Sector Centro', 'daniela.preciado@gmail.com', '2026-08-07 02:36:18'),
(11, '0801000005', 'Jorge', 'Estupiñán', '0976543218', 'Barrio 5 de Agosto', 'jorge.estupinan@gmail.com', '2026-08-07 02:36:18'),
(12, '0801000006', 'Valeria', 'Quiñónez', '0998765432', 'Calle Colón', 'valeria.quinonez@gmail.com', '2026-08-07 02:36:18'),
(13, '0801000007', 'Luis', 'Angulo', '0965432187', 'Barrio Codesa', 'luis.angulo@gmail.com', '2026-08-07 02:36:18'),
(14, '0801000008', 'María', 'Mina', '0987654329', 'Sector La Tolita', 'maria.mina@gmail.com', '2026-08-07 02:36:18'),
(15, '0801000009', 'Fernando', 'Páez', '0971234568', 'Av. Pedro Vicente Maldonado', 'fernando.paez@gmail.com', '2026-08-07 02:36:18'),
(16, '0801000010', 'Sofía', 'Valencia', '0994567821', 'Barrio San Rafael', 'sofia.valencia@gmail.com', '2026-08-07 02:36:18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_servicio`
--

CREATE TABLE `detalle_servicio` (
  `id_detalle` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_servicio`
--

INSERT INTO `detalle_servicio` (`id_detalle`, `id_servicio`, `id_producto`, `cantidad`, `subtotal`) VALUES
(2, 2, 20, 1, 7.50),
(3, 4, 20, 1, 7.50),
(4, 7, 20, 1, 7.50),
(5, 10, 15, 1, 48.00),
(6, 3, 14, 1, 32.00),
(7, 6, 17, 1, 38.00),
(8, 8, 22, 1, 4.00),
(9, 9, 26, 1, 6.50),
(10, 11, 21, 1, 18.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipos`
--

CREATE TABLE `equipos` (
  `id_equipo` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `tipo_equipo` varchar(50) NOT NULL,
  `marca` varchar(50) NOT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `numero_serie` varchar(100) DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  `fecha_ingreso` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `equipos`
--

INSERT INTO `equipos` (`id_equipo`, `id_cliente`, `tipo_equipo`, `marca`, `modelo`, `numero_serie`, `observaciones`, `fecha_ingreso`, `estado`) VALUES
(1, 1, 'Laptop', 'Hp', 'Pavilion', 'ABC123', 'Problemas con la tarjeta de video', '2026-05-22 11:38:43', 'Reparando'),
(2, 2, 'Laptop', 'Asus', 'VivoBook 15', 'ASUS98745', 'Lentitud del sistema', '2026-07-28 22:07:47', 'Reparando'),
(3, 3, 'Pc Escritorio', 'Dell', 'OptiPlex 3080', 'DELL308012', 'Cambio de disco SSD', '2026-07-28 22:08:53', 'Entregado'),
(4, 7, 'Laptop', 'HP', '15-DY2032LA', 'HP001TEST2026', 'Equipo utilizado para trabajo y navegación.', '2026-08-07 02:36:18', 'Recibido'),
(5, 8, 'Laptop', 'Lenovo', 'IdeaPad 3', 'LEN002TEST2026', 'Presenta lentitud durante el inicio.', '2026-08-07 02:36:18', 'En revisión'),
(6, 9, 'PC', 'Dell', 'OptiPlex 3080', 'DEL003TEST2026', 'Equipo de oficina.', '2026-08-07 02:36:18', 'Reparación'),
(7, 10, 'Laptop', 'Acer', 'Aspire 5', 'ACE004TEST2026', 'Problemas con sistema operativo.', '2026-08-07 02:36:18', 'Entregado'),
(8, 11, 'PC', 'HP', 'ProDesk 400 G6', 'HP005TEST2026', 'No enciende correctamente.', '2026-08-07 02:36:18', 'En revisión'),
(9, 12, 'Laptop', 'ASUS', 'VivoBook 15', 'ASU006TEST2026', 'Temperatura elevada.', '2026-08-07 02:36:18', 'Reparación'),
(10, 13, 'PC', 'Lenovo', 'ThinkCentre M720', 'LEN007TEST2026', 'Mantenimiento preventivo.', '2026-08-07 02:36:18', 'Entregado'),
(11, 14, 'Laptop', 'Dell', 'Inspiron 15', 'DEL008TEST2026', 'Pantalla presenta fallas.', '2026-08-07 02:36:18', 'Recibido'),
(12, 15, 'PC', 'Acer', 'Veriton X', 'ACE009TEST2026', 'Problemas de almacenamiento.', '2026-08-07 02:36:18', 'En revisión'),
(13, 16, 'Laptop', 'HP', 'Pavilion 14', 'HP010TEST2026', 'Requiere mantenimiento general.', '2026-08-07 02:36:18', 'Recibido');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_producto` int(11) NOT NULL,
  `nombre_producto` varchar(100) NOT NULL,
  `marca` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `precio` decimal(10,2) NOT NULL,
  `categoria` varchar(50) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_producto`, `nombre_producto`, `marca`, `descripcion`, `stock`, `precio`, `categoria`, `fecha_registro`) VALUES
(2, 'RTX 4060 Ventus 2X OC', 'MSI', '8 GB GDDR6', 4, 430.00, 'Tarjeta Gráfica', '2026-07-28 05:00:00'),
(3, 'Ryzen 5 5600G', 'AMD', 'Procesador 6 núcleos', 3, 165.00, 'Procesador', '2026-07-28 05:00:00'),
(4, 'Core i5-12400F', 'Intel', 'Procesador 6 núcleos', 5, 189.90, 'Procesador', '2026-07-28 05:00:00'),
(5, 'Ryzen 7 5700X', 'AMD', 'Procesador 8 núcleos', 4, 249.90, 'Procesador', '2026-07-28 05:00:00'),
(6, 'RTX 3060 12GB', 'MSI', 'Tarjeta gráfica Gaming', 2, 399.00, 'Tarjeta Gráfica', '2026-07-28 05:00:00'),
(7, 'RX 6600 8GB', 'Sapphire', 'Tarjeta gráfica AMD', 3, 289.00, 'Tarjeta Gráfica', '2026-07-28 05:00:00'),
(8, 'GTX 1650 4GB', 'ASUS', 'Tarjeta gráfica básica', 4, 185.00, 'Tarjeta Gráfica', '2026-07-28 05:00:00'),
(9, 'RAM 8GB DDR4', 'Kingston', '3200 MHz', 4, 32.00, 'Memoria RAM', '2026-07-28 05:00:00'),
(10, 'RAM 16GB DDR4', 'Corsair', '3200 MHz', 8, 58.00, 'Memoria RAM', '2026-07-28 05:00:00'),
(11, 'RAM 16GB DDR5', 'Crucial', '5600 MHz', 9, 82.00, 'Memoria RAM', '2026-07-28 05:00:00'),
(12, 'Memoria RAM 8GB DDR4', 'Kingston', 'Memoria RAM DDR4 de 8GB para equipos compatibles.', 12, 28.50, 'Memoria RAM', '2026-08-07 02:36:18'),
(13, 'Memoria RAM 16GB DDR4', 'Kingston', 'Memoria RAM DDR4 de 16GB.', 8, 45.00, 'Memoria RAM', '2026-08-07 02:36:18'),
(14, 'SSD 240GB', 'Kingston', 'Unidad de almacenamiento SSD SATA de 240GB.', 10, 32.00, 'Almacenamiento', '2026-08-07 02:36:18'),
(15, 'SSD 480GB', 'Kingston', 'Unidad de almacenamiento SSD SATA de 480GB.', 6, 48.00, 'Almacenamiento', '2026-08-07 02:36:18'),
(16, 'Disco HDD 1TB', 'Seagate', 'Disco duro mecánico SATA de 1TB.', 5, 42.00, 'Almacenamiento', '2026-08-07 02:36:18'),
(17, 'Fuente de poder 500W', 'Cooler Master', 'Fuente de alimentación de 500W.', 4, 38.00, 'Fuentes de poder', '2026-08-07 02:36:18'),
(18, 'Teclado USB', 'Logitech', 'Teclado USB estándar.', 15, 12.50, 'Periféricos', '2026-08-07 02:36:18'),
(19, 'Mouse USB', 'Logitech', 'Mouse óptico USB.', 20, 8.50, 'Periféricos', '2026-08-07 02:36:18'),
(20, 'Pasta térmica', 'Arctic', 'Pasta térmica para mantenimiento de procesadores.', 9, 7.50, 'Mantenimiento', '2026-08-07 02:36:18'),
(21, 'Ventilador para laptop', 'Generic', 'Ventilador de reemplazo para laptop.', 3, 18.00, 'Repuestos', '2026-08-07 02:36:18'),
(22, 'Cable SATA', 'Genérico', 'Cable SATA para conexión de almacenamiento.', 14, 4.00, 'Cables', '2026-08-07 02:36:18'),
(23, 'Adaptador WiFi USB', 'TP-Link', 'Adaptador inalámbrico USB.', 7, 16.00, 'Redes', '2026-08-07 02:36:18'),
(24, 'Batería para laptop', 'Green Cell', 'Batería compatible para equipos portátiles.', 4, 55.00, 'Repuestos', '2026-08-07 02:36:18'),
(25, 'Cargador universal', 'Genérico', 'Cargador universal para laptops.', 6, 30.00, 'Accesorios', '2026-08-07 02:36:18'),
(26, 'Cable HDMI', 'Genérico', 'Cable HDMI de alta velocidad.', 18, 6.50, 'Cables', '2026-08-07 02:36:18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios_tecnicos`
--

CREATE TABLE `servicios_tecnicos` (
  `id_servicio` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `falla_reportada` text NOT NULL,
  `diagnostico` text DEFAULT NULL,
  `solucion` text DEFAULT NULL,
  `estado` varchar(30) NOT NULL,
  `fecha_ingreso` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_entrega` datetime DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios_tecnicos`
--

INSERT INTO `servicios_tecnicos` (`id_servicio`, `id_equipo`, `id_usuario`, `falla_reportada`, `diagnostico`, `solucion`, `estado`, `fecha_ingreso`, `fecha_entrega`, `costo`) VALUES
(2, 4, 3, 'El equipo presenta lentitud general.', 'Se detectó acumulación de archivos temporales y programas innecesarios.', 'Limpieza del sistema y optimización de inicio.', 'Entregado', '2026-08-07 02:36:18', '2026-07-29 00:00:00', 25.00),
(3, 5, 3, 'El equipo demora demasiado en iniciar.', 'Se encontró saturación del almacenamiento.', 'Limpieza y optimización del sistema.', 'En revisión', '2026-08-07 02:36:18', NULL, 20.00),
(4, 6, 3, 'El equipo se apaga inesperadamente.', 'Se detectó problema relacionado con temperatura.', 'Limpieza interna y mantenimiento del sistema de refrigeración.', 'Reparación', '2026-08-07 02:36:18', NULL, 35.00),
(5, 7, 3, 'El sistema operativo presenta errores.', 'Archivos del sistema dañados.', 'Reparación y actualización del sistema operativo.', 'Entregado', '2026-08-07 02:36:18', '2026-07-22 00:00:00', 40.00),
(6, 8, 3, 'El computador no enciende.', 'Se detectó problema en la alimentación eléctrica.', 'Revisión de fuente de poder y conexiones.', 'En revisión', '2026-08-07 02:36:18', NULL, 30.00),
(7, 9, 3, 'La laptop se calienta demasiado.', 'Sistema de refrigeración con acumulación de polvo.', 'Limpieza interna y cambio de pasta térmica.', 'Reparación', '2026-08-07 02:36:18', NULL, 35.00),
(8, 10, 3, 'Mantenimiento preventivo.', 'Equipo con acumulación de polvo y archivos innecesarios.', 'Limpieza física y optimización del sistema.', 'Entregado', '2026-08-07 02:36:18', '2026-07-17 00:00:00', 30.00),
(9, 11, 3, 'La pantalla presenta fallas.', 'Se detectó problema en la conexión del display.', 'Revisión de cableado interno de pantalla.', 'Recibido', '2026-08-07 02:36:18', NULL, 45.00),
(10, 12, 3, 'El equipo funciona lentamente.', 'Unidad de almacenamiento con bajo rendimiento.', 'Diagnóstico de disco y revisión de almacenamiento.', 'En revisión', '2026-08-07 02:36:18', NULL, 25.00),
(11, 13, 3, 'Mantenimiento general de laptop.', 'Se encontró polvo acumulado y sistema desactualizado.', 'Mantenimiento preventivo y actualización.', 'Recibido', '2026-08-07 02:36:18', NULL, 30.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `rol` varchar(30) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `usuario`, `correo`, `password`, `rol`, `fecha_creacion`) VALUES
(3, 'Leonel Cepeda', 'l.cepeda', 'leofer2334@gmail.com', 'scrypt:32768:8:1$wUhiPD5Pbd8Gv3GK$05410457ce8727b754fb6bad1152b6fbbc62ff1b3bb752c02d6f9604605e74f7d8dcc973d7728d8002d8cb019a9619242a8215d41da77d75b261449ed817e42b', 'Técnico', '2026-08-06 05:00:00'),
(4, 'Administrador', 'admin', 'admin@sistema.com', 'scrypt:32768:8:1$GXLOIBybGLEl3XTc$1bca9411d36abe36492b3176d8a42197d42b89d3ef1438d6f4bfae443b229480f086c305d97fa617f8078d0cb95441a43a04b548e7768935497def17ca91c9fb', 'Administrador', '2026-08-06 05:00:00'),
(5, 'prueba', 'prueba', 'pruebatesis7@gmail.com', 'scrypt:32768:8:1$NBcj4MT3N30WJDcL$b85567458bc2fd29f349d80fc1b9de750063f6d37108ce90cffb63209a998a70f7feeafcded511437b7a7c459f196a8ba96fd366bdd2539ac6f7891b6cf1e805', 'Técnico', '2026-08-06 05:00:00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `cedula` (`cedula`);

--
-- Indices de la tabla `detalle_servicio`
--
ALTER TABLE `detalle_servicio`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `fk_detalle_servicio` (`id_servicio`),
  ADD KEY `fk_detalle_producto` (`id_producto`);

--
-- Indices de la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD PRIMARY KEY (`id_equipo`),
  ADD KEY `fk_equipo_cliente` (`id_cliente`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `servicios_tecnicos`
--
ALTER TABLE `servicios_tecnicos`
  ADD PRIMARY KEY (`id_servicio`),
  ADD KEY `fk_servicio_equipo` (`id_equipo`),
  ADD KEY `fk_servicio_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `detalle_servicio`
--
ALTER TABLE `detalle_servicio`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `equipos`
--
ALTER TABLE `equipos`
  MODIFY `id_equipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `servicios_tecnicos`
--
ALTER TABLE `servicios_tecnicos`
  MODIFY `id_servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_servicio`
--
ALTER TABLE `detalle_servicio`
  ADD CONSTRAINT `fk_detalle_producto` FOREIGN KEY (`id_producto`) REFERENCES `inventario` (`id_producto`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_detalle_servicio` FOREIGN KEY (`id_servicio`) REFERENCES `servicios_tecnicos` (`id_servicio`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD CONSTRAINT `fk_equipo_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `servicios_tecnicos`
--
ALTER TABLE `servicios_tecnicos`
  ADD CONSTRAINT `fk_servicio_equipo` FOREIGN KEY (`id_equipo`) REFERENCES `equipos` (`id_equipo`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_servicio_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
