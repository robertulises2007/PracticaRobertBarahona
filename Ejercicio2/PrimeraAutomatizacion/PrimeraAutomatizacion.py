import xlwings as xw
import random
import pandas as pd 


def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    if sheet["A1"].value == "Hello xlwings!":
        sheet["A1"].value = "Bye xlwings!"
    else:
        sheet["A1"].value = "Hello xlwings!"


@xw.sub
def my_macro():
    wb = xw.Book.caller()
    wb.sheets[0].range('A1').value = wb.name 

@xw.sub
def celda_aleatoriaform():
    wb = xw.Book.caller()
    sht = wb.sheets.active

    sht.range('A1:C10').clear()

    sht.range('E1').value = 'Num1'
    sht.range('F1').value = 'Num2'

    fila_min = 1
    fila_max = 10
    col_min = 1
    col_max = 3



    fila_aleatoria = random.randint(fila_min, fila_max)
    col_aleatoria = random.randint(col_min, col_max)

    celda = sht.range((fila_aleatoria, col_aleatoria))

    celda.value = '=SUM(E2,F2)'

    celda.select()

@xw.sub
def contador_btn():
    nombre_de_la_tabla = 'TABLE' 
    nombre_columna_contador = 'Contador'
    
    wb = xw.Book.caller()
    sht = wb.sheets.active
    

    tabla_excel = sht.tables[nombre_de_la_tabla]
        
        # Leemos solo los datos (sin encabezados) para evitar modificar el tipo de celda del encabezado
        # Usaremos el rango total para determinar el tamaño, pero leeremos solo los valores
    df = tabla_excel.range.options(pd.DataFrame, header=1, index=False).value

        # 3. Preparar los datos para la actualización
        
        # Convertir la columna a tipo numérico, forzando los errores (como texto) a NaN
    df[nombre_columna_contador] = pd.to_numeric(df[nombre_columna_contador], errors='coerce')
        
        # Sumar 1 a todos los valores (ignora automáticamente los NaN/errores)
    df[nombre_columna_contador] = df[nombre_columna_contador].fillna(0) + 1 # Rellena NaN con 0 antes de sumar
        
        # 4. Escribir la columna modificada de vuelta a Excel
        
        # Obtenemos la celda de inicio de la columna 'Contador' dentro de la tabla
        # Esto asegura que solo se sobrescriba la columna de datos
    rango_columna_datos = tabla_excel.range.columns[df.columns.get_loc(nombre_columna_contador)].resize(row_size=tabla_excel.range.rows.count - 1, column_size=1).offset(row_offset=1)
        
        # Escribir los valores de la columna de Pandas directamente al rango de datos de Excel
    rango_columna_datos.value = df[nombre_columna_contador].values.reshape(-1, 1)

@xw.sub
def reiniciar():
        
    nombre_de_la_tabla = 'TABLE'   
    nombre_columna_contador = 'Contador' 

    wb = xw.Book.caller()
    sht = wb.sheets.active

    # 1. Leer la tabla
    tabla_excel = sht.tables[nombre_de_la_tabla]
    df = tabla_excel.range.options(pd.DataFrame, header=1, index=False).value

    # 2. Generar la secuencia de ceros (Vertical)
    num_filas = len(df)
    ceros = [0] * num_filas

    # 3. Asignar los ceros a la columna del DataFrame
    df[nombre_columna_contador] = ceros

    # 4. Escribir la columna modificada de vuelta a Excel
    # Ubicamos la columna correspondiente dentro de la tabla
    col_index = df.columns.get_loc(nombre_columna_contador)

    # Creamos el rango de datos (excluyendo el encabezado)
    rango_columna_datos = (
        tabla_excel.range.columns[col_index]
        .offset(row_offset=1)  # saltar el encabezado
        .resize(row_size=num_filas, column_size=1)  # solo las filas de datos
    )

    # Escribir los ceros verticalmente (una lista de listas)
    rango_columna_datos.value = [[valor] for valor in df[nombre_columna_contador]]