import pymongo
from pymongo.errors import OperationFailure

# ==========================================
# CONFIGURACIÓN
# ==========================================
# Cambia esto si usas Atlas:
client = pymongo.MongoClient("mongodb+srv://grupo_admin:Admin123456789@cluster0.jpytws2.mongodb.net/")

db = client["GlobalMarket"]

print(f"🔌 Conectado a: {db.name}")

# ==========================================
# FUNCIÓN MAESTRA DE VALIDACIÓN
# ==========================================
def aplicar_validacion(nombre_coleccion, reglas):
    print(f"\nProcessing '{nombre_coleccion}'...")
    
    # 1. Chequeamos si la colección existe
    colecciones_existentes = db.list_collection_names()
    
    if nombre_coleccion in colecciones_existentes:
        # SI EXISTE: La modificamos (collMod)
        try:
            db.command("collMod", nombre_coleccion, validator=reglas, validationLevel="strict")
            print(f"✅ Validación ACTUALIZADA en '{nombre_coleccion}' (la colección ya existía).")
        except OperationFailure as e:
            print(f"❌ Error al actualizar: {e}")
    else:
        # NO EXISTE: La creamos (create_collection)
        try:
            db.create_collection(nombre_coleccion, validator=reglas)
            print(f"✨ Colección '{nombre_coleccion}' CREADA con validación (estaba vacía).")
        except OperationFailure as e:
            print(f"❌ Error al crear: {e}")

# ==========================================
# REGLAS (JSON SCHEMA)
# ==========================================

schema_clientes = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "segmento", "pais"],
        "properties": {
            "nombre": { "bsonType": "string" },
            "segmento": { "enum": ["Consumer", "Corporate", "Home Office"] }
        }
    }
}

schema_ordenes = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["fecha_orden", "total_venta", "items", "cliente"],
        "properties": {
            "total_venta": { "bsonType": ["double", "int"], "minimum": 0 },
            "items": { "bsonType": "array", "minItems": 1 },
            "cliente": { 
                "bsonType": "object", 
                "required": ["id", "nombre"],
                "properties": {
                    "id": {"bsonType": "string"},
                    "nombre": {"bsonType": "string"}
                }
            }
        }
    }
}

# ==========================================
# EJECUCIÓN
# ==========================================
aplicar_validacion("clientes", schema_clientes)
aplicar_validacion("ordenes", schema_ordenes)

print("\n🎉 ¡Listo! Validaciones aplicadas.")