from abc import ABC, abstractmethod
import calculCercle

class abstractWriter (ABC):
    def __init__(self):
        pass

    @abstractmethod
    def writeBLKFORM(self,min,max):
        pass

    @abstractmethod
    def writeTCall(self,t,param):
        pass
    
    @abstractmethod
    def writeCommentaire(self,commentaire:str):
        pass
    
    @abstractmethod
    def writeLine(self,param):
        pass
    
    @abstractmethod
    def writeCircle(self,param):
        pass

    @abstractmethod
    def unimplemented(self,line):
        pass
    
    @abstractmethod
    def writeEntete(self,line):
        pass



class Siemens(abstractWriter):
    ext = '.spf'
    nom_fichier = 'Nouveau dossier/out.spf'

    def ouvrir_fichier(self): 
        try: 
            self.fichier = open(self.nom_fichier, 'w') 
        except IOError as e: 
            print(f"Erreur lors de l'ouverture du fichier {self.nom_fichier} : {e}") 

    def ecrire_fichier(self, contenu): 
        if self.fichier: 
            try: 
                self.fichier.write(contenu) 
                #print(f"Contenu écrit dans {self.nom_fichier}.") 
            except IOError as e: 
                print(f"Erreur lors de l'écriture dans le fichier {self.nom_fichier} : {e}") 

    def fermer_fichier(self): 
        if self.fichier: 
            try: 
                self.fichier.close() 
                #print(f"Fichier {self.nom_fichier} fermé.") 
            except IOError as e: 
                print(f"Erreur lors de la fermeture du fichier {self.nom_fichier} : {e}")

    def __init__(self):
        self.ouvrir_fichier()

    def writeBLKFORM(self,min,max):
        self.ecrire_fichier(f"min: {min}\n")
        self.ecrire_fichier(f"max: {max}\n")

    def writeTCall(self,t,param):
        self.ecrire_fichier(f"T=\"{t}\" D1\n")
        self.ecrire_fichier(f"M6\n")
        self.ecrire_fichier(f"S{param['S']}\n")

    def writeCommentaire(self,commentaire:str):
        self.ecrire_fichier(f";;{commentaire}")

    def unimplemented(self, line):
        self.ecrire_fichier(f"Unimplemented  " + line)

    def writeEntete(self,line):
        self.ecrire_fichier(f"%{line}")

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
        self.ecrire_fichier(ligne+"\n")
        
    def writeCircle(self,param):
        centre = calculCercle.calculer_centre(
            self.currentX,
            self.currentY,
            param['X'],
            param['Y'],
            param['R'],
            "horaire" if param['DR'] > 0 else "antihoraire"
            )
        if param['DR'] > 0:
            retour = "G02"
        else:
            retour = "G03"
        self.currentX = param['X']
        self.currentY = param['Y']
        self.ecrire_fichier(f"{retour} X{param['X']} Y{param['Y']} I{centre[0]:.4f} J{centre[1]:.4f}\n")