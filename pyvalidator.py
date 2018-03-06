#!/usr/bin/env python3
#coding=utf-8
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.ttk import *
from tkinter.font import Font


from lxml import etree
from lxml.etree import tostring

from io import StringIO
import string

DTD_INICIAL="""<!ELEMENT listaclientes (cliente+)>
<!ELEMENT cliente (cif, nombre, diasentrega?)>
<!ELEMENT cif (#PCDATA)>
<!ELEMENT nombre (#PCDATA)>
<!ELEMENT diasentrega (#PCDATA)>
"""
INICIAL="""<?xml version="1.0"?>
<listaclientes>
	<cliente>
		<cif>3</cif>
		<nombre>Juan Diaz</nombre>
	</cliente>
	<cliente>
		<cif>5</cif>
		<nombre>Juan Diaz</nombre>
		<diasentrega>6</diasentrega>
	</cliente>
</listaclientes>
"""


DTD_INICIAL="""
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <xsd:element name="a" type="xsd:integer"/>
</xsd:schema>
"""
INICIAL="""
<a>no int</a>
"""


DTD_INICIAL="""<xsl:stylesheet version="1.0"
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
     <xsl:template match="/">
         <bar><foo><xsl:value-of select="/a/b/text()" /></foo></bar>
     </xsl:template>
 </xsl:stylesheet>
"""
INICIAL="""<a><b>Text</b></a>
"""


DTD_INICIAL="""
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head><title>Catalogo</title></head>
            <body>
                <h1>Autores</h1>
                <ul>
                    <xsl:for-each select="//autor">
                        <xsl:sort select="." order="descending"/>
                        <li><xsl:value-of select="."/></li>
                    </xsl:for-each>
                </ul>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
"""

INICIAL="""
<inventario>
    <producto codigo="AAA-111">
        <nombre>Teclado</nombre>
        <peso unidad="g">480</peso>
    </producto>
    <producto codigo="ACD-981">
        <nombre>Monitor</nombre>
        <peso unidad="kg">1.8</peso>
    </producto>
    <producto codigo="DEZ-138">
        <nombre>Raton</nombre>
        <peso unidad="g">50</peso>
    </producto>
</inventario>
"""


#DTD_INICIAL="/inventario/producto[1]"
INICIAL=""
class Validator(object):
    def __init__(self):
        self.almacenar_en_fichero=True
        self.nombre_fichero_resultado="resultado_xslt"
        self.main_window=Tk()
        #self.main_window.attributes("-zoomed", True)
        self.main_window.title("Validador XML")
        self.fuente=Font(family="Courier", size=12, weight="bold")
        self.buildUI()
        self.configurar_tipos_de_letra()
        
    def boton_derecho_dtd(self, evento):
        self.dtd.delete(1.0, END)
        texto_portapapeles=self.main_window.clipboard_get()
        self.dtd.insert(END, texto_portapapeles)
        
        
    def boton_derecho_xml(self, evento):
        self.text.delete(1.0, END)
        texto_portapapeles=self.main_window.clipboard_get()
        self.text.insert(END, texto_portapapeles)
    
    
        
    def buildUI(self):
        self.frame_xml=Frame(self.main_window)
        self.frame_xml.pack(fill=BOTH, expand=True, side=TOP)
        
        self.dtd=ScrolledText(self.frame_xml, width=50, height=30)
        self.dtd.pack(fill=BOTH, expand=True,  side=LEFT)
        self.dtd.bind("<Button-3>", self.boton_derecho_dtd)
        self.dtd.insert(END, "Pulsa aquí con el botón derecho para borrar y pegar lo que tuvieses copiado (debería ser una DTD o XML Schema o XPath)")
        self.text=ScrolledText(self.frame_xml, width=50, height=30)
        self.text.pack(fill=BOTH,  expand=True, side=LEFT)
        self.text.insert(END, INICIAL)
        self.text.bind("<Button-3>", self.boton_derecho_xml)
        self.text.insert(END, "Pulsa aquí con el botón derecho para borrar y pegar lo que tuvieses copiado (debería ser XML)")
        #self.dtd.insert(END, DTD_INICIAL)
        
        self.btn_xpath=Button(self.frame_xml, text="Evaluar con XPath")
        self.btn_xpath.pack(fill=X, expand=True, side=BOTTOM)
        self.btn_xpath.bind("<Button-1>", self.evaluate_xpath)
        self.btn_xslt=Button(self.frame_xml, text="Transformar con XSLT")
        self.btn_xslt.pack(fill=X,expand=True,  side=BOTTOM)
        self.btn_xslt.bind("<Button-1>", self.transform_xml_with_xslt)
        
        self.btn_validate=Button(self.frame_xml, text="Validar con DTD")
        self.btn_validate.pack(fill=X,expand=True,  side=BOTTOM)
        self.btn_validate.bind("<Button-1>", self.validate_dtd)
        self.btn_schema=Button(self.frame_xml, text="Validar con esquema")
        self.btn_schema.pack(fill=X,expand=True,  side=BOTTOM)
        self.btn_schema.bind("<Button-1>", self.validate_schema)
        
        self.label=Label(self.main_window,text="Mensajes")
        self.label.pack(side=TOP)
        self.report=ScrolledText(self.main_window)
        self.report.pack(side=TOP, expand=True, fill=BOTH)
        self.report.insert(END, "Informes")
        
    def configurar_tipos_de_letra(self):
        controles_con_tipo_de_letra_grande=[
            self.report, self.text, self.dtd
        ]
        for c in controles_con_tipo_de_letra_grande:
            c.configure(font=self.fuente)
        
    def validate_dtd(self, event):
        text=self.text.get(1.0, END)
        texto_dtd=self.dtd.get(1.0,END)
        self.report.delete(1.0, END)
        try:
            #root_element=etree.fromstring(text)
            dtd=etree.DTD(StringIO(texto_dtd))
            xml=etree.XML(text)
            if dtd.validate(xml):
                self.report.insert(END, "XML procesado sin errores")
                return 
            else:
                for e in dtd.error_log.filter_from_errors():
                    self.report.insert(END, str(e))
                    self.report.insert(END, "\n")
            return 
        except Exception as e:
            self.report.insert(END, str(e) )
            return
        self.report.insert(END, "XML procesado sin errores")
    
    
    
    def get_xml_elemento(self, elemento):
        
        texto=tostring(elemento, pretty_print=True).decode("utf-8")
        return texto
    
    
    def get_xml_desde_lista_elementos(self, lista):
        elementos=[]
        for e in lista:
            texto=self.get_xml_elemento(e)
            elementos.append(texto)
        return "\n".join(elementos)
    
    
    
    def get_resultado(self, resultado_xpath):
        xml=""
        if isinstance(resultado_xpath, list):
            if isinstance(resultado_xpath[0], etree._Element):
                xml=self.get_xml_desde_lista_elementos(resultado_xpath)
            else:
                xml="\n".join(resultado_xpath)
                
        if isinstance(resultado_xpath, etree._Element):
            xml=self.get_xml_elemento(resultado_xpath)
        
        return xml
    def evaluate_xpath(self, evento):
        print ("Evaluando XPath")
        text=self.text.get(1.0, END)
        texto_xpath=self.dtd.get(1.0,END)
        self.report.delete(1.0, END)
        
        try:
            xml=etree.XML(text)
            resultado_xpath=xml.xpath(texto_xpath)
            print(resultado_xpath)
            
            xml=self.get_resultado(resultado_xpath)
            self.report.insert(END, xml)
                
        except Exception as e:
            self.report.insert(END, "El XML de la derecha no está bien formado o el XPath es incorrecto\n" )
            self.report.insert(END, str(e) )
        
    def validate_schema(self, event):
        text=self.text.get(1.0, END)
        texto_dtd=self.dtd.get(1.0,END)
        self.report.delete(1.0, END)
        try:
            #root_element=etree.fromstring(text)
            schema_root=etree.XML(texto_dtd)
        except Exception as e:
            self.report.insert(END, "El esquema no es XML bien formado\n" )
            self.report.insert(END, str(e) )
        try:
            schema=etree.XMLSchema(schema_root)
            parser=etree.XMLParser(schema=schema)
            
            root=etree.fromstring(text, parser)
        except Exception as e:
            self.report.insert(END, str(e) )
            return
        self.report.insert(END, "XML procesado sin errores")
        
        
    def bytes_a_cadena(self, bytes, codificacion="utf-8"):
        result=str(bytes, "utf-8")
        return result
    
    def result_is_html(self, result):
        result=self.bytes_a_cadena(result)
        contains_html   =   result.find("<html>")
        contains_body   =   result.find("<body>")
        if contains_body!=-1 and contains_html!=-1:
            print("Es html")
            return True
        print("Es xml")
        return False
    
    def transform_xml_with_xslt(self, event):
        texto_xml=self.text.get(1.0, END)
        texto_xslt=self.dtd.get(1.0,END)
        self.report.delete(1.0, END)
        try:
            #root_element=etree.fromstring(text)
            raiz_xslt=etree.XML(texto_xslt)
        except Exception as e:
            self.report.insert(END, "El XSLT de la izquierda no es XML bien formado\n" )
            self.report.insert(END, str(e) )
            return 
        try:
            #root_element=etree.fromstring(text)
            raiz_xml=etree.XML(texto_xml)
        except Exception as e:
            self.report.insert(END, "El XML (derecha) no es XML bien formado\n" )
            self.report.insert(END, str(e) )
            return
        
        
        try:
            
            funcion_transfomadora_de_xml_con_xslt=etree.XSLT(raiz_xslt)
            arbol_resultado=funcion_transfomadora_de_xml_con_xslt(raiz_xml)
            arbol_resultado_embellecido=etree.tostring(arbol_resultado, pretty_print=True)
            #self.report.insert(END, str(arbol_resultado_embellecido))
            self.report.insert(END, arbol_resultado_embellecido)
            
            nombre_fichero=self.nombre_fichero_resultado
            if self.almacenar_en_fichero:
                if self.result_is_html ( arbol_resultado_embellecido):
                    nombre_fichero+=".html"
                else:
                    nombre_fichero+=".xml"
                fichero=open(nombre_fichero,"w")
                cad_resultado=self.bytes_a_cadena(arbol_resultado_embellecido)
                fichero.write(cad_resultado)
                fichero.close()
                return 
        except Exception as e:
            self.report.insert(END, str(e) )
            return
        
    def start(self):
        self.main_window.mainloop()
    
    
    
if __name__ == '__main__':
    validator=Validator()
    validator.start()
        