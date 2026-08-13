import pandas as pd
import glob 
import matplotlib.pyplot as plt

#Exploracion de los datos y diferentes tipos de archivos 
#.csv y xlsx

df_medellin = pd.read_csv("sucursal_medellin.csv")
#print(df_medellin.head(3))

df_bogota = pd.read_excel ("sucursal_bogota.xlsx")
#print(df_bogota.head(3))
#print(df_bogota.columns)
#print(df_medellin.columns)

#AGRUPAR ARCHIVOS POR TIPO .CSV Y XLSX
archivos_csv=glob.glob ("*.csv")
archivos_excel=glob.glob ("*.xlsx")

#print (archivos_csv)

#UNIFICAR DATAFRAMES EN UNA LISTA 
lista_informes=[]

# Columnas finales esperadas (7 columnas)
columnas_finales = [
    "fecha",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "vendedor",
    "metodo_pago",
]

for archivo in archivos_csv:
  df = pd.read_csv(archivo)

  # Si el CSV tiene los nombres viejos, se renombran directamente
  if "Fecha_Venta" in df.columns:
    df = df.rename(
        columns={
            "Fecha_Venta": "fecha",
            "Producto": "producto",
            "Categoria": "categoria",
            "Cant": "cantidad",
            "Valor_Unitario": "precio_unitario",
            "Vendedor": "vendedor",
            "pago": "metodo_pago",
        }
    )

    lista_informes.append(df)
    print(f"Leído CSV: {archivo} - {len(df)} filas")
    

# 2. Leer Excels (renombrando las columnas específicas de Bogotá/Excel)
for archivo in archivos_excel:
  df = pd.read_excel(archivo)

  # Renombrar columnas específicas
  df = df.rename(
      columns={
          "Fecha_Venta": "fecha",
          "Producto": "producto",
          "Categoria": "categoria",
          "Cant": "cantidad",
          "Valor_Unitario": "precio_unitario",
          "Vendedor": "vendedor",
          "pago": "metodo_pago",
      }
  )
  lista_informes.append(df)
  print(f"Leído Excel: {archivo} - {len(df)} filas")

#UNIFICAR LOS DATAFRAMES 
df_consolidado =pd.concat(lista_informes, ignore_index =True)
# 4. Asegurar exactamente las 7 columnas y eliminar duplicadas/extra
df_consolidado = df_consolidado[columnas_finales]

print("\n--- CONSOLIDACIÓN INICIAL ---")
print(df_consolidado.info())

# --------------------------------------------
# PARTE 4: Limpieza de datos (NUEVO)
# --------------------------------------------

# 4a. Eliminar filas duplicadas
filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
print(f"\nFilas antes: {filas_antes} - despues: {len(df_consolidado)}")

# 4b. Explorar valores nulos ANTES de decidir qué hacer
print("\nValores nulos por columna (ANTES):")
print(df_consolidado.isnull().sum())

# 4c. Rellenar según el tipo de columna
# Estrategia de imputación recomendada según el tipo de dato:
valores_imputacion = {
    # Categóricas / Texto -> 'Sin Información' o 'Desconocido'
    "producto": "Desconocido",
    "categoria": "Sin Categoría",
    "vendedor": "Sin Asignar",
    "metodo_pago": "No Especificado",
    # Numéricas -> 0 o el valor promedio/mediana
    "cantidad": 0,
    "precio_unitario": 0,
    # Fechas -> Conservar o rellenar con un valor por defecto si aplica
    "fecha": "Sin Fecha",
}

# Aplicar el rellenado de nulos
df_consolidado = df_consolidado.fillna(valores_imputacion)

# Verificación final
print("\nValores nulos por columna (DESPUÉS):")
print(df_consolidado.isnull().sum())

print("\n--- DATAFRAME CONSOLIDADO Y LIMPIO ---")
print(df_consolidado.head())
# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
df_consolidado.to_excel("consolidado_limpio.xlsx", index=False)
print("Archivo guardado")

# --------------------------------------------
# PREGUNTA 1: ¿Cuánto vendió cada categoría en total?
# (EJEMPLO RESUELTO)
# --------------------------------------------
ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
print(ventas_categoria)

ventas_categoria.plot(kind='bar', title='Ventas por Categoria')
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel('Ventas totales ($)')
plt.xlabel('Categoría')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_categoria.png")
plt.show()

# --------------------------------------------
# PREGUNTA 2: ¿Qué porcentaje de las ventas representa 
# cada vendedor?
# --------------------------------------------
ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
print(ventas_vendedor)
ventas_vendedor.plot(
    kind='pie',
    autopct='%1.1f%%',
    title='Porcentaje de Ventas por Vendedor'
)

plt.ylabel('')
plt.tight_layout()

plt.savefig("grafico_vendedor.png")

plt.show()

# --------------------------------------------
# PREGUNTA 3: ¿Cuál es el producto que más se vende?
# --------------------------------------------
productos_vendidos = df_consolidado['producto'].value_counts()
print(productos_vendidos)
# Paso 3: impriman el resultado

# --------------------------------------------
# PREGUNTA 4: ¿Cómo se distribuyen las ventas según 
# el método de pago?
# --------------------------------------------
metodo_pago = df_consolidado.groupby('metodo_pago')['precio_unitario'].sum()
print(metodo_pago)
metodo_pago.plot(
    kind='pie',
    autopct='%1.1f%%',
    title='Distribución de Ventas por Método de Pago'
)

plt.ylabel('')
plt.tight_layout()

plt.savefig("grafico_metodo_pago.png")

plt.show()


# --------------------------------------------
# PREGUNTA 5: ¿Cuál es el día de la semana con más ventas?
# --------------------------------------------

df_consolidado["fecha"] = pd.to_datetime(
    df_consolidado["fecha"],
    errors="coerce"
)

df_consolidado["dia_semana"] = df_consolidado["fecha"].dt.day_name()

ventas_dia = df_consolidado.groupby("dia_semana")["precio_unitario"].sum()

print("--- VENTAS POR DÍA DE LA SEMANA ---")
print(ventas_dia)

dia_mayor_venta = ventas_dia.idxmax()
mayor_venta = ventas_dia.max()

print(f"El día de la semana con más ventas es: {dia_mayor_venta}")
print(f"Total de ventas: ${mayor_venta:,.0f}")