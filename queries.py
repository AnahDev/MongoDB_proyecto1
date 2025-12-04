import pymongo #pip install pymongo (para instalar)
import pprint # Para imprimir los resultados de forma bonita

# ==========================================
# CONFIGURACIÓN DE CONEXIÓN
# ==========================================
# Opción A: Si usas Localhost (Tu PC)
#client = pymongo.MongoClient("mongodb://localhost:27017/")

# Opción B: Si usas Atlas (Nube), descomenta y usa tu link:
client = pymongo.MongoClient("mongodb+srv://grupo_admin:Admin123456789@cluster0.jpytws2.mongodb.net/")

db = client["GlobalMarket"]
collection = db["ordenes"]

print(f"🔌 Conectado a: {db.name} -> Colección: {collection.name}\n")

# ==========================================
# 1. AGREGACIÓN: REPORTE DE VENTAS
# ==========================================
pipeline_reporte_ventas = [
  {
    '$addFields': {
      'fecha_obj': {
        '$toDate': '$fecha_orden'
      }
    }
  }, {
    '$group': {
      '_id': {
        'mes': { '$month': '$fecha_obj' }, 
        'anio': { '$year': '$fecha_obj' }
      }, 
      'total_vendido': { '$sum': '$total_venta' }, 
      'cantidad_ordenes': { '$sum': 1 }
    }
  }, {
    '$sort': {
      '_id.anio': 1, 
      '_id.mes': 1
    }
  }
]

print("📊 --- EJECUTANDO REPORTE DE VENTAS (Por Mes) ---")
try:
    resultados = list(collection.aggregate(pipeline_reporte_ventas))
    for doc in resultados:
        print(f"Fecha: {doc['_id']['mes']}/{doc['_id']['anio']} | Total: ${doc['total_vendido']:.2f} | Ordenes: {doc['cantidad_ordenes']}")
except Exception as e:
    print(f"Error: {e}")
print("\n" + "="*50 + "\n")


# ==========================================
# 2. AGREGACIÓN: TOP PRODUCTOS VENDIDOS
# ==========================================
pipeline_top_productos = [
  {
    '$unwind': { 'path': '$items' }
  }, {
    '$group': {
      '_id': '$items.nombre_producto', 
      'total_vendido': { '$sum': '$items.cantidad' }, 
      'ganancia_promedio': { '$avg': '$items.ganancia' }
    }
  }, {
    '$match': {
      'total_vendido': { '$gte': 50 }
    }
  }, {
    '$sort': { 'ganancia_promedio': -1 }
  },
  { '$limit': 5 } # Limitamos a 5 para no llenar la pantalla
]

print("🏆 --- EJECUTANDO TOP PRODUCTOS (Más de 50 vendidos) ---")
try:
    resultados = list(collection.aggregate(pipeline_top_productos))
    for i, doc in enumerate(resultados, 1):
        print(f"{i}. {doc['_id']} | Vendidos: {doc['total_vendido']} | Ganancia Avg: ${doc['ganancia_promedio']:.2f}")
except Exception as e:
    print(f"Error: {e}")
print("\n" + "="*50 + "\n")


# ==========================================
# 3. AGREGACIÓN: BUCKET PATTERN (Rangos de Precio)
# ==========================================
pipeline_bucket = [
  {
    '$unwind': { 'path': '$items' }
  }, {
    '$bucket': {
      'groupBy': '$items.precio_total_linea', 
      'boundaries': [ 0, 50, 200, 1000, 5000 ], 
      'default': 'Otros', 
      'output': {
        'cantidad_productos': { '$sum': 1 }, 
        # Nota: Comenté 'ejemplos' para que la consola no explote de texto, 
        # pero el cálculo se hace igual. Si quieres verlos, descomenta la linea de abajo.
        # 'ejemplos': { '$push': '$items.nombre_producto' } 
      }
    }
  }
]

print("🏷️  --- EJECUTANDO BUCKET PATTERN (Rangos de Precio) ---")
try:
    resultados = list(collection.aggregate(pipeline_bucket))
    for doc in resultados:
        print(f"Rango: {doc['_id']} | Cantidad de Productos: {doc['cantidad_productos']}")
except Exception as e:
    print(f"Error: {e}")

print("\n✅ Consultas finalizadas.")