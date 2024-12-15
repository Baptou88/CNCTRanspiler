import re
import calculCercle
from writer import abstractWriter

class HReader():

    writer: abstractWriter = None
    blk_form_01 = []

    def __init__(self,writer) -> None:
        self.writer = writer

    
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
        if ligne.find("DR-"):
            return -1
        elif ligne.find("DR+"):
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
            self.writer.writeEntete(temp[0]+"\n")

            return
        
        if ligne.startswith(";"):
            self.writer.writeCommentaire(ligne.removeprefix(";"))
            return
        
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

            self.writer.writeBLKFORM(blk_form_01,blk_form_02)
            return
        
        if patternTOOLCALL.match(ligne):
            nouvelle_ligne = re.sub(r'^TOOL CALL\s*','',ligne)
            tool_id = nouvelle_ligne[0]
            result = re.findall(r'([a-zA-Z]+)([+-]?\d+)',nouvelle_ligne) 
            param ={lettre: int(nombre) for lettre, nombre in result} 
            self.writer.writeTCall(tool_id,param=param)
            return
        
        if patternL.match(ligne):
            nouvelle_ligne = re.sub(r'^L\s*','',ligne)
            result = re.findall(r'([a-zA-Z]+)([+-]?\d+\.\d+|[+-]?\d+)',nouvelle_ligne) 

            param = {}

            for groupe, nombre in result: 
                if groupe.startswith('M'): 
                    param[groupe + str(nombre)] = nombre 
                else: 
                    param[groupe] = float(nombre)


            param["RAPID"] = self.isRapid(nouvelle_ligne)
            param ["R"] = self.corrRayon(nouvelle_ligne)

            self.writer.writeLine(param=param)
            return
        
        if ligne.startswith("CR"):
            ligne = ligne.removeprefix("CR")
            result = re.findall(r'([a-zA-Z]+)([+-]?\d+\.\d+|[+-]?\d+)',ligne) 

            param = {}

            for groupe, nombre in result: 
                if groupe.startswith('M'): 
                    param[groupe + str(nombre)] = nombre 
                else: 
                    param[groupe] = float(nombre)
            param ["DR"] = self.sensCercle(ligne)
            self.writer.writeCircle(param=param)
            return
        
        if ligne.startswith("CC"):
            ligne = ligne.removeprefix("CC")
            result = re.findall(r'([a-zA-Z]+)([+-]?\d+\.\d+|[+-]?\d+)',ligne) 
            self.cc = result
            
            return 
        
        if ligne.startswith("M"):
            self.writer.ecrire_fichier(ligne)
            return
        if ligne.startswith('\n'): 
            self.writer.ecrire_fichier("\n")
            return
        
        self.writer.unimplemented(ligne)

