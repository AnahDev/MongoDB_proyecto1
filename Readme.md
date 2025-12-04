# Proyecto de Migración NoSQL: E-commerce Analytics

## Descripción del Proyecto

Este proyecto consiste en la migración de un dataset transaccional relacional (`Global_Superstore2.csv`) a una base de datos documental en **MongoDB**. El objetivo es optimizar el rendimiento de lectura para un dashboard de E-commerce y asegurar la integridad de los datos mediante validaciones JSON Schema.

## Arquitectura de Datos (Modelado)

Se implementó una **Estrategia Híbrida** para balancear rendimiento y flexibilidad:

1.  **Colección `ordenes` (Embedding):**
    - Utilizamos el patrón de **Documentos Embebidos** para los productos (`items`) dentro de cada orden.
    - _Razón:_ Mejora el rendimiento de lectura (evita JOINs) al consultar el historial de una compra.
2.  **Colección `clientes` (Referencing):**

    - Utilizamos **Referencias** para los datos del cliente.
    - _Patrón Extended Reference:_ Guardamos el `id` y `nombre` del cliente dentro de la orden para evitar lookups frecuentes, pero mantenemos el perfil completo (dirección, segmento) en su propia colección.

3.  **Colección `productos`:**
    - Catálogo maestro utilizado para búsquedas difusas (Atlas Search).

## Requisitos Previos

- MongoDB Atlas (Cluster M0 Gratuito)
- MongoDB Compass
- Python 3.x (con librería pandas)

## Instrucciones de Instalación

### 1. Transformación de Datos (ETL)

Ejecutar el script de Python incluido (`convertir_datos.py`) para transformar el CSV plano en documentos JSON estructurados:

```bash
python convertir_datos.py
```

# Esto generará los archivos: ordenes.json, clientes.json, productos_catalogo.json.

2. Importación
   Utilizar MongoDB Compass para importar los archivos JSON generados en la base de datos EcommerceStore.

3. Aplicar Validaciones
   Ejecutar el script validation.js en la consola de Mongo (Mongosh) para establecer las reglas de integridad (precios positivos, campos obligatorios).

4. Consultas y Visualización
   Las consultas de agregación se encuentran en queries.js.

# El Dashboard visual está disponible en MongoDB Atlas Charts.#
