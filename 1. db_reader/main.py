# Librerias
import mysql.connector

# Implementaciones
# schema = 'techniques' # En español
schema = 'techniques_eng' # En ingles

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database="tecnicasdb"
)

# mycursor = db.cursor()
# mycursor.execute("DESCRIBE technique")
# mycursor.execute("SELECT name, description FROM technique")
# for x in mycursor:
#     print(x)

def describe_db(database, schema):
    '''
    Describe la base de datos y sus componentes
    '''
    mycursor = database.cursor()
    mycursor.execute("DESCRIBE " + schema)
    cadena = []
    for x in mycursor:
        cadena.append(x)
        # print(x)
    # print(cadena)
    return cadena


def read_db(database, schema):
    '''
    Lee la base de datos y seleccionar todo de la tabla dada como parametro, retorna la lista completa
    '''
    mycursor = database.cursor()
    mycursor.execute("SELECT * FROM " + schema)
    cadena = []
    for i in mycursor:
        cadena.append(i)
    return cadena


#  bd descrita
d = describe_db(db, schema)

# bd leida
r = read_db(db, schema)

# for x in r:
#     print(x)

# print(len(r))
# print(r[0])

def extender(cad):
    """ Separa los campos de una fila de la de BD
    Args:
        cad (string): cadena de caracteres
    Ejem: 
        r = read_bd(bd, schema)
        extender(r)
        --
        1
        NEWLINE
        Clase Magistral
        NEWLINE
        Centrada en el docente, los alumnos son receptores de conocimientos y suelen tener la oportunidad de preguntar.
        NEWLINE
        El docente puede ofrecer una vision más equilibrada.
        A los estudiantes ofrece la oportunidad de ser motivado.
        NEWLINE
    """
    for i in range(len(cad)):
        print(cad[i])
        print('\nNEWLINE\n')



def extractor(cad):
    """ Extrae los campos que consideramos importantes para el procesamiento:
    0 -> id -> identificador
    1 -> name -> nombre de la tecnica
    3 -> utility -> tipo de utilidad
    5 -> type_learning -> tipo de aprendizaje
    Args:
        cad (string): cadena de caracteres
    Returns:
        dic: diccionario con clave -> campos elegidos| valores -> contenido de cada campo
    """
    dataline = {'id': cad[0], 'name': cad[1], 'utility': cad[3], 'type_learning': cad[5]}
    return dataline
    # print(cad[0])
    # print('\n')
    # print(cad[1])
    # print('\n')
    # print(cad[3])
    # print('\n')
    # print(cad[5])

# print(extractor(r[0])['utility'])
# print(extractor(r[0]))
# print(extractor(r[1]))

def save_csv(data_buffer):
    """ Guarda el los datos de la BD en un archivo csv
    Args:
        data_buffer (string): Datos separados de la BD
    """
    filename = 'NEW_pipes_data_test.csv'
    inputfile = open(filename, 'w', encoding='utf8')
    inputfile.write(data_buffer)
    inputfile.close()


def create_csv(data):
    """ Crea el fomato para ser guardado en csv
    Args:
        data (string): dataset
    """
    d = data
    extr = extractor(d[0])
    dataset = ''
    # cabeza
    headerline = ''
    for i in extr:
        headerline += str(i) + '|'
    headerline = headerline[:-1]
    print('headerline \n')
    print(headerline)
    # cuerpo
    dataset+=headerline + '\n'
    for line in range(0,len(d)):
        extrline = extractor(d[line])
        print('line: ', line)
        print(extrline)
        dataline = ''
        for j in extrline:
            dataline += str(extrline[j]) + '|'
        dataline = dataline[:-1]
        print(dataline)
        dataset += dataline + '\n'
    print(dataset)
    save_csv(dataset)


create_csv(r)










