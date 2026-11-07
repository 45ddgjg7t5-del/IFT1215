#J.A / 4.11 / Jeu de la vie
taille_g = struct(nx=20, ny=20, dim=10)



def creer(taille_g):
    tab = []
    for y in range(taille_g.ny):
        ligne = []
        for x in range(taille_g.nx):
            ligne.append(0)
        tab.append(ligne)

    return struct(grille=tab, nx=taille_g.nx, ny=taille_g.ny, dim=taille_g.dim)


def init(g):
    nb_cases = g.nx * g.ny
    pourcentage = 0.4 * random() + 0.1
    nb_vivantes = round(pourcentage * nb_cases)

    compteur = 0
    while compteur < nb_vivantes:
        x = int(random() * g.nx)
        y = int(random() * g.ny)

        if g.grille[y][x] == 0:
            g.grille[y][x] = 1
            compteur += 1

    return g


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


def dessiner(g):
    clear()
    ht()

    dim = g.dim
    x0 = -g.nx * dim / 2
    y0 = -g.ny * dim / 2

    pencolor(1, 0, 0)
    pensize(dim)
    for y in range(g.ny):
        for x in range(g.nx):
            if g.grille[y][x] == 1:
                pu()
                goto(x0 + x*dim, y0 + (g.ny - 1 - y)*dim + dim/2)
                pd()
                fd(dim)

    pencolor(0, 0, 0)
    pensize(1)
    pu()
    goto(x0, y0)
    pd()
    quadrillage(g.nx, g.ny, dim)


def suivant(g):
    futur = creer(struct(nx=g.nx, ny=g.ny, dim=g.dim))

    for y in range(g.ny):
        for x in range(g.nx):
            voisins = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx != 0 or dy != 0:
                        yv = y + dy
                        xv = x + dx
                        if 0 <= yv < g.ny and 0 <= xv < g.nx:
                            voisins += g.grille[yv][xv]

            if g.grille[y][x] == 1:
                if voisins == 2 or voisins == 3:
                    futur.grille[y][x] = 1
            else:
                if voisins == 3:
                    futur.grille[y][x] = 1

    return futur


def jouer(taille_g, f_aff):
    g = creer(taille_g)
    g = init(g) 

    while True:
        dessiner(g)
        futur = suivant(g)
        g = futur
        sleep(1 / f_aff)


jouer(taille_g, 10)