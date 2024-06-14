import mysql.connector

#Parámetros de conexión para el desarrollo
bd_config_dev ={
    "user": "root",
    "password": "0pt1mu5Pr1m3",
    "host": "localhost",
    "database":"hotel"
    
}

#Puedo cambiar de base de datos para no "estropear" la base de datos original y hacer mis pruebas chungas jajajaja
bd_config_dummy = {
    "user": "root",
    "password": "0pt1mu5Pr1m3",
    "host": "localhost",
    "database":"dummy"
}



#Conectar con la BD 
#base_de_datos =mysql.connector.connect(host="localhost",user="root",password = "0pt1mu5Pr1m3",database="hotel")
#se ponen ** antes del diccionario pasado como parámetro para que lo tome como **kwargs
conexion =mysql.connector.connect(**bd_config_dummy)