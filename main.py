
from translator import Siemens
from H_Reader import HReader
import sys

from writer import Writer

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Appel en terminal pour créer une barre de progression
    @params:
        iteration   - Itération actuelle (int)
        total       - Nombre total d'itérations (int)
        prefix      - Préfixe de la chaîne (str)
        suffix      - Suffixe de la chaîne (str)
        decimals    - Nombre de décimales dans le pourcentage de progression (int)
        length      - Longueur de la barre de progression (int)
        fill        - Caractère de remplissage (str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    # Print New Line on Complete
    if iteration == total:
        sys.stdout.write('\n')


if __name__ == '__main__':

    translator = Siemens()
    reader = HReader(translator)
    writer = Writer()

    try:
        # with open('Nouveau dossier/NoName.h', 'r') as fichier:
        with open(r'\\192.168.1.10\Dnc\Supervision\Atelier\DMC64V\L7751.h', 'r') as fichier:
            # Calculer le nombre total de lignes 
            total_lines = sum(1 for line in fichier) 
            fichier.seek(0) # Revenir au début du fichier
            for i, ligne in enumerate(fichier):
                #print(f"{i+1}/{total_lines}")
                print_progress_bar(i + 1, total_lines, prefix='Progress:', suffix='Complete', length=50)
                
                writer.ecrire_fichier(reader.convert(ligne)) 
    except ValueError as e:
        writer.ecrire_fichier(f"erreur {e} ligne {i}")

    #convert("4545 L X+10 Y-50")
    #convert("4546 L Y+0")
    #convert("4547 CR X+0 Y+10 R+10 DR-")

    writer.fermer_fichier()