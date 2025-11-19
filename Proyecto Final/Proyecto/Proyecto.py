import xlwings as xw
import numpy as np
import os
import glob
from datetime import datetime, timedelta
import calendar
import pandas as pd 

def month_number_to_name(month):
    try:
        month_name = calendar.month_name[month]
        return month_name
    except IndexError:
        raise ValueError('Invalid Month Number')

def month_to_semester(month):
    if month in [1, 2, 3, 4, 5, 6]:
        return 'S1'
    elif month in [7, 8, 9, 10, 11, 12]:
        return 'S2'
    raise ValueError('Invalid Month Number')

def month_to_trimester(month):
    if month in [1, 2, 3]:
        return 'Q1'
    elif month in [4, 5, 6]:
        return 'Q2'
    elif month in [7, 8, 9]:
        return 'Q3'
    elif month in [10, 11, 12]:
        return 'Q4'
    return ValueError('Invalid Month Number')


def leer_archivo_excel(path):
    """Lee un archivo Excel y devuelve un DataFrame"""
    try:
        df = pd.read_excel(path)
        print(f"✅ Archivo leído: {os.path.basename(path)} ({len(df)} filas)")
        return df
    except Exception as e:
        print(f"❌ Error leyendo {path}: {e}")
        return pd.DataFrame()

@xw.sub
def funcion1():
    # === CONFIGURACIÓN ===
    # Carpeta donde se buscarán los archivos
    CARPETA = r"C:\Users\rbarahona\Desktop\Practica2025\Proyecto Final"

    # === ABRIR EXCEL ===
    wb = xw.Book.caller()  # Si lo ejecutas desde Excel con un botón
    ws = wb.sheets['Sheet1']  # Cambia al nombre de tu hoja      

    # === LEER DATOS DESDE EXCEL ===
    codigo_cliente = ws.range('D1').value   # O vinculado a ComboBox
    linea = ws.range('D2').value        # Segundo ComboBox
    lote = ws.range('D3').value            #Tomar en cuenta que se puede agregar mas de un lote o ninguno,

    # === CALCULAR ÚLTIMO DÍA DEL MES ANTERIOR ===
    hoy = datetime.today()
    primer_dia_mes_actual = datetime(hoy.year, hoy.month, 1)
    ultimo_dia_mes_anterior = primer_dia_mes_actual - timedelta(days=1)
    fecha_formato = ultimo_dia_mes_anterior.strftime("%Y%m%d")  # → "20250930"

    # === CONSTRUIR NOMBRES DE ARCHIVOS ===
    archivo1 = f"{codigo_cliente}_{linea}_{fecha_formato}"

    archivo2 = f"{codigo_cliente}_{linea}_{fecha_formato}_{lote}"

    # === BUSCAR ARCHIVOS EN LA CARPETA ===

    def buscar_archivo(nombre_base, carpeta):
        """
        Busca un archivo que comience con 'nombre_base' dentro de 'carpeta'
        y en todas sus subcarpetas.
        Devuelve la ruta del primer archivo encontrado, o None si no encuentra.
        """
        if nombre_base is None:
            return None
            
        patron_busqueda = os.path.join(carpeta, '**', f"{nombre_base}*")

        archivos_encontrados = glob.glob(patron_busqueda, recursive=True)

        # 3. Devolver el resultado
        if archivos_encontrados:
            # Devuelve el primer archivo que encontró
            return archivos_encontrados[0] 
        else:
            # Si la lista está vacía, no se encontró nada
            return None

    ruta1 = buscar_archivo(archivo1, CARPETA)
    ruta2 = buscar_archivo(archivo2, CARPETA)


    df1 = leer_archivo_excel(ruta1) if ruta1 else pd.DataFrame()
    df2 = leer_archivo_excel(ruta2) if ruta2 else pd.DataFrame()

     # === PROCESAR DATAFRAMES ===
    if not df2.empty:
        # Agregar columna 'Lote' con el valor del textbox
        df2["Lote"] = lote

    if not df1.empty and not df2.empty:
        # Eliminar de df1 las filas que ya están en df2 (basado en todas las columnas comunes)
        columnas_comunes = list(set(df1.columns).intersection(set(df2.columns))) #excluir columna pronostico
        print(columnas_comunes)
        if columnas_comunes:
            df1_filtrado = df1.merge(df2[columnas_comunes], on=columnas_comunes, how='left', indicator=True)
            df1_filtrado = df1_filtrado[df1_filtrado['_merge'] == 'left_only']
            df1_filtrado.drop(columns=['_merge'], inplace=True)
        else:
            # Si no hay columnas en común, no filtramos nada
            df1_filtrado = df1.copy()

        # Combinar los DataFrames
        df_final = pd.concat([df1_filtrado, df2], ignore_index=True)

    elif not df1.empty:
        df_final = df1

    COLUMNAS_FINALES = [
        "CodigoCliente", "MesCreacion", "FechaModificacion", "Fecha", "Mes", 
        "NoMes", "Año", "Semestre", "Trimestre", "Linea", "BaseTipo", 
        "BaseNumero", "Categoria", "Sublinea", "CodigoColor", "Talla", 
        "Cantidad", "Base", "OfertadoEn"
    ]

    df_db = pd.DataFrame(columns=COLUMNAS_FINALES)

    hoy = datetime.today()
    df_db['CodigoCliente'] = df_final['CodigoCliente - Cliente'].str.split('(', expand = True)[0]
    df_db['MesCreacion'] = hoy.replace(day=1, hour=0, minute=0)
    df_db['FechaModificacion'] = datetime.now()
    df_db['Fecha'] = pd.to_datetime(df_final['Año'].astype(str) + '-' +df_final['Período'].astype(str) + '-01') + pd.offsets.MonthEnd()
    df_db['Mes'] = pd.to_datetime(df_db['Fecha']).dt.month_name(locale='es_ES')
    df_db['NoMes'] = pd.to_datetime(df_db['Fecha']).dt.month
    df_db['Año'] = pd.to_datetime(df_db['Fecha']).dt.year
    df_db['Semestre'] = df_db['NoMes'].apply(month_to_semester)
    df_db['Trimestre'] = df_db['NoMes'].apply(month_to_trimester)
    df_db['Linea'] = df_final['Linea']
    df_db['BaseTipo'] = df_final['BaseTipo']
    df_db['BaseNumero'] = df_final['BaseNumero']
    df_db['Categoria'] = np.nan
    df_db['Sublinea'] = np.nan
    df_db['CodigoColor'] = df_final['CodigoColor - Color'].str.split('(', expand = True)[0]
    df_db['Talla'] = df_final['Talla']
    df_db['Cantidad'] = df_final['Pronóstico']
    df_db['Base'] = df_final['BaseTipo'] + df_final['BaseNumero'].astype(str)
    df_db['OfertadoEn'] = df_final['Lote'] #Agregar a los campos restantes el valor de Sin Filtro


    # === MOSTRAR RESULTADO EN EXCEL ===
    # (opcional) Escribirlo en una hoja nueva (si ya existe, la reemplaza)
    try:
        salida = wb.sheets['Resultado']
        salida.clear()
    except:
        salida = wb.sheets.add("Resultado", after=ws)

    salida.range("A1").value = df_db

