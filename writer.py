class Writer:

    nom_fichier = 'default'
    ligne = 10
    inc_ligne = 10

    def __init__(self,nomFichier,lignifie = False ) -> None:
        self.lignifie = lignifie
        self.nom_fichier = nomFichier
        self.ouvrir_fichier()

    def ouvrir_fichier(self): 
        try: 
            self.fichier = open(self.nom_fichier, 'w') 
        except IOError as e: 
            print(f"Erreur lors de l'ouverture du fichier {self.nom_fichier} : {e}") 

    def ecrire_fichier(self, contenu:str): 
        if contenu == None:
            return
        if self.fichier: 
            try: 
                lignes = contenu.splitlines()
                for l in contenu.splitlines():

                    if self.lignifie:
                        self.fichier.write(f"{self.ligne} {l}\n") 
                        self.ligne += 10
                    
                    else:

                        self.fichier.write(f"{l}\n") 
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