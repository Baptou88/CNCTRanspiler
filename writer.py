class Writer:

    nom_fichier = 'Nouveau dossier/out7751.spf'
    def __init__(self) -> None:
        self.ouvrir_fichier()


    def ouvrir_fichier(self): 
        try: 
            self.fichier = open(self.nom_fichier, 'w') 
        except IOError as e: 
            print(f"Erreur lors de l'ouverture du fichier {self.nom_fichier} : {e}") 

    def ecrire_fichier(self, contenu): 
        if contenu == None:
            return
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