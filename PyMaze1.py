#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------#
#Programme générant un labyrinthe rectangulaire composé de m lignes et n colonnes, soit m*n cases.
#Chaque case est constituée de 4 murs qui peuvent être un bord ou un mur interne. Elle possède un numéro
 
#Algorithme utilisé : Fusion aléatoire de chemins
# 1 - On part d'un labyrinthe où toutes les cases sont fermées et associées à un numéro unique.
# 2 - À chaque itération, on choisit un mur interne à ouvrir de manière aléatoire.
# 3 - On vérifie que les deux cases séparées par le mur ont des numéros différents. 
#     Si les numéros sont identiques, c'est que les deux cases sont déjà reliées et appartiennent donc au même chemin. On ne peut donc pas ouvrir le mur.
#     Si les numéros sont différents, le mur est ouvert, les deux cases sont liées entre elles, elles forment un chemin et le numéro de la première case est affecté à toutes les cases du second chemin ou vice-versa.
# 4 - Au final, on obtient un chemin unique lorsque le nombre de murs ouverts atteint m*n − 1

#Creation : 29/11/2008
#Date de modification : 14/03/2011
#Par : Dirac

import random
import Tkinter
import time

class Mur:
	"""Classe représentant un mur"""
	
	def __init__(self, identiteCase1, identiteCase2, numeroCase1, numeroCase2, directionCase1, directionCase2, etat):
		"""	Paramètres : 
				- identiteCase1,identiteCase2  correspondent au identité des deux cases séparées par le mur. Pour un bord, les identités sont identiques.
				- numeroCase1, numeroCase2 correspondent aux numéros des deux cases séparées par le mur.
				- directionCase1, directionCase2 correspondent à la direction du mur par rapport à la case1 respectivement la case 2
				- etat: 0 (fermé) et 1 (ouvert).
		"""	
		self.identiteCase1=identiteCase1
		self.identiteCase2=identiteCase2
		self.numeroCase1=numeroCase1
		self.numeroCase2=numeroCase2
		self.directionCase1=directionCase1
		self.directionCase2=directionCase2
		self.etat=etat

	def __repr__(self):
		"""Affiche Mur"""
		return "Mur id1={0} id2={1} num1={2} num2={3} dir1={4} dir2={5} etat={6} \n".format(self.identiteCase1, self.identiteCase2, self.numeroCase1, self.numeroCase2, self.directionCase1, self.directionCase2, self.etat)

class Labyrinthe:
	"""Classe représentant le labyrinthe"""

	def __init__(self, nb_lignes, nb_colonnes):
		self.nb_lignes = nb_lignes #Nombre de lignes du labyrinthe
		self.nb_colonnes = nb_colonnes #Nombre de colonnes du labyrinthe
		self.i_max = nb_lignes-1 #Indice max des lignes
		self.j_max = nb_colonnes-1 #Indice max des colonnes
		
		self.nb_cases = self.nb_lignes*self.nb_colonnes #Nombre de cases totales du labyrinthe
		self.nb_mursAOuvrir = self.nb_cases-1

		#Initialisation du labyrinthe en définissant les murs internes et les bords
		self.index = range(self.nb_cases)
		self.mursInternes = []
		self.mursBords= []
		
		for n in self.index:

			if (n/self.nb_colonnes)==0: #Première ligne
				mur = Mur(n, n, n, n, "N","N", 0) #Bords Nords
				self.mursBords.append(mur)

			if (n%self.nb_colonnes)==0: #Première colonne
				mur = Mur(n, n, n, n, "O","O", 0) #Bords Ouest
				self.mursBords.append(mur)

			if (n%self.nb_colonnes)==self.j_max: #Dernière colonne
				mur = Mur(n, n, n, n, "E", "E", 0) #Bords Est
				self.mursBords.append(mur)

			if (n/self.nb_colonnes)==self.i_max: #Dernière ligne
				mur = Mur(n, n, n, n, "S", "S", 0) #Bords Sud
				self.mursBords.append(mur)

			if (n/self.nb_colonnes)!=0: #N'est pas la Première ligne
				m = self.trouverIndiceCaseAdjacente(n,"N")
				mur = Mur(n, m, n, m, "N", "S", 0) #Murs Nords
				self.mursInternes.append(mur)

			if (n%self.nb_colonnes)!=0: #N'est pas la Première colonne
				m = self.trouverIndiceCaseAdjacente(n,"O") 
				mur = Mur(n, m, n, m, "O", "E", 0)#Murs Ouest
				self.mursInternes.append(mur)


	def trouverIndiceCaseAdjacente(self, n, mur):
		"""Cherche l'indice de la case adjacente à la case d'indice n séparée par 'mur'"""

		# Convertit indice n en indice (i,j)
		i = n/self.nb_colonnes
		j = n%self.nb_colonnes

		if mur=="N": #case Nord
			x = i-1
			y = j
		
		elif mur=="E": #case Est
			x = i
			y = j+1

		elif mur=="S": #case Sud
			x = i+1
			y = j

		elif mur=="O": #case Ouest
			x = i
			y = j-1

		return x*self.nb_colonnes + y

	def generer(self):
		"""Génère le labyrinthe"""

		self.mursChoisis=[]
		self.mursOuverts = 0
		
		while self.mursOuverts<self.nb_mursAOuvrir:

			#Choix d'un mur
			mur = random.choice(self.mursInternes)

			#Verification des numéros
			if mur.numeroCase1!=mur.numeroCase2: #le mur peut-etre ouvert
				mur.etat=1
				self.mursOuverts = self.mursOuverts+1
				#Change les numéros des cases
				numeroCaseMere = mur.numeroCase1 
				numeroCaseAdjacente = mur.numeroCase2
				for wall in self.mursInternes:
					if wall.numeroCase1==numeroCaseAdjacente:
						wall.numeroCase1=numeroCaseMere
					if wall.numeroCase2==numeroCaseAdjacente:
						wall.numeroCase2=numeroCaseMere
				for wall in self.mursChoisis:
					if wall.numeroCase1==numeroCaseAdjacente:
						wall.numeroCase1=numeroCaseMere
					if wall.numeroCase2==numeroCaseAdjacente:
						wall.numeroCase2=numeroCaseMere
				for wall in self.mursBords:
					if wall.numeroCase1==numeroCaseAdjacente:
						wall.numeroCase1=numeroCaseMere
					if wall.numeroCase2==numeroCaseAdjacente:
						wall.numeroCase2=numeroCaseMere
			self.mursChoisis.append(mur)
			self.mursInternes.remove(mur)

class Cellule:
	"""Tracé d'une case de labyrinthe"""

	def __init__(self, centre, taille, epaisseur, color, canvas):
		demiLongueur = taille/2.0
		x0 = centre[0]-demiLongueur
		x1 = centre[0]+demiLongueur
		y0 = centre[1]-demiLongueur
		y1 = centre[1]+demiLongueur
		
		self.can = canvas

		self.background = canvas.create_rectangle(x0,y0,x1,y1,fill=color,width=0)

		self.murNord = canvas.create_line(x0,y0,x1,y0, width=epaisseur)
		self.murEst = canvas.create_line(x1,y0,x1,y1, width=epaisseur)
		self.murSud = canvas.create_line(x1,y1,x0,y1, width=epaisseur)
		self.murOuest = canvas.create_line(x0,y1,x0,y0, width=epaisseur)


	def supprimerMur(self,mur):
		if mur=="N": #case Nord
			self.can.delete(self.murNord)
		elif mur=="E": #case Est
			self.can.delete(self.murEst)
		elif mur=="S": #case Sud
			self.can.delete(self.murSud)
		elif mur=="O": #case Ouest
			self.can.delete(self.murOuest)

	def changerCouleur(self,color):
		self.can.itemconfigure(self.background, fill=color)


class Dedale(Tkinter.Tk):
	"""Application graphique générant un labyrinthe"""

	def __init__(self, nbLignes, nbColonnes, tailleCellule, epaisseurCellule):
		Tkinter.Tk.__init__(self)
		
		self.nbLignes=nbLignes
		self.nbColonnes=nbColonnes

		#Creation d'un canvas"
        	self.can=Tkinter.Canvas(self,bg="white",bd=0,height=tailleCellule*nbLignes+epaisseurCellule,width=tailleCellule*nbColonnes+epaisseurCellule)
		
		#Creation du labyrinthe"
		self.dedale = []
		origin=epaisseurCellule+tailleCellule/2.0

		for i in xrange(nbLignes):
			for j in xrange(nbColonnes):
				case = Cellule((origin+j*tailleCellule,origin+i*tailleCellule), tailleCellule, epaisseurCellule, "white", self.can)
				self.dedale.append(case)
		
		self.can.pack(padx =10, pady =10)

		#générer le labyrinthe
		self.maze = Labyrinthe(self.nbLignes, self.nbColonnes)
		self.maze.generer()
		
		#Creation d'un bouton
		self.flag=1
		bouton=Tkinter.Button(self,text="Générer", command=self.animer)
		bouton.pack(side=Tkinter.BOTTOM, padx =10, pady =10)

	def animer(self):
		"""ouvrir les murs"""
		if self.flag:
			self.flag=0
			for mur in self.maze.mursChoisis:
				if mur.etat:
					self.dedale[mur.identiteCase1].supprimerMur(mur.directionCase1)
					self.dedale[mur.identiteCase1].changerCouleur("#E0E0E0")
					self.dedale[mur.identiteCase2].supprimerMur(mur.directionCase2)
					self.dedale[mur.identiteCase2].changerCouleur("#E0E0E0")
					self.can.update_idletasks()
				time.sleep(0.01)

if __name__== "__main__":
	app=Dedale(40,50,20,2)
    	app.title("PyMaze_v1")
    	app.mainloop()
	
