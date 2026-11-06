#J.A / 4.11 / Jeu de la vie


def creer(taille_g):                                 
    taille_g = struct(nx=20, ny=20, dim=10)  #nx: cases sur axe x, ny: cases y
    grille = []                                    #dim: nb de pixel/case

    for y in range(taille_g.ny):                   
        ligne = []                                      #crée la grille 
        for x in range(taille_g.nx):
            ligne.append(0)

        grille.append(ligne)

    return grille


def init(grille):                   
    grille = creer(1)
    
    ran = random() * 0.4 + 0.1     #choisi aléatoirement 10-50% cases vivantes
    case_vivante = round(ran * 400)     #determine le nb de cases vivantes
    
    compteur = 0
    
    while compteur < case_vivante:
        x = int(random() * 20)                 #choisi une case aléatoire
        y = int(random() * 20)
        
        if grille[y][x] == 0:              #si morte, la rend vivante
            grille[y][x] = 1
            compteur += 1
    
    print("Cases vivantes calculées:",case_vivante)   #TEST, À ENLEVER
    print("Cases vivantes réelles:",compteur)
    return grille

           
def dessiner(grille):
    set_screen_mode(200, 200)                            #20x20 cases de 10px

    for y in range(len(grille)):                #trace le contour des cases 
        for x in range(len(grille[y])):
            pu()
            goto(x * 10, -y * 10)             #coin de depart chaque pixel
            pd()                #-y car y de notre grille augmente vers le bas
            fd(10)                            
            rt(90)
            fd(10)
            rt(90)
            fd(10)
            rt(90)
            fd(10)
            rt(90)

            if grille[y][x] == 1:              #si case vivante: fill en rouge
                for py in range(1, 10):     #part du coins et fill en balayant
                    for px in range(1, 10):              #chaque pixel
                        set_pixel(x * 10 + px, y * 10 + py, "#f00")
            
            else:                              #si case morte: fill en blanc
                for py in range(1, 10):
                    for px in range(1, 10):
                        set_pixel(x * 10 + px, y * 10 + py, "#fff")


grille = init(1)
dessiner(grille)

for ligne in grille:
    print(ligne)

    


    

    
  
