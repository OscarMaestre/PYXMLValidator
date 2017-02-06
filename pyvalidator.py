#!/usr/bin/env python3
#coding=utf-8

from tkinter import *
from tkinter.ttk import *
from lxml import etree

class Validator(object):
    def __init__(self):
        self.main_window=Tk()
        self.buildUI()
    def buildUI(self):
        self.frame_xml=Frame(self.main_window)
        self.frame_xml.pack(fill=BOTH, expand=True, side=TOP)
        self.text=Text(self.frame_xml)
        self.text.pack(fill=BOTH, expand=True, side=LEFT)
        self.text.insert(END, "<?xml version=\"1.0\"?>\n")
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
        self.report.delete(1.0, END)
        try:
            root_element=etree.fromstring(text)
        except Exception as e:
            print("Error")
            self.report.insert(END, str(e) )
            return
        self.report.insert(END, "XML procesado sin errores")
        
        
        
    def start(self):
        self.main_window.mainloop()
    
    
    
if __name__ == '__main__':
    validator=Validator()
    validator.start()
        