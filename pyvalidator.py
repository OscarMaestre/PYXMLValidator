#!/usr/bin/env python3
#coding=utf-8
import Stringi
from tkinter import *
from tkinter.ttk import *
from lxml import etree

DTD_INICIAL="""
<!DOCTYPE listaclientes [
   <!ELEMENT listaclientes (cliente+)>
   <!ELEMENT cliente (cif, nombre, diasentrega?)>
   <!ELEMENT cif (#PCDATA)>
   <!ELEMENT nombre (#PCDATA)>
   <!ELEMENT diasentrega (#PCDATA)>
]>
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
class Validator(object):
    def __init__(self):
        self.main_window=Tk()
        self.main_window.geometry("800x480+100+100")
        self.buildUI()
    def buildUI(self):
        self.frame_xml=Frame(self.main_window)
        self.frame_xml.pack(fill=BOTH, expand=True, side=TOP)
        self.dtd=Text(self.frame_xml, width=50, height=30)
        self.dtd.pack(fill=BOTH, expand=True, side=LEFT)
        self.text=Text(self.frame_xml, width=50, height=30)
        self.text.pack(fill=BOTH, expand=True, side=LEFT)
        self.text.insert(END, INICIAL)
        self.dtd.insert(END, DTD_INICIAL)
        self.btn_validate=Button(self.frame_xml, text="VALIDATE")
        self.btn_validate.pack(fill=X, expand=True, side=LEFT)
        self.btn_validate.bind("<Button-1>", self.validate)
        self.label=Label(self.main_window,text="Messages")
        self.label.pack(side=TOP)
        self.report=Text(self.main_window)
        self.report.pack(side=TOP, expand=True, fill=BOTH)
        self.report.insert(END, "Reports")
    def validate(self, event):
        text=self.text.get(1.0, END)
        texto_dtd=self.dtd.get(1.0,END)
        self.report.delete(1.0, END)
        try:
            #root_element=etree.fromstring(text)
            dtd=etree.DTD(texto_dtd)
            parser=etree.XMLParser(dtd_validation=True)
            print("Ok")
        except Exception as e:
            self.report.insert(END, str(e) )
            return
        self.report.insert(END, "XML procesado sin errores")
        
        
        
    def start(self):
        self.main_window.mainloop()
    
    
    
if __name__ == '__main__':
    validator=Validator()
    validator.start()
        