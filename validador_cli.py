from lxml import etree
from lxml.etree import tostring
from io import StringIO
from os import listdir
from os.path import isfile, join

import sys

def get_contenido_fichero(ruta_fichero):
    
    with open(ruta_fichero, "r") as fich:
        datos=fich.read()
        return datos
    raise Exception()

def validar_dtd(text, texto_dtd):        
        try:
            #root_element=etree.fromstring(text)
            dtd=etree.DTD(StringIO(texto_dtd))
            xml=etree.XML(text)
            if dtd.validate(xml):
                return (True, "")
            else:
                error=""
                for e in dtd.error_log.filter_from_errors():
                    error=str(e)+"\n"
            return (False, error)
        except Exception as e:
            return (False, str(e))
    
def validar_xsd(text, texto_dtd):
        try:
            schema_root=etree.XML(texto_dtd)
        except Exception as e:
            return (False, str(e))
        try:
            schema=etree.XMLSchema(schema_root)
            parser=etree.XMLParser(schema=schema)
            root=etree.fromstring(text, parser)
        except Exception as e:
            return (False, str(e))
        return (True, "")

def get_ficheros_en_carpeta(carpeta):
    ficheros = [join(carpeta, f) for f in listdir(carpeta) if isfile(join(carpeta, f))]
    return ficheros

def validar_con_dtd(argv, funcion_validacion):
    carpeta_casos_buenos=argv[2]
    carpeta_casos_malos =argv[3]
    fichero_dtd_o_esquema=argv[4]

    lista_casos_buenos=get_ficheros_en_carpeta(carpeta_casos_buenos)
    texto_dtd=get_contenido_fichero(fichero_dtd_o_esquema)
    print(texto_dtd)
    for caso_bueno in lista_casos_buenos:
        #print(caso_bueno)
        texto_caso_bueno=get_contenido_fichero(caso_bueno)
        #print(texto_caso_bueno)


mecanismo_a_validar=sys.argv[1]

if sys.argv[1]=="xsd":
    validar_con_xsd(sys.argv, validar_xsd)

if sys.argv[1]=="dtd":
    validar_con_dtd(sys.argv, validar_dtd)