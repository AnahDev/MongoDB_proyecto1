import pymongo   #pip install pymongo (para instalar) 
from pymongo.errors import OperationFailure

# ==========================================
# CONFIGURACIÓN DE CONEXIÓN
# ==========================================
# Si usas Atlas (Nube), descomenta la línea de abajo y pon tu link:

client = pymongo.MongoClient("mongodb+srv://grupo_admin:Admin123456789@cluster0.jpytws2.mongodb.net/")

# Si usas Localhost (Tu PC), descomenta y usa esta:
#client = pymongo.MongoClient("<tu direccion>")

db = client["GoblalMarket"]

print("🔌 Conectado a la base de datos:", db.name)

# ==========================================
# 1. VALIDACIÓN PARA CLIENTES
# ==========================================
validator_clientes = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "segmento", "pais"],
        "properties": {
            "nombre": {
                "bsonType": "string",
                "description": "El nombre del cliente es obligatorio"
            },
            "segmento": {
                "enum": ["Consumer", "Corporate", "Home Office"],
                "description": "Solo permitimos estos 3 segmentos de negocio"
            }
        }
    }
}

try:
    print("⏳ Aplicando validación a 'clientes'...")
    db.command("collMod", "clientes", validator=validator_clientes, validationLevel="strict")
    print("✅ Validación de CLIENTES aplicada con éxito.")
except OperationFailure as e:
    print(f"❌ Error al validar clientes: {e}")


# ==========================================
# 2. VALIDACIÓN PARA ORDENES
# ==========================================
validator_ordenes = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["fecha_orden", "total_venta", "items", "cliente"],
        "properties": {
            "fecha_orden": {
                "bsonType": "string",
                "description": "La fecha es obligatoria"
            },
            "total_venta": {
                "bsonType": ["double", "int"],
                "minimum": 0,
                "description": "El total debe ser un numero positivo (mayor o igual a 0)"
            },
            "cliente": {
                "bsonType": "object",
                "required": ["id", "nombre"],
                "properties": {
                    "id": {"bsonType": "string"},
                    "nombre": {"bsonType": "string"}
                }
            },
            "items": {
                "bsonType": "array",
                "minItems": 1,
                "description": "La orden debe tener al menos un producto",
                "items": {
                    "bsonType": "object",
                    "required": ["producto_id", "cantidad", "precio_venta"],
                    "properties": {
                        "producto_id": {"bsonType": "string"},
                        "cantidad": {
                            "bsonType": "int",
                            "minimum": 1,
                            "description": "La cantidad debe ser al menos 1"
                        },
                        "precio_venta": {
                            "bsonType": ["double", "int"],
                            "minimum": 0,
                            "description": "El precio no puede ser negativo"
                        }
                    }
                }
            }
        }
    }
}

try:
    print("⏳ Aplicando validación a 'ordenes'...")
    db.command("collMod", "ordenes", validator=validator_ordenes, validationLevel="strict")
    print("✅ Validación de ORDENES aplicada con éxito.")
except OperationFailure as e:
    print(f"❌ Error al validar ordenes: {e}")

print("\n🎉 ¡Proceso finalizado!")