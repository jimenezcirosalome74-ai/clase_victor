import pandas as pd
import glob 

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
for archivos in archivos_csv:
    df=pd.read_csv(archivos)
    lista_informes.append(df)
    print(f"leidos:{archivos} - {len(df)}filas")

for archivo in archivos_excel:
    df=pd.read_excel(archivo)
    lista_informes.append(df)
    print(f"leido:{archivo} - {len(df)}filas")

#UNIFICAR LOS DATAFRAMES 
df_consolidado =pd.concat(lista_informes, ignore_index =True)
print (df_consolidado)

#RESOLVER RENOMBRANDO COLUMNAS DE BOGOTA 
for i, df in enumerate (lista_informes):
    if 'Fecha_Venta' in df.columns:
        lista_informes [i] = df.rename(columns={
            "Fecha_Venta":"fecha","Producto":"producto","Categoria":"categoria",
            "Cant":"cantidad","Valor_Unitario":"precio_unitario",
            "Vendedor":"vendedor","pago":"metodo_pago"
        })

df_consolidado =pd.concat(lista_informes,ignore_index=True)
print(df_consolidado)

