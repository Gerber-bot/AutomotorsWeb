# Automotors Web

Sistema web integral de gestión comercial para concesionarias automotrices, desarrollado con **Python**, **Flask** y **Microsoft SQL Server**.

> **Acreditación:** Proyecto original desarrollado por **Grupo 48** para la cátedra de Ingeniería de Software II.

---

## 📋 Descripción del Sistema

Automotors Web permite administrar el ciclo comercial completo de una concesionaria de vehículos nuevos y usados:

- **Gestión de Inventario y Catálogo:**
  - Registro de vehículos con especificaciones técnicas detalladas (motor, transmisión, dimensiones, equipamiento, historial de services).
  - Administración de marcas y servicios de postventa asociados.
  - Control de stock y estado de disponibilidad (`disponible`, `vendido`, `baja`).

- **Gestión de Clientes:**
  - Alta, baja y modificación de clientes con validación de datos de contacto.
  - Consulta de historial de compras y estado de planes de cuotas activas.
  - Reglas de integridad: bloqueo de eliminación si el cliente posee ventas asociadas.

- **Ventas y Financiación:**
  - Registro unificado de ventas con ítems mixtos (vehículos y servicios).
  - Soporte de múltiples formas de pago:
    - **Contado:** Validación estricta de totales calculados contra precios oficiales.
    - **Financiado:** Planes de 2 a 60 cuotas, cálculo de anticipos, capital, tasa de interés y cronograma de vencimientos.
  - Cancelación de operaciones con reversión automática de estados de vehículos y cuotas pendientes.

- **Seguridad y Control de Acceso:**
  - Autenticación mediante sesiones seguras con credenciales hasheadas en SHA-256.
  - Control de acceso basado en roles (`Administrador`, `Vendedor`).
  - Gestión de usuarios y roles del sistema.

- **Reportes y Respaldos:**
  - Informes operativos por rango de fechas y estado de stock de vehículos.
  - Módulo administrativo para generación de copias de seguridad de la base de datos (`.bak`).

---

## 🏗️ Arquitectura y Buenas Prácticas

El proyecto implementa una arquitectura en capas desacoplada y orientada al dominio:

- **Capa Web / Presentación (Blueprints):** Controladores Flask modulares (`app/auth`, `app/inventario`, `app/ventas`, `app/clientes`, `app/admin`, `app/reportes`, `app/cuotas`).
- **Capa de Servicios:** Lógica de negocio encapsulada con manejo transaccional explícito (`commit` / `rollback`).
- **Capa de Repositorios:** Abstracción de acceso a datos (`pyodbc`) con consultas parametrizadas y consumo de procedimientos almacenados.
- **Patrones de Diseño:**
  - **Strategy:** Resolución dinámica y validación desacoplada de pagos (`PagoContado`, `PagoFinanciado`).
  - **Dependency Injection:** Configuración de estrategias mediante contenedores (`dependency-injector`).
- **Configuración Segura:** Separación estricta de configuración y secretos mediante variables de entorno (`Config`), con fallback a claves efímeras en desarrollo.

---

## 📁 Estructura del Repositorio

```text
Automotorsweb/
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Reglas de exclusión de git (pyc, venv, secretos)
├── README.md                 # Documentación del proyecto
├── script.sql                # Script DDL de SQL Server (tablas, SPs, triggers)
└── AutomotsWeb/              # Código fuente de la aplicación Flask
    ├── config.py             # Configuración desacoplada (entorno y conexión DB)
    ├── run.py                # Entrada principal del servidor Flask
    ├── requirements.txt      # Dependencias del proyecto
    ├── app/
    │   ├── __init__.py       # Factory de la aplicación Flask (create_app)
    │   ├── db.py             # Conexión centralizada a base de datos
    │   ├── containers.py     # Contenedores de inyección de dependencias
    │   ├── admin/            # Controladores de administración, usuarios y roles
    │   ├── auth/             # Controladores de autenticación y sesiones
    │   ├── clientes/         # Controladores y vistas de clientes
    │   ├── cuotas/           # Controladores de cobranza y pagos de cuotas
    │   ├── inventario/       # Controladores de vehículos, marcas y servicios
    │   ├── reportes/         # Reportes analíticos de ventas y stock
    │   ├── ventas/           # Flujo de nueva venta y detalles de operación
    │   ├── repositorios/     # Acceso a base de datos por entidad
    │   ├── servicios/        # Lógica de negocio por módulo
    │   ├── strategies/       # Estrategias de validación de pagos
    │   ├── static/           # Archivos estáticos (CSS, JS, imágenes)
    │   └── templates/        # Plantillas Jinja2 / Bootstrap 5
    └── tests/                # Suite de pruebas automatizadas
        ├── test_app_startup.py
        ├── test_cliente_service.py
        ├── test_crear_vehiculo_error.py
        ├── test_crear_vehiculo_exitoso.py
        ├── test_estrategia_pago.py
        ├── test_registrar_venta_exitosa.py
        └── test_registrar_venta_sin_stock.py
```

---

## 🚀 Instalación y Puesta en Marcha

### Prerrequisitos

- **Python 3.10+** (probado en Python 3.13).
- **Microsoft SQL Server / SQL Express** (2019 o superior).
- **ODBC Driver 17 for SQL Server** (o driver ODBC compatible configurado).

### 1. Clonar el repositorio

```bash
git clone https://github.com/Gerber-bot/AutomotorsWeb.git
cd AutomotorsWeb
```

### 2. Crear y activar el entorno virtual

En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r AutomotsWeb/requirements.txt
```

### 4. Configurar variables de entorno

Copiar la plantilla `.env.example` a `.env`:
```powershell
Copy-Item AutomotsWeb\.env.example AutomotsWeb\.env
```

Ajustar los valores según el entorno:
- `SECRET_KEY`: Cadena aleatoria segura para proteger sesiones Flask.
- `DB_SERVER`: Servidor SQL Server (ej. `localhost\SQLEXPRESS`).
- `DB_NAME`: Nombre de la base de datos (por defecto `Automotors`).
- `DB_DRIVER`: Driver ODBC instalado (ej. `ODBC Driver 17 for SQL Server`).
- `DB_TRUSTED_CONNECTION`: `yes` para Windows Authentication, o definir `DB_USER` y `DB_PASSWORD`.

### 5. Configurar la Base de Datos (SQL Server)

1. Abrir **SQL Server Management Studio (SSMS)** o ejecutar mediante `sqlcmd`.
2. Ejecutar el archivo `script.sql` ubicado en la raíz del repositorio. Este script crea:
   - Base de datos `Automotors`.
   - Tablas principales y secundarias con claves foráneas e índices.
   - Procedimientos almacenados (`sp_InsertarCliente`, `sp_ActualizarCliente`, `sp_ObtenerClientes`).
   - Triggers de validación de vehículos antes de la venta (`trg_DV_ValidarVehiculoAntesVenta`) y actualización de totales.
3. Para insertar el primer usuario Administrador en la base de datos (con contraseña hasheada en SHA-256):

```sql
USE [Automotors];
GO

-- 1. Asegurar roles base
IF NOT EXISTS (SELECT 1 FROM Rol WHERE nombre = 'Administrador')
    INSERT INTO Rol (nombre) VALUES ('Administrador');
IF NOT EXISTS (SELECT 1 FROM Rol WHERE nombre = 'Vendedor')
    INSERT INTO Rol (nombre) VALUES ('Vendedor');

-- 2. Insertar usuario administrador inicial (password: Admin2026!)
DECLARE @id_rol_admin INT = (SELECT id_rol FROM Rol WHERE nombre = 'Administrador');
DECLARE @pwd_hash VARBINARY(256) = HASHBYTES('SHA2_256', 'Admin2026!');

IF NOT EXISTS (SELECT 1 FROM Usuario WHERE email = 'admin@automotors.local')
BEGIN
    INSERT INTO Usuario (nombre, apellido, dni, fecha_nacimiento, password_hash, email, id_rol, is_activo)
    VALUES ('Administrador', 'Principal', '00000000', '1990-01-01', @pwd_hash, 'admin@automotors.local', @id_rol_admin, 1);
END
GO
```

### 6. Ejecutar la Aplicación

```powershell
python AutomotsWeb/run.py
```

La aplicación quedará disponible en `http://localhost:5000`.

---

## 🧪 Pruebas Automatizadas

La suite incluye pruebas unitarias y de integración de servicios, estrategias de pago y arranque de la aplicación:

```powershell
python -m unittest discover -s AutomotsWeb/tests -v
```

Cobertura de pruebas:
- **Vehículo:** Creación exitosa, inserción de detalles técnicos, rollback ante VIN duplicado.
- **Venta:** Registro de venta contado, validación de stock disponible, rechazo de venta sin stock.
- **Estrategias de Pago:** Validación de montos contra precio oficial, planes de financiación válidos/inválidos, rechazo de cuotas en ventas al contado.
- **Clientes:** Inserción, actualización y bloqueo de eliminación ante ventas existentes.
- **Arranque y Seguridad:** Verificación de clave secreta, protección de rutas contra usuarios anónimos y ciclo de sesiones.

---

## 🔍 Estado de Verificación Técnica

| Componente / Flujo | Estado | Notas |
|---|---|---|
| **Sintaxis de código (57 archivos Python)** | ✅ Verificado | 100% sintaxis válida (Python 3.13). |
| **Arranque de servidor Flask** | ✅ Verificado | Mapeo de rutas y renderizado de templates comprobado. |
| **Templates HTML / Jinja2 (9 plantillas)** | ✅ Verificado | Estructura validada; etiquetas corregidas en navegación. |
| **Suite de pruebas unitarias (20 pruebas)** | ✅ Verificado | Ejecución exitosa con mocks de capa de datos. |
| **Gestión de secretos y modo debug** | ✅ Verificado | Debug desactivado por defecto; clave fija eliminada del código. |
| **Índice Git limpio de binarios (.pyc)** | ✅ Verificado | 68 archivos `.pyc` removidos del índice; `.gitignore` agregado. |
| **Conexión a SQL Server real** | ⚠️ Pendiente | No verificado contra servidor SQL Server físico en esta máquina por ausencia de servicio local; verificada compatibilidad de esquemas y queries contra `script.sql`. |
