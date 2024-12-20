from abc import ABC, abstractmethod
import calculCercle

class abstractTranslator (ABC):
    def __init__(self):
        pass

    @abstractmethod
    def writeBLKFORM(self,min,max)-> str:
        pass

    @abstractmethod
    def writeTCall(self,t,param)-> str:
        pass
    
    @abstractmethod
    def writeCommentaire(self,commentaire:str)-> str:
        pass
    
    @abstractmethod
    def writeLine(self,param)-> str:
        pass
    
    @abstractmethod
    def writeCircle(self,param)-> str:
        pass

    @abstractmethod
    def unimplemented(self,line)-> str:
        pass
    
    @abstractmethod
    def writeEntete(self,line)-> str:
        pass



class Siemens(abstractTranslator):
    ext = '.spf'
    

    def __init__(self):
        pass

    def writeBLKFORM(self,min,max):
        retour =  (f"min: {min}\n"
                   f"max: {max}")
        
        return retour
       

    def writeTCall(self,t,param):
        retour = (f"T=\"{t}\" D1\n")
        retour +=      f"M6\n"
        if 'S' in param:
            f"S{param['S']}"
            retour += "\n"
        return retour

    def writeCommentaire(self,commentaire:str):
        return(f";;{commentaire}")

    def unimplemented(self, line):
        return(f"Unimplemented  " + line)

    def writeEntete(self,line):
        return(f"%{line}")

    def writeLine(self,param):
        
        if param["RAPID"]:
            ligne = "G00"
        else:
            ligne = "G01"

        match param["R"]:
            case 40:
                ligne += " G40"
            case 41:
                ligne += " G41"
            case 42:
                ligne += " G42"
                
        if 'X' in param:
            self.currentX = param['X']
            ligne += " X" + str(param['X'])
        if 'Y' in param:
            self.currentY = param['Y']
            ligne += " Y" + str(param['Y'])
        if 'Z' in param:
            ligne += " Z" + str(param['Z'])
            
        for cle  in param:
            if cle.startswith("M") :
                ligne += " M" + str(param[cle])
            elif cle.startswith("F") and cle != "FMAX":
                ligne += " F" + str(param[cle])
        return(ligne+"\n")
        
    def writeCircle(self,param,cc=None):
        if cc == None:
            cc= {}
            centre = calculCercle.calculer_centre(
                self.currentX,
                self.currentY,
                param['X'],
                param['Y'],
                param['R'],
                "horaire" if param['DR'] < 0 else "antihoraire"
                )
            cc['X'] = centre[0]
            cc['Y'] = centre[1]
        if param['DR'] > 0:
            retour = "G03"
        else:
            retour = "G02"

        self.currentX = param['X']
        self.currentY = param['Y']
        return(f"{retour} X{param['X']} Y{param['Y']} I=AC({cc['X']:.4f}) J=AC({cc['Y']:.4f})\n")