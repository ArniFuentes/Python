from bs4 import BeautifulSoup as bs
import requests as req
import pyodbc
import datetime as dt


url = "https://www.bcentral.cl/en/home"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/80.0.3987.149 Safari/537.36"
}

cod_htlm = req.get(url, headers=headers)
parser = bs(cod_htlm.text, features='lxml')
html_found = parser.find(
    'div',
    {'class': "row justify-content-between"}
)

# Buscando el Tag
for x, y in enumerate(html_found):
    if x == 11:
        # Pasando de tipo Tag a Str
        tag_string = str(y)
        break

# Devuelve la posición (un número) tanto de > como </ en el str (como int)
position_1 = tag_string.find('$')
position_2 = tag_string.find(' \r')

# Cortando tag_string [inicio:final - 1]
dolar_str = tag_string[position_1 + 1:position_2]

# Cambiando la compa por punto
dolar_str = dolar_str.replace(',', '.')
dolar = float(dolar_str)
print(dolar)

# Instrucciones SQL
query_limpia = "delete from tabla_dolar where fecha = '%s'" % dt.date.today()
# Cuando es más de un dato se pasa en tupla
query = "insert into tabla_dolar values ('%s', %s)" % (dt.date.today(), dolar)


# Conectando con SQL Server
conexion = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-S9566PE\SQLEXPRESS;'
    'Database=TEST;'
    'Trusted_Connection=yes;'
)

cursor = conexion.cursor()
# Validación de las intrucciones
cursor.execute(query_limpia)
cursor.execute(query)
# Ejecución de las instrucciones
conexion.commit()
# Cierre de la conexión
conexion.close()

print('Dolar cargado en la tabla tipo_cambio.')

