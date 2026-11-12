# TP 1 - Jeu de vie
# Jonathan Audet (20373865)
# Yasser Metnani (20365600)

# Cette fonction retourne un tableau vide (cellules mortes = 0) ainsi que ses dimensions

def creer(taille_g):  #taille_g = (nx = ..., ny = ..., dim = ...)
    tab = []
    for y in range(taille_g.ny):  # y est le nombre de lignes
        ligne = []
        for x in range(taille_g.nx):  # x est le nombre de colonnes
            ligne.append(0)      # dans chaque ligne, on rajoute x zéros
        tab.append(ligne)       # on ajourte les lignes dans le tableau

    return struct(tab=tab, nx=taille_g.nx, ny=taille_g.ny, dim=taille_g.dim)

#------------------------------------------------------------------------------

# Cette fonction remplit aléatoirement le tableau avec des cellules vivantes (1)

def init(grille):
    nb_cases = grille.nx * grille.ny
    pourcentage = 0.4 * random() + 0.1  # 10% à 50% (0.1 à 0.5)
    nb_vivantes = round(pourcentage * nb_cases)

    compteur = 0
    while compteur < nb_vivantes:    # tant que le nombre de cases vivantes n'est pas atteint
        x = int(random() * grille.nx)
        y = int(random() * grille.ny)  # génère un emplacement aléatoire dans le tableau

        if grille.tab[y][x] == 0:  # rend la cellule morte à l'emplacement généré vivante
            grille.tab[y][x] = 1
            compteur += 1

    return grille

#------------------------------------------------------------------------------

# Les fonctions lignes, positionner et quadrillage ont été prises de la 
# diapositive 18 des notes de cours sur tortue pour dessiner une grille

def lignes(nbLignes, pas, largeur):
    for _ in range(nbLignes):
        fd(largeur)
        positionner(-largeur, pas)
    positionner(0, -pas * nbLignes)


def positionner(x, y):
    pu(); fd(x); lt(90); fd(y); rt(90); pd()


def quadrillage(nx, ny, pas):
    lignes(ny + 1, pas, pas * nx)
    lt(90)
    lignes(nx + 1, -pas, pas * ny)
    rt(90)

#------------------------------------------------------------------------------

def dessiner(grille):
    clear()  # efface la grille tracé avant (pour la boucle plus tard)
    ht()  # cache la tortue

    dim = grille.dim
    x0 = -grille.nx * dim / 2
    y0 = -grille.ny * dim / 2

    pencolor(1, 0, 0)  # rouge
    pensize(dim)  # trait épaisseur d'une case
    for y in range(grille.ny):
        for x in range(grille.nx):
            if grille.tab[y][x] == 1:  # trace un carré plein rouge si emplacement d'une cellule vivante
                pu()
                goto(x0 + x*dim, y0 + (grille.ny - 1 - y)*dim + dim/2)
                pd()
                fd(dim)

    # Quadrillage
    pencolor(0, 0, 0)  # noir
    pensize(1)  # trait de 1 pixel
    pu()
    goto(x0, y0) # on se positionne au coin inférieur gauche
    pd()
    quadrillage(grille.nx, grille.ny, dim)  # pas de dim pixels

#------------------------------------------------------------------------------

def suivant(grille):
    futur = creer(struct(nx=grille.nx, ny=grille.ny, dim=grille.dim))

    for y in range(grille.ny):
        for x in range(grille.nx):
            voisins = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx != 0 or dy != 0:
                        yv = y + dy
                        xv = x + dx
                        if 0 <= yv < grille.ny and 0 <= xv < grille.nx:
                            voisins += grille.tab[yv][xv]

            if grille.tab[y][x] == 1:
                if voisins == 2 or voisins == 3:
                    futur.tab[y][x] = 1
            else:
                if voisins == 3:
                    futur.tab[y][x] = 1

    return futur

#------------------------------------------------------------------------------

def jouer(taille_g, f_aff):
    grille = creer(taille_g)  # 1. grille vide
    grille = init(grille)  # 2. remplir la grille vide aléatoirement avec des 1

    repeter = True

    while repeter:
        dessiner(grille)  # afficher la génération actuelle
        # gr1 = grille
        futur = suivant(grille)  # calculer la suivante
        # if gr1 == futur:  # (Nous aurious ajouté les lignes 121, 123-124 pour arrêter le programme si l'état ne change pas)
        #    repeter = False
        grille = futur  # elle devient la génération courante
        sleep(1/f_aff)  # pause pour que l'animation soit visible



jouer(struct(nx=20, ny=20, dim=10), 10) # 20 x 20 cases, 10 pixels par case, 10 Hz