import math

def calculer_centre(x1, y1, x2, y2, r, sens_rotation):
    # Milieu du segment entre les deux points
    x_mid = (x1 + x2) / 2
    y_mid = (y1 + y2) / 2

    # Distance entre les deux points
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Vérifier que la distance est inférieure ou égale à deux fois le rayon
    if d > 2 * r:
        raise ValueError("Les points sont trop éloignés pour former un cercle avec le rayon donné")

    # Distance du milieu au centre du cercle
    h = math.sqrt(r**2 - (d / 2)**2)

    # Calculer les coordonnées du centre
    dx = (y2 - y1) / d * h
    dy = (x2 - x1) / d * h

    # Deux centres possibles
    centre_1 = (x_mid + dx, y_mid - dy)
    centre_2 = (x_mid - dx, y_mid + dy)

    # Choisir le centre en fonction du sens de rotation
    if sens_rotation == "horaire":
        centre_final = centre_1 if (x1 - centre_1[0]) * (y2 - y1) - (y1 - centre_1[1]) * (x2 - x1) < 0 else centre_2
    else:
        centre_final = centre_1 if (x1 - centre_1[0]) * (y2 - y1) - (y1 - centre_1[1]) * (x2 - x1) > 0 else centre_2

    return centre_final

if __name__ == '__main__':
    # Exemple d'utilisation
    x1, y1 = 1, 1
    x2, y2 = 4, 5
    r = 5
    sens_rotation = "horaire"  # ou "antihoraire"
    centre = calculer_centre(x1, y1, x2, y2, r, sens_rotation)
    print(f"Le centre du cercle est : {centre}")
