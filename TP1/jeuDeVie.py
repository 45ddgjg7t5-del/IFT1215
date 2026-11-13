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

# Cette fonction calcule le nombre de cellules vivantes

def calculer_nb_vivantes(nb_cases, pourcentage): 
    return round(pourcentage * nb_cases)

#------------------------------------------------------------------------------

# Cette fonction remplit aléatoirement le tableau avec des cellules vivantes (1)

def init(grille):
    nb_cases = grille.nx * grille.ny
    pourcentage = 0.4 * random() + 0.1  # 10% à 50% (0.1 à 0.5)
    nb_vivantes = calculer_nb_vivantes(nb_cases, pourcentage)

    compteur = 0
    while compteur < nb_vivantes:    # tant que le nombre de cases vivantes n'est pas atteint
        x = int(random() * grille.nx)
        y = int(random() * grille.ny)  # génère un emplacement aléatoire dans le tableau

        if grille.tab[y][x] == 0:  # rend la cellule morte à l'emplacement généré vivante
            grille.tab[y][x] = 1
            compteur += 1     # On compte seulement si la case était morte, on évite
                              # de compter deux fois la même case et de fausser le total

            

    return grille

#------------------------------------------------------------------------------

# Les fonctions lignes, positionner et quadrillage ont été prises de la 
# diapositive 18 des notes de cours sur tortue pour dessiner une grille

def lignes(nbLignes, pas, largeur):   # trace nbLignes lignes parallèles, espacées de 'pas', de longueur 'largeur'
    for _ in range(nbLignes):
        fd(largeur)    # trace une ligne
        positionner(-largeur, pas)  # revient au début et monte d'un cran, sans tracer
    positionner(0, -pas*nbLignes)   # une fois toutes les lignes tracées, on revient au point de départ


def positionner(x, y):
    pu(); fd(x); lt(90); fd(y); rt(90); pd()   # déplace la tortue de x (devant) et y (côté gauche) SANS tracer


def quadrillage(nx, ny, pas):   # dessine le quadrillage : nx colonnes et ny lignes de cases de côté 'pas'
    lignes(ny+1, pas, pas*nx)
    lt(90)
    lignes(nx+1, -pas, pas*ny)
    rt(90)

#------------------------------------------------------------------------------

# Cette fonction dessine la grille et colorie les cellules vivantes en rouge

def dessiner(grille):
    clear()  # efface la grille tracé avant (pour la boucle plus tard)
    ht()  # cache la tortue

    dim = grille.dim
    x0 = -grille.nx * dim / 2  # à gauche complètement (pour avoir une grille centrée à 0,0)
    y0 = -grille.ny * dim / 2  # en bas complètement (pour avoir une grille centrée à 0,0)

    pencolor(1, 0, 0)  # rouge
    pensize(dim)  # trait épaisseur d'une case
    for y in range(grille.ny):
        for x in range(grille.nx):
            if grille.tab[y][x] == 1:  # trace un carré plein rouge si emplacement d'une cellule vivante
                pu()
                goto(x0 + x*dim, y0 + (grille.ny - 1 - y)*dim + dim/2)   # aidés de Claude pour la partie (grille.ny - 1 - y)
                # on veut commencer au y le plus bas, car la tortue monte
                # pour tracer le quadrillage donc chaque fois que y augmente, on monte.
                # dim/2, car l'épaisseur du trait dépasse de chaque côté de la tortue
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

# Cette fonction calcule le nombre de voisins d'une cellule

def compter_voisins(grille, x, y):
    total = 0
    for dy in range(-1, 2): # y avoisinnant la cellule
        for dx in range(-1, 2): # x avoisinnant la cellule
            if dx != 0 or dy != 0:  # on rejette dx = 0 ET dy = 0, car c'est la cellule elle-même
                yv = y + dy  # coordonnée en y du voisin
                xv = x + dx  # coordonnée en x du voisin
                if 0 <= yv < grille.ny and 0 <= xv < grille.nx:  # on vérifie que le voisin est dans la grille
                    total += grille.tab[yv][xv] # pour ajouter seulement les voisins vivants (1), car les voisins morts on la valeur 0
    return total  # nombre de voisins vivants

#------------------------------------------------------------------------------

# Cette fonction applique les changements d'état en fonction du nombre de voisins pour chaque cellule

def etat_suivant(etat, voisins):
    if voisins == 3:
        return 1    # survie ou reproduction
    if voisins == 2:
        return etat    # stabilité
    return 0      # sous-population ou surpopulation

#------------------------------------------------------------------------------

# Cette fonction retourne la grille après les changements

def suivant(grille):
    futur = creer(struct(nx=grille.nx, ny=grille.ny, dim=grille.dim))  # crée un tableau rempli de zéros avec les 
                                                                       # mêmes dimensions que la grille actuelle

    for y in range(grille.ny):
        for x in range(grille.nx):
            voisins = compter_voisins(grille, x, y)   # compte le nombre de voisins
            futur.tab[y][x] = etat_suivant(grille.tab[y][x], voisins)  # applique les changements

    return futur

#------------------------------------------------------------------------------

# Cette fonction est la fonction qui fait fonctionner le jeu
# f_aff = nombre d'images affichées par seconde

def jouer(taille_g, f_aff):
    grille = creer(taille_g)  # 1. grille vide
    grille = init(grille)  # 2. remplir la grille vide aléatoirement avec des 1

    repeter = True  # boucle infinie

    while repeter:
        dessiner(grille)  # afficher la génération actuelle
        # gr1 = grille
        futur = suivant(grille)  # calculer la suivante
        # if gr1 == futur:  # (Nous aurious ajouté les lignes 156, 158-159 pour arrêter le programme si l'état ne change pas)
        #    repeter = False
        grille = futur  # elle devient la génération courante
        sleep(1/f_aff)  # pause pour que l'animation soit visible

#------------------------------------------------------------------------------

# Fonctions tests unitaires

def test_calculer_nb_vivantes():
    assert calculer_nb_vivantes(25, 0.35) == 9   # 8.75 -> 9
    assert calculer_nb_vivantes(25, 0.33) == 8   # 8.25 -> 8
    assert calculer_nb_vivantes(400, 0.10) == 40
    assert calculer_nb_vivantes(400, 0.50) == 200


def test_compter_voisins():
    g = creer(struct(nx=3, ny=3, dim=10))
    g.tab[0][0] = 1               # 1 1 0
    g.tab[0][1] = 1               # 0 1 0
    g.tab[1][1] = 1               # 0 0 0
    assert compter_voisins(g, 1, 1) == 2     # centre : ne se compte pas lui-même
    assert compter_voisins(g, 0, 0) == 2     # coin : bords ne sont pas comptés
    assert compter_voisins(g, 2, 2) == 1
    assert compter_voisins(g, 2, 0) == 2     # coin opposé

    vide = creer(struct(nx=3, ny=3, dim=10))  # test pour grille vide
    assert compter_voisins(vide, 1, 1) == 0

    pleine = creer(struct(nx=3, ny=3, dim=10))  # test pour grille pleine
    for y in range(3):
        for x in range(3):
            pleine.tab[y][x] = 1
    assert compter_voisins(pleine, 1, 1) == 8   # maximum
    assert compter_voisins(pleine, 0, 0) == 3   # coin


def test_etat_suivant():
    assert etat_suivant(1, 1) == 0    # sous-population
    assert etat_suivant(1, 2) == 1    # stabilité (vivante)
    assert etat_suivant(0, 2) == 0    # stabilité (morte)
    assert etat_suivant(1, 3) == 1    # survie
    assert etat_suivant(1, 4) == 0    # surpopulation
    assert etat_suivant(0, 3) == 1    # reproduction
    assert etat_suivant(0, 4) == 0    # surpopulation

#------------------------------------------------------------------------------

# Tests unitaires

test_calculer_nb_vivantes()
test_compter_voisins()
test_etat_suivant()

#------------------------------------------------------------------------------

jouer(struct(nx=20, ny=20, dim=10), 10) # 20 x 20 cases, 10 pixels par case, 10 Hz