import pandas as pd
import json

# 1. Cargar el CSV (Intenta detectar la codificación correcta)
try:
    df = pd.read_csv('Global_Superstore2.csv', encoding='latin1')
except:
    df = pd.read_csv('Global_Superstore2.csv')

print("Procesando datos... esto puede tardar unos segundos.")

# --- PARTE 1: CLIENTES (Colección 'clientes') ---
# Estrategia: Referencing. Extraemos clientes únicos para no repetir datos.
customers_df = df[['Customer ID', 'Customer Name', 'Segment', 'City', 'State', 'Country', 'Postal Code', 'Market', 'Region']].drop_duplicates(subset='Customer ID')
# Renombramos columnas a formato snake_case (mejor práctica en MongoDB)
customers_df.columns = ['_id', 'nombre', 'segmento', 'ciudad', 'estado', 'pais', 'codigo_postal', 'mercado', 'region']

# Guardar clientes.json
customers_df.to_json('clientes.json', orient='records', indent=2)
print(f"✔ Generado 'clientes.json' con {len(customers_df)} clientes únicos.")


# --- PARTE 2: PRODUCTOS (Colección 'productos') ---
# Estrategia: Catálogo Maestro.
products_df = df[['Product ID', 'Category', 'Sub-Category', 'Product Name']].drop_duplicates(subset='Product ID')
products_df.columns = ['_id', 'categoria', 'sub_categoria', 'nombre']

# Guardar productos_catalogo.json
products_df.to_json('productos_catalogo.json', orient='records', indent=2)
print(f"✔ Generado 'productos_catalogo.json' con {len(products_df)} productos únicos.")


# --- PARTE 3: ÓRDENES (Colección 'ordenes') ---
# Estrategia: Embedding (Items) + Extended Reference (Cliente).

# Agrupamos por ID de Orden
grouped = df.groupby('Order ID')
orders_list = []

for order_id, group in grouped:
    first_record = group.iloc[0] # Tomamos los datos comunes de la primera fila
    
    # Lista de items (Embedding)
    items = []
    for _, row in group.iterrows():
        items.append({
            "producto_id": row['Product ID'],
            "nombre_producto": row['Product Name'],
            "cantidad": int(row['Quantity']),
            "precio_total_linea": float(row['Sales']), 
            "descuento": float(row['Discount']),
            "ganancia": float(row['Profit'])
        })
    
    # Construimos el documento de la orden
    order_doc = {
        "_id": order_id,
        "fecha_orden": first_record['Order Date'], # Ojo: MongoDB Compass lo detectará como String, puedes convertirlo a Date allá o aquí.
        "fecha_envio": first_record['Ship Date'],
        "prioridad": first_record['Order Priority'],
        # Extended Reference: Guardamos ID y Nombre para consultas rápidas
        "cliente": {
            "id": first_record['Customer ID'], 
            "nombre": first_record['Customer Name'] 
        },
        "envio": {
            "modo": first_record['Ship Mode'],
            "costo_total": float(group['Shipping Cost'].sum())
        },
        "total_venta": float(group['Sales'].sum()), # Total calculado
        "items": items # Aquí va el array embebido
    }
    orders_list.append(order_doc)

# Guardar ordenes.json
with open('ordenes.json', 'w', encoding='utf-8') as f:
    json.dump(orders_list, f, indent=2, ensure_ascii=False)

print(f"✔ Generado 'ordenes.json' con {len(orders_list)} órdenes consolidadas.")
print("¡Listo! Ahora importa estos 3 archivos en MongoDB Compass.")