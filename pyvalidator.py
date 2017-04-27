#!/usr/bin/env python3
#coding=utf-8
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.ttk import *

from lxml import etree
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
<catalogo>
    <libro>
        <title>Don Quijote</title>
        <autores>
            <autor>Cervantes</autor>
            <autor>Otro</autor>
        </autores>
    </libro>
    <libro>
        <titulo>Historia</titulo>
        <autores>
            <autor>Autor 2</autor>
            <autor>Autor 3</autor>
        </autores>
    </libro>
</catalogo>
"""


DTD_INICIAL=""
INICIAL=""
class Validator(object):
    def __init__(self):
        self.almacenar_en_fichero=True
        self.nombre_fichero_resultado="resultado_xslt"
        self.main_window=Tk()
        #self.main_window.attributes("-zoomed", True)
        self.main_window.title("Validador XML")
        self.buildUI()
    def buildUI(self):
        self.frame_xml=Frame(self.main_window)
        self.frame_xml.pack(fill=BOTH, expand=True, side=TOP)
        self.dtd=ScrolledText(self.frame_xml, width=50, height=30)
        self.dtd.pack(fill=BOTH, expand=True,  side=LEFT)
        self.text=ScrolledText(self.frame_xml, width=50, height=30)
        self.text.pack(fill=BOTH,  expand=True, side=LEFT)
        self.text.insert(END, INICIAL)
        self.dtd.insert(END, DTD_INICIAL)
        self.btn_xslt=Button(self.frame_xml, text="Transformar con XSLT")
        self.btn_xslt.pack(fill=X,expand=True,  side=BOTTOM)
        self.btn_xslt.bind("<Button-1>", self.transform_xml_with_xslt)
        
        self.btn_validate=Button(self.frame_xml, text="Validar con DTD")
        self.btn_validate.pack(fill=X,expand=True,  side=BOTTOM)
        self.btn_validate.bind("<Button-1>", self.validate_dtd)
        self.btn_schema=Button(self.frame_xml, text="Validar con esquema")
        self.btn_schema.pack(fill=X,expand=True,  side=BOTTOM)
        self.btn_schema.bind("<Button-1>", self.validate_schema)
        
        
        
        self.label=Label(self.main_window,text="Messages")
        self.label.pack(side=TOP)
        self.report=ScrolledText(self.main_window)
        self.report.pack(side=TOP, expand=True, fill=BOTH)
        self.report.insert(END, "Reports")
        
        
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
        