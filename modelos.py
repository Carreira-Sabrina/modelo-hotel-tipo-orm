from conexion_bd import conexion

#Super-clase de todos los modelos de la base de datos
class Modelo():
    #Comunes a todas las instancias de la clase
    cnx = conexion
    tabla = None # El modelo "abstracto no tiene tabla ni campos, cada clase define los suyos"
    campos = None # Idem
    
    #Constructor, se hereda, cuidado que no haya alguna clase que no tenga que sobreescribirlo
    def __init__(self,*args,id=None):
        if id:
            for campo, valor in zip(self.campos, args[0]):
                setattr(self, campo, valor) 
        else:
            for campo, valor in zip(self.campos[1:], args):
                setattr(self, campo, valor) 
    
    @classmethod
    def obtener_todos_de_tabla(cls):
        #Primero conectar con la base de datos, la conexion se abre y se cierra sucesivamente
        cls.cnx.connect()
        #Crear cursor
        cursor = cls.cnx.cursor()
        consulta = f"SELECT * FROM {cls.tabla}"
        cursor.execute(consulta)
        resultado_consulta = cursor.fetchall()
        cls.cnx.close()
        #Cuidado ! Por ahora esto devuelve tuplas, no objetos de una clase ! 
        # Como hago para que cada clase devuelva un objeto de si misma si ahora estoy en una super clase?
        # IGUAL COMO QUE ACÁ DEBERIA DEVOLVER POR EJEMPLO UN ARRAY DE OBJETOS, SON VARIOS, NO UNO SOLO !!!!!!!!!!!
        # LA CLAVE PUEDE ESTAR EN LLAMAR A UN CONSTRUCTOR pero estoy en un metodo de clase _/ '_' \_
        return resultado_consulta
    
    @classmethod
    def obtener_elemento_por_campo(cls,campo,valor_a_buscar): #LALALALALA
        
        #EL PARAMETRO CAMPO ME PERMITE IR UN POQUITO MAS ALLA, PUEDO PASAR UN NOMBRE DE COLUMNA CUALQUIERA !!! 
        
        #Primero conectar con la base de datos, la conexion se abre y se cierra sucesivamente
        cls.cnx.connect()
        #Crear cursor
        cursor = cls.cnx.cursor()
        
        #Trato de sacar las comillas del campo y cambiarlas por backticks como hizo el profe, PERO ACORDARME DE PASAR EL PARAMETRO COMO COMILLAS SIMPLES !
        campo = str(campo).replace("'","`")
        
        consulta = f"SELECT * FROM {cls.tabla} WHERE {campo} = %s;"
        parametros_consulta = (valor_a_buscar,) #esto va como tupla
        cursor.execute(consulta,parametros_consulta)
        resultado_consulta = cursor.fetchone()
        cls.cnx.close()
        #Cuidado ! Por ahora esto devuelve tuplas, no objetos de una clase !
        return resultado_consulta

    @classmethod 
    def eliminar_elemento(cls,id):
        pass
    
    @classmethod
    def modificar_elemento(cls,id):
        pass
    

    #Lo más trabajoso es la construcción dinamica de los campos a insertar y la generacion dinámica de placeholders...    
    def insertar_en_tabla_bd(self):
        # Una consulta no dinámica es del tipo "INSERT INTO nombre_tabla (col1,col2,) VALUES(%s,%s)" A los "%s" se les llama "placeholders"
        # Aquí nos encontramos con el problema que cada modelo tiene una cantidad diferente de columnas, con nombres distintos. Al ser variable la cantidad de columnas, debe serlo
        # también la cantidad de placeholders. 
        # Los nombres de las columnas provienen del atributo de clase campos
        # Un poco más de trabajo y logro convertir el plomo en oro jajajajajajaja
        
        self.cnx.connect()
        cursor = self.cnx.cursor()
        
        # Estas 4 lineas generan la cantidad necesaria de placeholders para la tabla
        placeholder=('%s',) #Hay que ponerlo entre comillas para que no de error, se retiran despues 
        cuantos_placeholders= len(self.campos) - 1 # Necesito un placeholder menos porque no guardo el id en la tabla ! (Es un placeholder por cada valor a insertar)
        placeholders = tuple(placeholder*cuantos_placeholders) # Tupla de '%s' repetido la cantidad necesaria
        formato_values_consulta = "VALUES " + str(placeholders).replace("'","") #Hay que sacarle las comillas a '%s', para eso sirve replace
        
        # La funcion vars() devuelve un diccionario con pares atributo-valor, de aqui se obtienen dinamicamente los valores de los atributos a insertar en la consulta! 
        valores_parametro_consulta = tuple(vars(self).values())
        
        #Se seleccionan de la tupla todos los campos menos el id 
        campos_a_insertar = str(self.campos[1:]).replace("'", "`")
        
        # Consulta SQL
        consulta_insertar = """ INSERT INTO %s %s %s""" %(self.tabla,campos_a_insertar,formato_values_consulta)
        
        print("000000 VEAMOS SI LA CONSULTA SE HA GENERADO CORRECTAMENTE 00000")
        print(consulta_insertar)
        
        cursor.execute(consulta_insertar,valores_parametro_consulta)
        self.cnx.commit()
        self.cnx.close()




#Cliente
class Cliente(Modelo):
    #Comunes a todas las instancias de la clase (a la conexion la herede de la super clase)
    #tabla = "clientes"
    tabla = "cliente"
    campos = ('id','nombre','apellido','celular','email') #Ojo porque esto se va a romper si no se cambian las comillas por backticks

    #Es muy loco pero creo que esto me puede servir
    clave_primaria = campos[0] # no tendre que cambiar comillas por backticks?

                
            
            
    def __repr__(self): 
        return f"El nombre del cliente es {self.nombre}, su apellido es {self.apellido} ,su celular es {self.celular}, y su mail es {self.email}"
    
    
#Habitacion
class Habitacion:
    tabla = "habitacion"
    campos = ('id','nombre','categoria','precio_por_dia') #Ojo porque esto se va a romper si no se cambian las comillas por backticks
        
    #Constructor
    #NO LO PUEDO TRAER DE LA SUPERCLASE?
        
    def __repr__(self): 
        return f"El nombre de la habitacion es {self.nombre}, es de categoría {self.categoria} y cuesta $ {self.precio_por_dia} por día"
        


#Reserva CUIDADO ! ESTA CLASE TIENE FOREINGN KEYS, NECESITA SABER ID DE CLIENTES E ID DE HABITACIONES !
class Reserva:
    tabla = "reserva"
    campos = ('id','id_habitacion','id_cliente','fecha_ingreso','fecha_egreso') #Ojo porque esto se va a romper si no se cambian las comillas por backticks
        
    #Constructor
    #NO LO PUEDO TRAER DE LA SUPERCLASE?
        
    def __repr__(self): 
        return f"El nombre de la reserva es {self.id}" #Cuidado con esto ! 
        