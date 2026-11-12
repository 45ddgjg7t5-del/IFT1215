#TP 1 - Jeu de vie
#Jonathan Audet ()
#Yasser Metnani (20365600)

###
def creer(taille_g):  #taille_g = (nx = ..., ny = ..., dim = ...)
    tab = []
    for y in range(taille_g.ny):
        ligne = []
        for x in range(taille_g.nx):
            ligne.append(0)
        tab.append(ligne)

    return struct(tab=tab, nx=taille_g.nx, ny=taille_g.ny, dim=taille_g.dim)

###
def init(grille):
    nb_cases = grille.nx * grille.ny
    pourcentage = 0.4 * random() + 0.1
    nb_vivantes = round(pourcentage * nb_cases)

    compteur = 0
    while compteur < nb_vivantes:
        x = int(random() * grille.nx)
        y = int(random() * grille.ny)

        if grille.tab[y][x] == 0:
            grille.tab[y][x] = 1
            compteur += 1

    return grille

###
def lignes(nbLignes, pas, largeur):
    for _ in range(nbLignes):
        fd(largeur)
        positionner(-largeur, pas)
    positionner(0, -pas * nbLignes)

###
def positionner(x, y):
    pu(); fd(x); lt(90); fd(y); rt(90); pd()

###
def quadrillage(nx, ny, pas):
    lignes(ny + 1, pas, pas * nx)
    lt(90)
    lignes(nx + 1, -pas, pas * ny)
    rt(90)


def dessiner(grille):
    clear()
    ht()

    dim = grille.dim
    x0 = -grille.nx * dim / 2
    y0 = -grille.ny * dim / 2

    pencolor(1, 0, 0)
    pensize(dim)
    for y in range(grille.ny):
        for x in range(grille.nx):
            if grille.tab[y][x] == 1:
                pu()
                goto(x0 + x*dim, y0 + (grille.ny - 1 - y)*dim + dim/2)
                pd()
                fd(dim)

    pencolor(0, 0, 0)
    pensize(1)
    pu()
    goto(x0, y0)
    pd()
    quadrillage(grille.nx, grille.ny, dim)


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


def jouer(taille_g, f_aff):
    grille = creer(taille_g)
    grille = init(grille)

    while True:
        dessiner(grille)
        futur = suivant(grille)
        grille = futur
        sleep(1 / f_aff)



jouer(struct(nx=20, ny=20, dim=10), 10)