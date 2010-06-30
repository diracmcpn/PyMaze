#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------#
#Programme générant un labyrinthe rectangulaire de taille m X n
#Creation : 04/12/2008
#Date de modification : 05/12/2008
#Par : Dirac

import Tkinter
import random
import numpy

class Dedale(Tkinter.Tk):
    """Application générant un labyrinthe"""
    
    def __init__(self,ligne,colonne,taille,origine):
        Tkinter.Tk.__init__(self)
        
        #Attributs
        self.ligne=ligne #Nombre de ligne
        self.colonne=colonne #nombre de colonne
        self.taille=taille #taille de la cellule carrée
        self.origine=origine #position origine du labyrinthe
        self.pile=[] #Murs visités stockés
        self.i=0 #indice de la pile
        
        #Creation du canvas"
        self.can=Tkinter.Canvas(self,bg="white",
                                height=self.ligne*self.taille+self.origine[0],
                                width=self.colonne*self.taille+self.origine[1])
        
        self.creerGrille() #Creation de la grille
        self.grilleNonVisite() #Associe un zero à toutes les cellules de la grille
        
        cell=self.choixCellule() #Choix aléatoire d'une cellule
        self.celluleVisite(cell) #La cellule est alors marqué comme vraie
        cellpossible=self.cellulePossible(cell) #Regarde les cellules voisines possibles
        ##print self.pile
        #choisit une cellule possible si elle existe,ouvre le mur ou autrement utilise la cellule précedente
        case=self.choixCellulePossible(cellpossible,cell)
        
        while case!=cell:
            self.celluleVisite(case)
            cellpossible=self.cellulePossible(case)
            ##print self.pile 
            case=self.choixCellulePossible(cellpossible,case)
        self.creerInOut()#Entree
        self.creerInOut()#Sortie
            
        self.can.pack()
    
    def creerGrille(self):
        "Creation d'une grille"
        
        for m in range(self.ligne+1):
            self.can.create_line(self.origine[0],self.origine[1]+m*self.taille,
                        self.origine[0]+self.colonne*self.taille,self.origine[1]+m*self.taille,width=1)
        for n in range(self.colonne+1):
            self.can.create_line(self.origine[0]+n*self.taille,self.origine[1],
                        self.origine[0]+n*self.taille,self.origine[1]+self.ligne*self.taille,width=1)
    
    def grilleNonVisite(self):
        "Associe un 0 à toutes les cellules"
        self.grille=numpy.zeros((self.ligne,self.colonne))
        ##print "Grille de départ :",self.grille
    
    def choixCellule(self):
        "Choisit la première cellule"
        
        card=['N','S','O','E']
        cote=random.choice(card)
        if cote=='N':
            cell=(0,random.randrange(self.colonne))
        elif cote=='S':
            cell=(self.ligne-1,random.randrange(self.colonne))
        if cote=='O':
            cell=(random.randrange(self.colonne),0)
        if cote=='E':
            cell=(random.randrange(self.colonne),self.colonne-1)
        
        ##print "cellule de départ:",cell
        return cell
    
    def celluleVisite(self,cellule):
        "Marquez vrai quand la cellule est visité"
        self.grille[cellule]=1
        ##print "Mise à jour de la grille :",self.grille
        
    def cellulePossible(self,cellule):
        "Regarde les cellules possibles adjacentes"
        possible=[]
        
        if cellule[0]-1>=0:
            if not(self.grille[cellule[0]-1,cellule[1]]):
                possible.append((cellule[0]-1,cellule[1]))
        if cellule[0]+1<(self.ligne):
            if not(self.grille[cellule[0]+1,cellule[1]]):
                possible.append((cellule[0]+1,cellule[1]))
        if cellule[1]-1>=0:
            if not(self.grille[cellule[0],cellule[1]-1]):
                possible.append((cellule[0],cellule[1]-1))
        if cellule[1]+1<(self.colonne):
            if not(self.grille[cellule[0],cellule[1]+1]):
                possible.append((cellule[0],cellule[1]+1))
        
        #print "les cellules possibles :",possible
        return possible
    
    def stockCellule(self,cellule):
        "Stocke la cellule en cours"
        self.pile.append(cellule)
        ##print "cellule stockée:",self.pile
    
    def choixCellulePossible(self,possible,cellule):
        "Choisit parmi les cellules possibles ou revient à la case précédente"
        
        if possible!=[]:
            self.stockCellule(cellule) #Stocke la cellule en cours
            choix=random.choice(possible)
            self.supprimeMur(choix,cellule)
            self.i=0
            #print 'choix:',choix
        
        else:
            self.i=self.i+1
            choix=self.pile[-self.i]
        
        ##print "cellule actuelle:",choix
        return choix
        
        
    def supprimeMur(self,adjacent,actuel):
        "Recolore le coté d'une cellule en blanc selon sa cellule adjacente"
        
        if actuel[0]==adjacent[0]-1:
            a,b,c,d=0,0,1,0
        elif actuel[1]==adjacent[1]+1:
            a,b,c,d=1,0,1,1
        elif actuel[0]==adjacent[0]+1:
            a,b,c,d=0,1,1,1
        elif actuel[1]==adjacent[1]-1:
            a,b,c,d=0,0,0,1
        
        x1=self.origine[0]+(adjacent[1]+a)*self.taille
        y1=self.origine[1]+(adjacent[0]+b)*self.taille
        x2=self.origine[0]+(adjacent[1]+c)*self.taille
        y2=self.origine[1]+(adjacent[0]+d)*self.taille
        
        self.can.create_line(x1,y1,x2,y2,fill='white')
    
    def creerInOut(self):
        "Crée une entrée et une sortie sur le labyrinthe de maniére aléatoire"
        
        card=['N','S','O','E']
        cote=random.choice(card)
        print cote
        if cote=='N':
            cell=(0,random.randrange(self.colonne))
            a,b,c,d=0,0,1,0
        elif cote=='S':
            cell=(self.ligne-1,random.randrange(self.colonne))
            a,b,c,d=0,1,1,1
        elif cote=='O':
            cell=(random.randrange(self.colonne),0)
            a,b,c,d=0,0,0,1
        elif cote=='E':
            cell=(random.randrange(self.colonne),self.colonne-1)
            a,b,c,d=1,0,1,1
        
        x1=self.origine[0]+(cell[1]+a)*self.taille
        y1=self.origine[1]+(cell[0]+b)*self.taille
        x2=self.origine[0]+(cell[1]+c)*self.taille
        y2=self.origine[1]+(cell[0]+d)*self.taille
        
        print x1,y1,x2,y2
        self.can.create_line(x1,y1,x2,y2,fill='white')
    

    
if __name__== "__main__":
    app=Dedale(ligne=50,colonne=50,taille=5,origine=(1,1))
    app.title("PyMaze_v2")
    app.mainloop()
    