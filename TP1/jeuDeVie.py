#J.A / 4.11 / Jeu de la vie

# Paramètres de la grille : 20 colonnes, 20 lignes, chaque case mesure 10 pixels
taille_g = struct(nx=20, ny=20, dim=10)

#Crée une grille vide (cellules mortes = 0)
# y = numéro de ligne (de haut en bas), x = numéro de colonne
def creer(taille_g):
   
    tab = []
    for y in range(taille_g.ny):
        ligne = []
        for x in range(taille_g.nx):
            ligne.append(0)      # 0 = cellule morte
        tab.append(ligne)

    # On renvoie la grille et ses dimensions
    return struct(grille=tab, nx=taille_g.nx, ny=taille_g.ny, dim=taille_g.dim)


#Remplit aléatoirement la grille avec des cellules vivantes.
def init(g):
    nb_cases = g.nx * g.ny

    # Pourcentage aléatoire de cellules vivantes, entre 10 % et 50 %
    pourcentage = 0.4 * random() + 0.1
    nb_vivantes = round(pourcentage * nb_cases)

    compteur = 0
    while compteur < nb_vivantes:
        #case au hasard
        x = int(random() * g.nx)
        y = int(random() * g.ny)

        # On compte seulement si la case était morte, on évite
        # de tomber deux fois sur la même case et de fausser le total
        if g.grille[y][x] == 0:
            g.grille[y][x] = 1
            compteur += 1

    return g

#Trace nbLignes lignes parallèles, espacées de 'pas', de longueur 'largeur'.
def lignes(nbLignes, pas, largeur):
    for _ in range(nbLignes):
        fd(largeur)                   # trace une ligne
        positionner(-largeur, pas)    # revient au début et monte d'un cran, sans tracer
    # Une fois toutes les lignes tracées, on revient au point de départ
    positionner(0, -pas * nbLignes)

#Déplace la tortue de x (devant) et y (côté gauche) SANS tracer.
def positionner(x, y):
    pu()          # lever le crayon
    fd(x)         # avancer dans la direction actuelle
    lt(90)        # tourner à gauche 
    fd(y)
    rt(90)        # remettre la tortue dans son orientation d'origine
    pd()          # baisser le crayon

#Dessine le quadrillage : nx colonnes et ny lignes de cases de côté 'pas'.
def quadrillage(nx, ny, pas):    
    # Il faut (ny + 1) traits horizontaux pour délimiter ny lignes de cases
    lignes(ny + 1, pas, pas * nx)
    lt(90)                            # on pivote pour tracer les traits verticaux
    lignes(nx + 1, -pas, pas * ny)    # pas négatif : on décale vers la droite
    rt(90)                            # retour à l'orientation initiale

#Affiche la grille : cellules vivantes en rouge + quadrillage noir.
def dessiner(g):
    clear()
    ht()                              # cache la tortue pour un affichage plus propre

    dim = g.dim
    # Coin inférieur gauche de la grille, pour qu'elle soit centrée à l'écran
    x0 = -g.nx * dim / 2
    y0 = -g.ny * dim / 2

    pencolor(1, 0, 0)                 # rouge
    pensize(dim)
    for y in range(g.ny):
        for x in range(g.nx):
            if g.grille[y][x] == 1:
                pu()
                goto(x0 + x*dim, y0 + (g.ny - 1 - y)*dim + dim/2)
                pd()
                fd(dim)               # trait horizontal de la largeur d'une case

    #Quadrillage
    pencolor(0, 0, 0)                 # noir
    pensize(1)                        # trait fin
    pu()
    goto(x0, y0)                      # on repart du coin inférieur gauche
    pd()
    quadrillage(g.nx, g.ny, dim)

#Calcule la génération suivante.
def suivant(g):
    futur = creer(struct(nx=g.nx, ny=g.ny, dim=g.dim))

    for y in range(g.ny):
        for x in range(g.nx):

            #Comptage des 8 voisins
            voisins = 0
            for dy in range(-1, 2):         
                for dx in range(-1, 2):     
                    
                    # (0, 0) est la cellule elle-même : on l'exclut
                    if dx != 0 or dy != 0:
                        yv = y + dy
                        xv = x + dx
                        
                        # On vérifie qu'on reste dans la grille
                        if 0 <= yv < g.ny and 0 <= xv < g.nx:
                            voisins += g.grille[yv][xv]   # 1 si vivante, 0 si morte
                            
            if g.grille[y][x] == 1:
                # Une cellule vivante survit avec 2 ou 3 voisins
                # (sinon elle meurt : isolement ou surpopulation)
                if voisins == 2 or voisins == 3:
                    futur.grille[y][x] = 1
            else:
                # Une cellule morte naît si elle a exactement 3 voisins
                if voisins == 3:
                    futur.grille[y][x] = 1

    return futur


def jouer(taille_g, f_aff):
    """Boucle principale. f_aff = nombre d'images affichées par seconde."""
    g = creer(taille_g)    # 1. grille vide
    g = init(g)            # 2. remplissage aléatoire

    while True:           
        dessiner(g)        # afficher la génération actuelle
        futur = suivant(g) # calculer la suivante
        g = futur          # elle devient la génération courante
        sleep(1 / f_aff)   # pause pour que l'animation soit visible


#grille 20x20, 10 images par seconde
jouer(taille_g, 10)
