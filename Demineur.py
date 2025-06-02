##DEMINEUR - LE JEU EST TEL QUE VOTRE CASE DE DEPART N'EST JAMAIS UNE BOMBE

from tkinter import * #interface
import numpy as np #matrices
import random #bombes aléatoires

from collections import deque #faire des piles
from tkinter import messagebox #message d'erreurs & de réussites


##FONCTIONS QUI ME DONNENT LES VOISINS D'UNE COORDONEE QLQC DE MA MATRICE
def rectangle(B,u,v):
    if (u >= 1 and u<=6) and (v>=1 and v<=6):
        return [B[u-1][v-1],B[u-1][v],B[u-1][v+1],B[u][v-1],B[u][v+1],B[u+1][v-1],B[u+1][v],B[u+1][v+1]]
    if u==0 and v==0:
        return [B[u][v+1],B[u+1][v+1],B[u+1][v]]
    if u==7 and v==7:
        return [B[u][v-1],B[u-1][v],B[u-1][v-1]]
    if u==7 and v==0:
        return [B[u][v+1],B[u-1][v],B[u-1][v+1]]
    if u==0 and v==7:
        return [B[u][v-1],B[u+1][v],B[u+1][v-1]]
    for i in range(1,7):
        if u==0 and v==i:
            return [B[u+1][v-1],B[u+1][v],B[u+1][v+1],B[u][v-1],B[u][v+1]]
    for i in range(1,7):
        if u==i and v==0:
            return [B[u-1][v+1],B[u][v+1],B[u+1][v+1],B[u-1][v],B[u+1][v]]
    for i in range(1,7):
        if u==7 and v==i:
            return [B[u-1][v-1],B[u-1][v],B[u-1][v+1],B[u][v-1],B[u][v+1]]
    for i in range(1,7):
        if u==i and v==7:
            return [B[u-1][v-1],B[u][v-1],B[u+1][v-1],B[u-1][v],B[u+1][v]]


def voisin(u,v):
    if (u >= 1 and u<=6) and (v>=1 and v<=6):
        return (u-1,v-1),(u-1,v),(u-1,v+1),(u,v-1),(u,v+1),(u+1,v-1),(u+1,v),(u+1,v+1)
    if u==0 and v==0:
        return (u,v+1),(u+1,v+1),(u+1,v)
    elif u==7 and v==7:
        return (u,v-1),(u-1,v),(u-1,v-1)
    elif u==7 and v==0:
        return (u,v+1),(u-1,v),(u-1,v+1)
    elif u==0 and v==7:
        return (u,v-1),(u+1,v),(u+1,v-1)
    for i in range(1,7):
        if u==0 and v==i:
            return (u+1,v-1),(u+1,v),(u+1,v+1),(u,v-1),(u,v+1)
    for i in range(1,7):
        if u==i and v==0:
            return (u-1,v+1),(u,v+1),(u+1,v+1),(u-1,v),(u+1,v)
    for i in range(1,7):
        if u==7 and v==i:
            return (u-1,v-1),(u-1,v),(u-1,v+1),(u,v-1),(u,v+1)
    for i in range(1,7):
        if u==i and v==7:
            return (u-1,v-1),(u,v-1),(u+1,v-1),(u-1,v),(u+1,v)

## LES CONSTANTES

PAD=0.1
COTE=40
SIDE= COTE + 2*PAD
R=[0,1,2,3,4,5,6,7]

Nb_ligne=8
Nb_colonne=8
LARG= Nb_colonne*2*SIDE
HAUT=Nb_ligne*2*SIDE
X=Y=SIDE/2
c=0



fenetre=Tk()
fenetre.geometry("320x320")
cnv=Canvas(fenetre,width= LARG, height= HAUT, background= "white smoke")
cnv.pack()

## L'INTERFACE PREMIERE
#Les case grises
cov=[]
for i in range(8):
    Li=[]
    for j in range(8):
        centre=(j*SIDE + X, i*SIDE + Y)
        covv= cnv.create_rectangle(40*j +0.2,40*i +0.2, 40*(j+1) + 0.2, 40*(i+1) +0.2, fill="white", outline = "black")
        Li.append(covv)
    cov.append(Li)

##LE CLIC
D=[] #liste des cases où nous sommes déjà passées (au coup n-1 + n-2 +...)
def premierclic(event):
    global x0, y0,c, LIST, booleen, ids_cover, lig, col, reste, courant, depl, D
    if booleen:
        ids_cover=[]
        depl= [(-1,0),(1,0),(0,-1),(0,1),(1,1),(-1,1),(1,-1),(-1,-1)]
        x0, y0=(int((event.y)// SIDE), int((event.x)/SIDE))
        LIST=jeu(x0,y0)
        booleen=False

        for i in range(Nb_ligne):
            L=[]
            for j in range(Nb_colonne):
                centre=(j*SIDE + X, i*SIDE + Y)
                nbr=LIST[i][j]
                cnv.create_text(centre,fill='black',text= nbr)
                id_cover=cnv.create_rectangle(40*j +0.2,40*i +0.2, 40*(j+1) + 0.2, 40*(i+1) +0.2, fill="grey", outline = "black")
                L.append(id_cover)
            ids_cover.append(L)

        cnv.delete(ids_cover[x0][y0])
    lig,col = int((event.y)// SIDE),int((event.x)/SIDE)
    if LIST[lig][col]==9:
        cnv.delete(ids_cover[lig][col])
        messagebox.showinfo("Resultat", " Vous avez perdu!", icon= 'error')
        quit()
    elif LIST[lig][col]!=9 and LIST[lig][col]!=0:
        c=c+1
        cnv.delete(ids_cover[lig][col])
        D.append((lig,col))
        print(c)

    if LIST[lig][col]==0: # cas ou le clic serait sur une case vide
        reste=deque()
        reste.append((lig,col))
        dejavu=[] #liste des cases où nous passons (au coup n seulement)
        while len(reste)!=0: #☻parcours en largeur
            courant= reste.popleft()
            cnv.delete(ids_cover[courant[0]][courant[1]]) #on supprime la case grise où nous sommes
            for dep in depl:
                voisinage= [tuple(p+q for p,q in zip(courant,dep))] #on fait tout les déplacements possibles autour

                if LIST[courant[0]][courant[1]]==0 : #avec certaines cdts (que la voisine soit vide, pas déja vue au coup d'avant (n-1), si le voisin n'est pas en dehors de la grille)
                    pos=voisin(courant[0],courant[1])
                    for vois in voisinage:
                        if vois not in dejavu:
                            if vois in pos :
                                reste.append(vois)
            dejavu.append(courant)
        intersect=list(set(D) & set(dejavu))
        c= c+ len(set(dejavu)) -len(intersect) # or quand on parcourt la grille, parfois on est en intersection avec le découvrement du prochain clic (déja vu et D possède un ou des élements communs), on enlève donc ce que l'algorithme à compter en trop dans le compteur.

        D= D + dejavu
        print(c)
    if c>=56:
        messagebox.showinfo("Resultat", "Bravo, vous avez gagné !")
        quit()

##LE JEU: CETTE FONCTION NOUS DONNE UNE MATRICE ALEATOIRE AVEC 8 BOMBES (notées: '9'), TEL QU'EN x0,y0 IL N'Y AIT PAS DE BOMBE
def jeu(x0,y0):
    mine=8
    A=np.zeros((8,8))
    A[x0][y0]=77.
    if (x0 >= 1 and x0<=6) and (y0>=1 and y0<=6):
        A[x0][y0]=77.
        A[x0-1][y0-1]=77.
        A[x0-1][y0]=77.
        A[x0-1][y0+1]=77.
        A[x0][y0-1]=77.
        A[x0][y0+1]=77.
        A[x0+1][y0-1]=77.
        A[x0+1][y0]=77.
        A[x0+1][y0+1]=77.
    if x0==0 and y0==0:
        A[x0][y0]=77.
        A[x0][y0+1]=77.
        A[x0+1][y0+1]=77.
        A[x0+1][y0]=77.
    if x0==7 and y0==7:
        A[x0][y0]=77.
        A[x0][y0-1]=77.
        A[x0-1][y0]=77.
        A[x0-1][y0-1]=77.
    if x0==7 and y0==0:
        A[x0][y0]=77.
        A[x0][y0+1]=77.
        A[x0-1][y0]=77.
        A[x0-1][y0]=77.
    if x0==0 and y0==7:
        A[x0][y0]=77.
        A[x0+1][y0]=77.
        A[x0+1][y0-1]=77.
        A[x0][y0-1]=77.
    for i in range(1,7):
        if x0==0 and y0==i:
            A[x0][y0]=77.
            A[x0+1][y0-1]=77.
            A[x0+1][y0]=77.
            A[x0+1][y0+1]=77.
            A[x0][y0-1]=77.
            A[x0][y0+1]=77.
    for i in range(1,7):
        if x0==i and y0==0:
            A[x0][y0]=77.
            A[x0-1][y0+1]=77.
            A[x0][y0+1]=77.
            A[x0+1][y0+1]=77.
            A[x0-1][y0]=77.
            A[x0+1][y0]=77.
    for i in range(1,7):
        if x0==7 and y0==i:
            A[x0][y0]=77.
            A[x0-1][y0]=77.
            A[x0-1][y0]=77.
            A[x0-1][y0+1]=77.
            A[x0][y0-1]=77.
            A[x0][y0+1]=77.
    for i in range(1,7):
        if x0==i and y0==7:
            A[x0][y0]=77.
            A[x0-1][y0-1]=77.
            A[x0][y0-1]=77.
            A[x0+1][y0-1]=77.
            A[x0-1][y0]=77.
            A[x0+1][y0]=77.
    while mine!=0:
        R1=random.choice(R)
        R2=random.choice(R)
        if A[R1][R2]!=77. and A[R1][R2]!=9.:
            A[R1][R2]=9.
            mine-=1
#on a placé des mines sauf en la coordonnée du premier clic - (x0,y0)



    for i in range(8):
        for j in range(8):
            if A[i][j]!=9.:
                if rectangle(A,i,j).count(9.)==1:
                    A[i][j]=1
                elif rectangle(A,i,j).count(9.)==2:
                    A[i][j]=2
                elif rectangle(A,i,j).count(9.)==3:
                    A[i][j]=3
                elif rectangle(A,i,j).count(9.)==4:
                    A[i][j]=4
                elif rectangle(A,i,j).count(9.)==5:
                    A[i][j]=5
                elif rectangle(A,i,j).count(9.)==6:
                    A[i][j]=6
                elif rectangle(A,i,j).count(9.)==7:
                    A[i][j]=7
                elif rectangle(A,i,j).count(9.)==8:
                    A[i][j]=8

# on a compté le nombres de mines voisinant chaque cases


    for i in range(8):
        for j in range(8):
            if A[i][j]==77.:
                A[i][j]=0.
# on remplace le pourtour de (x0,y0) en 0. Car on avait des 77. - voir plus haut
    LIST=[]
    for i in range(8):
        LIST.append([])
        for j in range(8):
            LIST[i].append(int(A[i][j]))
    return LIST




##AFFICHAGE -
booleen=True
print("A 56, vous avez gagné")
cnv.bind("<Button>", premierclic)
fenetre.mainloop()
