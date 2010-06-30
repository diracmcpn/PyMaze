#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------#
#Programme générant un labyrinthe rectangulaire de taille m X n
#Creation : 29/11/2008
#Date de modification : 03/12/2008
#Par : Dirac

import Tkinter
import random

class Dedale(Tkinter.Tk):
    """Application générant un labyrinthe"""
    
    def __init__(self,ligne,colonne,taille,origine):
        Tkinter.Tk.__init__(self)
        
        #Attributs
        self.ligne=ligne #Nombre de ligne
        self.colonne=colonne #nombre de colonne
        self.taille=taille #taille de la cellule carrée
        self.origine=origine #position origine du labyrinthe
        self.interne=[] #Murs internes
        self.externe=[] #Murs externes
        self.ouvert=[] #Murs ouverts
        
        #Creation du canvas"
        self.can=Tkinter.Canvas(self,bg="white",
                                height=self.ligne*self.taille+self.origine[0],
                                width=self.colonne*self.taille+self.origine[1])
        
        self.creerGrille() #Creation de la grille
        self.genererMur() #Generation de tous les murs du labyrinthe
        
        unique=0 #compteur du labyrinthe (m*n-1 fois seulement)
        
        while unique!=(self.ligne*self.colonne-1):
            mur=random.choice(self.interne) #Choix d'un mur dans la liste interne
            ##print "mur choisit:",mur
            adjacent=self.findNumero(mur) #Recherche le numéro de la cellule adjacente
            if mur[2]!=adjacent:
                self.supprimeMur(mur) #Supprime le mur sur la grille
                self.updateNumero(adjacent,mur) #Mise à jour des numeros de tous les murs
                self.deplaceMur(mur)
                unique=unique+1
            else:
                self.deplaceMur(mur)
        
        self.creerInOut() #Crée l'entrée et la sortie du labyrinthe
                
        self.can.pack()
    
    def creerGrille(self):
        "Creation d'une grille"
        
        for m in range(self.ligne+1):
            self.can.create_line(self.origine[0],self.origine[1]+m*self.taille,
                        self.origine[0]+self.colonne*self.taille,self.origine[1]+m*self.taille,width=1)
        for n in range(self.colonne+1):
            self.can.create_line(self.origine[0]+n*self.taille,self.origine[1],
                        self.origine[0]+n*self.taille,self.origine[1]+self.ligne*self.taille,width=1)
    
    def genererMur(self):
        "Géneration des murs internes et externes du labyrinthe"
        
        c=0 #numero de la cellule
        for m in range(self.ligne):
            for n in range(self.colonne):
                if m==0:
                    self.externe.append([m,n,c,'N'])
                else:
                    self.interne.append([m,n,c,'N'])
                if n==0:
                    self.externe.append([m,n,c,'O'])
                else:
                    self.interne.append([m,n,c,'O'])
                if m==self.ligne-1:
                    self.externe.append([m,n,c,'S'])
                if n==self.colonne-1:
                    self.externe.append([m,n,c,'E'])
                c=c+1
        
        ##print "mur interne:",self.interne
        ##print "mur externe:",self.externe
    
    def supprimeMur(self,mur):
        "Recolore le coté d'une cellule en blanc selon sa direction"
        
        if mur[3]=='N':
            a,b,c,d=0,0,1,0
        elif mur[3]=='E':
            a,b,c,d=1,0,1,1
        elif mur[3]=='S':
            a,b,c,d=0,1,1,1
        elif mur[3]=='O':
            a,b,c,d=0,0,0,1
        
        x1=self.origine[0]+(mur[1]+a)*self.taille
        y1=self.origine[1]+(mur[0]+b)*self.taille
        x2=self.origine[0]+(mur[1]+c)*self.taille
        y2=self.origine[1]+(mur[0]+d)*self.taille
        
        self.can.create_line(x1,y1,x2,y2,fill='white')
    
    def findNumero(self,mur):
        "Cherche le numero de la cellule adjacente correspondant au mur"
        
        numero=''
        
        if mur[3]=='N':
            i=0
            while (numero==''):
                if i<len(self.interne):
                    if self.interne[i][0:2]==[mur[0]-1,mur[1]]:
                        numero=self.interne[i][2]
                        break
                if i<len(self.externe):
                    if self.externe[i][0:2]==[mur[0]-1,mur[1]]:#on recherche la cellule adjacente dans liste externe
                        numero=self.externe[i][2]
                        break
                if i<len(self.ouvert):
                    if self.ouvert[i][0:2]==[mur[0]-1,mur[1]]:#on recherche la cellule adjacente dans liste externe
                        numero=self.ouvert[i][2]
                        break
                i=i+1
                    
        elif mur[3]=='O':
            i=0
            while numero=='':
                if i<len(self.interne):
                    if self.interne[i][0:2]==[mur[0],mur[1]-1]:
                        numero=self.interne[i][2]
                if i<len(self.externe):
                    if self.externe[i][0:2]==[mur[0],mur[1]-1]:#on recherche la cellule adjacente dans liste externe
                        numero=self.externe[i][2]
                if i<len(self.ouvert):
                    if self.ouvert[i][0:2]==[mur[0],mur[1]-1]:#on recherche la cellule adjacente dans liste externe
                        numero=self.ouvert[i][2]
                i=i+1
        
        ##print "numero adjacent:",numero
        return numero
    
    def updateNumero(self,numero,mur):
        "Met à jour les numeros de tous les murs correspondant au numero de la cellule adjacente"
        
        for i in range(len(self.interne)): #les murs internes
            if self.interne[i][2]==numero:
                self.interne[i][2]=mur[2]
        
        for i in range(len(self.externe)): #les murs externes
            if self.externe[i][2]==numero:
                self.externe[i][2]=mur[2]
        
        if self.ouvert!=[]:
            for i in range(len(self.ouvert)): #les murs ouverts
                if self.ouvert[i][2]==numero:
                    self.ouvert[i][2]=mur[2]
        
        ##print "murs internes modifiés:",self.interne
        ##print "murs externes modifiés:",self.externe
        ##print "murs ouverts modifiés:",self.ouvert
    
    def deplaceMur(self,mur):
        "Deplace le mur choisi de la liste interne dans la liste des murs ouverts"
        self.interne.remove(mur)
        self.ouvert.append(mur)
    
    def creerInOut(self):
        "Crée une entrée et une sortie sur le labyrinthe de maniére aléatoire"
        entree=random.choice(self.externe)
        self.supprimeMur(entree)
        self.externe.remove(entree) #pour ne pas choisir 2 fois le même mur
        sortie=random.choice(self.externe)
        self.supprimeMur(sortie)

if __name__== "__main__":
    app=Dedale(ligne=50,colonne=50,taille=5,origine=(1,1))
    app.title("PyMaze_v1")
    app.mainloop()
    