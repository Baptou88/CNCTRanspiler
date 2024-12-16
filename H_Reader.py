import re
import calculCercle
from translator import abstractTranslator

class HReader():

    
    blk_form_01 = []

    def __init__(self,writer) -> None:
        self.writer:abstractTranslator = writer

    
    def isRapid(self,ligne:str):
        
        return ligne.find("FMAX") >= 0
    
    
    def corrRayon(self,ligne:str):
        if ligne.find("R0") >= 0:
            return 40
        elif ligne.find("RL") >= 0:
            return 41
        elif ligne.find("RR") >= 0:
            return 42
        else:
            return 0
        
    
    def sensCercle(self,ligne:str):
        if "DR-" in ligne:
            return -1
        elif "DR+" in ligne:
            return 1
        else:
            return 0

    
    def convert(self,ligne):

        patternBLKFORM1 = re.compile(r'^BLK FORM 0.1 Z')
        patternBLKFORM2 = re.compile(r'^BLK FORM 0.2')
        patternTOOLCALL = re.compile(r'^TOOL CALL')
        patternL = re.compile(r'^L')

        regex = re.compile(r'^\d+')
        ligne = re.sub(r'^\d+\s*', '', ligne)

        if ligne.startswith("BEGIN PGM "):
            ligne = ligne.removeprefix("BEGIN PGM ")
            temp = ligne.split(" ")
            self.pgmTitle = temp[0]
            self.mm =  temp[1].startswith("MM")
            return self.writer.writeEntete(temp[0]+"\n")

            
        
        if ligne.startswith(";"):
            return self.writer.writeCommentaire(ligne.removeprefix(";"))
            
        
        if patternBLKFORM1.match(ligne):
            nouvelle_ligne = re.sub(r'^BLK FORM 0.1 Z\s*','',ligne)
            
            result = re.findall(r'([a-zA-Z])([+-]?\d+)',nouvelle_ligne)
            global blk_form_01
            blk_form_01 = {lettre: int(nombre) for lettre, nombre in result}
            return 
        
        if patternBLKFORM2.match(ligne):

            nouvelle_ligne = re.sub(r'^BLK FORM 0.2\s*','',ligne)
            result = re.findall(r'([a-zA-Z])([+-]?\d+)',nouvelle_ligne)  
            blk_form_02 = {lettre: int(nombre) for lettre, nombre in result} 

            return self.writer.writeBLKFORM(blk_form_01,blk_form_02)
            
        
        if patternTOOLCALL.match(ligne):
            nouvelle_ligne = re.sub(r'^TOOL CALL\s*','',ligne)
            tool_id = nouvelle_ligne[0]
            result = re.findall(r'([a-zA-Z]+)([+-]?\d+)',nouvelle_ligne) 
            param ={lettre: int(nombre) for lettre, nombre in result} 
            return self.writer.writeTCall(tool_id,param=param)
            
        
        if patternL.match(ligne):
            nouvelle_ligne = re.sub(r'^L\s*','',ligne)
            #result = re.findall(r'([a-zA-Z]+)([+-]?\d+\.\d+|[+-]?\d+)',nouvelle_ligne) 
            result =  re.findall(r'([a-zA-Z]+)([-+]?\d*\,?\d*\.?\d*)', nouvelle_ligne)
            param = {}

            for groupe, nombre in result: 
                if groupe.startswith('M'): 
                    param[groupe + str(nombre)] = nombre 
                #elif groupe =='F': 
                    #param[groupe + str(nombre)] = nombre 
                else: 
                    if nombre != '':
                        param[groupe] = float(nombre.replace(',', '.'))


            param["RAPID"] = self.isRapid(nouvelle_ligne)
            param ["R"] = self.corrRayon(nouvelle_ligne)

            return self.writer.writeLine(param=param)
            
        
        if ligne.startswith("CR"):
            ligne = ligne.removeprefix("CR")
            #result = re.findall(r'([a-zA-Z]+)([+-]?\d+\.\d+|[+-]?\d+)',ligne) 
            result =  re.findall(r'([a-zA-Z]+)([-+]?\d*\,?\d*\.?\d*)', ligne)
            param = {}

            for groupe, nombre in result: 
                if groupe.startswith('M'): 
                    param[groupe + str(nombre)] = nombre 
                else: 
                    if nombre not in ['','+','-']:
                        param[groupe] = float(nombre.replace(',', '.'))
                    
            param["DR"] = self.sensCercle(ligne)
            return self.writer.writeCircle(param=param)
            
        
        if ligne.startswith("CC"):
            ligne = ligne.removeprefix("CC")
            #result = re.findall(r'([a-zA-Z]+)([+-]?\d+\.\d+|[+-]?\d+)',ligne) 
            result =  re.findall(r'([a-zA-Z]+)([-+]?\d*\,?\d*\.?\d*)', ligne)
            param = {}
            for groupe, nombre in result:
                param[groupe] = float(nombre.replace(',', '.'))
            self.cc = param
            return
        
        if ligne.startswith("C "):
            ligne = ligne.removeprefix("C ")     
            result =  re.findall(r'([a-zA-Z]+)([-+]?\d*\,?\d*\.?\d*)', ligne)
            param = {}

            for groupe, nombre in result: 
                if groupe.startswith('M'): 
                    param[groupe + str(nombre)] = nombre 
                else: 
                    if nombre not in ['','+','-']:
                        param[groupe] = float(nombre.replace(',', '.'))
                    
            param["DR"] = self.sensCercle(ligne)
            return self.writer.writeCircle(param=param,cc=self.cc)
        if ligne.startswith("M"):
            return ligne
        if ligne.startswith('\n'): 
            
            return "\n"
        
        return self.writer.unimplemented(ligne)

