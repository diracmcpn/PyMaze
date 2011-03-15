#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------#
#Programme générant un labyrinthe rectangulaire composé de m lignes et n colonnes, soit m*n cases.
#Chaque case est constituée de 4 murs qui peuvent être un bord ou un mur interne. Elle possède une variable booléenne qui indique si la case a déjà été visitée ou non
 
#Algorithme utilisé : Exploration exhaustive
# 1 - On part d'un labyrinthe où tous les murs sont fermés et où toutes les cases sont marquées comme non visitées.
# 2 - Au départ, on choisit arbitrairement une case et on la marque comme visitée.
# 3 - Puis on regarde quelles sont les cases voisines non visitées en vérifiant d'abord que le mur qui séparent les deux cases soit fermé et ne soit pas un bord.
#     S'il y a au moins une possibilité, on en choisit une au hasard, on ouvre le mur, on stocke la position en cours dans un tableau servant de pile et on recommence avec la nouvelle case.
#     S'il n'y en pas, on supprime la position en cours de la pile et on revient à la case précédente et on recommence.
# 4 - Lorsque l'on est revenu à la case de départ et qu'il n'y a plus de possibilités (plus de position dans la pile), le labyrinthe est terminé.

#Creation : 29/11/2008
#Date de modification : 15/03/2011
#Par : Dirac

import random
import Tkinter
import time

class Case:
	"""Classe représentant une case de labyrinthe"""
	
	DEFAUT = "0b000000000" # murs internes fermés non visitée
	INORD = "0b000010000" # mur nord interne ouvert non visitée
	IEST = "0b000001000" # mur est interne ouvert non visitée
	ISUD = "0b000000100" # mur sud interne ouvert non visitée
	IOUEST = "0b000000010" # mur Ouest interne ouvert non visitée
	BNORD = "0b100000000" # bord nord fermé non visitée
	BEST = "0b010000000" # bord est fermé non visitée
	BSUD = "0b001000000" # bord sud fermé non visitée
	BOUEST = "0b000100000" # bord Ouest fermé non visitée
	VISITE = "0b000000001" #case visitée
	
	def __init__(self, numero, case):
		"""	Paramètres : 
				- numéro est le numéro unique de la case
				- case est un nombre binaire décrivant l'état des murs entourant la case, le type des murs et si la case a été visitée ou pas. 
				  Il est codé sur 2 lots de 4 bits + 1 bits soit 9 bits au total. Les 4 bits représentent la direction Nord(N), Est(E), Sud(S), Ouest(O) des 4 murs de la case.
				  les 4 premiers bits codent pour un mur interne(0) ou un bord(1).
				  les 4 seconds bits codent pour l'ouverture (1) ou la fermeture (0) des murs.
				  le dernier bit représentent l'état de visite : visité (1), non visitée (0).
				  Ex : "0b110000101" --> Les murs Nord et Est sont des bords fermés, le mur Sud est un mur interne ouvert alors que celui Ouest est fermé. La case a été visitée.
		"""
		self.numero = numero
		self.case = case
	
	def ouvrirMur(self, mur):
		"""Ouvre le mur de la case"""
		self.case = bin(int(self.case,2)|int(mur,2))

	def construireBord(self, mur):
		"""Construit un bord sur la case"""
		self.case = bin(int(self.case,2)|int(mur,2))

	def visiter(self):
		"""Marque la case comme visitée"""
		self.case = bin(int(self.case,2)|int(Case.VISITE,2))

	def isVisite(self):
		"""verifie si la case est visitée"""
		return int(self.case,2)&int(Case.VISITE,2) 
	
	def getListeMursInternesFermes(self):
		"""Renvoie une liste de murs internes fermés"""
		listeMurs = []
		if not(int(self.case,2)&int(Case.BNORD,2)):
			listeMurs.append(Case.INORD)
		if not(int(self.case,2)&int(Case.BEST,2)):
			listeMurs.append(Case.IEST)
		if not(int(self.case,2)&int(Case.BSUD,2)):
			listeMurs.append(Case.ISUD)
		if not(int(self.case,2)&int(Case.BOUEST,2)):
			listeMurs.append(Case.IOUEST)
		return listeMurs

	def getListeMursOuverts(self):
		"""Renvoie une liste de murs ouverts"""
		listeMur = []
		if int(self.case,2)&int(Case.INORD,2):
			listeMur.append(Case.INORD)
		if int(self.case,2)&int(Case.IEST,2):
			listeMur.append(Case.IEST)
		if int(self.case,2)&int(Case.ISUD,2):
			listeMur.append(Case.ISUD)
		if int(self.case,2)&int(Case.IOUEST,2):
			listeMur.append(Case.IOUEST)
		return listeMur
	
	def __repr__(self):
		"""Affiche l'objet"""
		return "Case : {0} \n".format(self.case)
		

class Labyrinthe:
	"""Classe représentant le labyrinthe"""

	def __init__(self, nb_lignes, nb_colonnes):
		self.nb_lignes = nb_lignes #Nombre de lignes du labyrinthe
		self.nb_colonnes = nb_colonnes #Nombre de colonnes du labyrinthe
		self.i_max = nb_lignes-1 #Indice max des lignes
		self.j_max = nb_colonnes-1 #Indice max des colonnes
		
		self.nb_cases = self.nb_lignes*self.nb_colonnes #Nombre de cases totales du labyrinthe

		#Initialisation du labyrinthe en définissant les murs des cases et les bords
		self.index = range(self.nb_cases)
		self.labyrinthe = []

		for n in self.index:
			case = Case(n,Case.DEFAUT)
			if (n/self.nb_colonnes)==0: #Première ligne
				case.construireBord(Case.BNORD) #bords Nord
			if (n%self.nb_colonnes)==0: #Première colonne
				case.construireBord(Case.BOUEST) #bords Ouest
			if (n%self.nb_colonnes)==self.j_max: #Dernière colonne
				case.construireBord(Case.BEST) #bords Est
			if (n/self.nb_colonnes)==self.i_max: #Dernière ligne
				case.construireBord(Case.BSUD) #bords Sud
			self.labyrinthe.append(case)

	def trouverIndiceCaseAdjacente(self, n, mur):
		"""Cherche l'indice de la case adjacente à la case d'indice n séparée par 'mur'"""

		# Convertit indice n en indice (i,j)
		i = n/self.nb_colonnes
		j = n%self.nb_colonnes

		if mur==Case.INORD: #case Nord
			x = i-1
			y = j
		
		elif mur==Case.IEST: #case Est
			x = i
			y = j+1

		elif mur==Case.ISUD: #case Sud
			x = i+1
			y = j

		elif mur==Case.IOUEST: #case Ouest
			x = i
			y = j-1

		return x*self.nb_colonnes + y

	def getMurOppose(self,mur):
		"""Retourne le mur opposé à une case"""
		if mur==Case.INORD:
			return Case.ISUD
		elif mur==Case.ISUD:
			return Case.INORD
		elif mur==Case.IOUEST:
			return Case.IEST	
		elif mur==Case.IEST:
			return Case.IOUEST

	def generer(self):
		""" Génére un labyrinthe """
		
		self.position=[]
		self.etat = [] #Stockage des états successifs pour animation

		#Choix arbitraire d'une case
		indice = random.choice(self.index)

		while 1:
			
			#Marque la case en cours comme visitée
			self.labyrinthe[indice].visiter()
		
			#Cherche cases voisines
			#On récupère d'abord la liste des murs qui sont internes et fermées
			choixMur = self.labyrinthe[indice].getListeMursInternesFermes()
	
			if choixMur!=[]: #Si des murs de la case mère sont internes et fermés

				murPossible=[]
				for mur in choixMur:
					indiceAdjacent=self.trouverIndiceCaseAdjacente(indice, mur)
					if not(self.labyrinthe[indiceAdjacent].isVisite()):
						murPossible.append((mur,indiceAdjacent))
		
				if murPossible!=[]: #Si des cases adjacentes sont non visitées
					couple = random.choice(murPossible) #On choisit alors un couple (mur,indice adjacent) dans liste disponible
					self.labyrinthe[indice].ouvrirMur(couple[0]) #on ouvre alors le mur de la case mère
					mop = self.getMurOppose(couple[0])
					self.labyrinthe[couple[1]].ouvrirMur(mop) #on ouvre aussi le mur de la case adjacente qui est opposé à celle de la case mère
			
					#On stocke la position en cours
					self.position.append(indice)

					self.etat.append(Case(indice,couple[0]))#Stockage pour animation
					self.etat.append(Case(couple[1],mop))#Stockage pour animation

					#On continue en examinant cette fois-ci la case de l'indice adjacent
					indice = couple[1]

				else: #Si toutes les cases adjacentes ont été visitées 
					#On revient à la case précédente en supprimant d'abord la position en cours de la liste de position	
					self.position.pop()
					if self.position!=[]:
						indice = self.position[-1]
					else:
						break
	
			else: #Si tous les murs de la case mère sont des bords ou ouverts
				#On revient à la case précédente en supprimant d'abord la position en cours de la liste de position	
				self.position.pop()
				if self.position!=[]:
					indice = self.position[-1]
				else:
					break

				#Au final on boucle tant que la liste self.position n'est pas vide


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
		if mur==Case.INORD: #case Nord
			self.can.delete(self.murNord)
		elif mur==Case.IEST: #case Est
			self.can.delete(self.murEst)
		elif mur==Case.ISUD: #case Sud
			self.can.delete(self.murSud)
		elif mur==Case.IOUEST: #case Ouest
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
			for c in self.maze.etat:
				self.dedale[c.numero].changerCouleur("#E0E0E0")
				self.dedale[c.numero].supprimerMur(c.case)
				self.can.update_idletasks()
				time.sleep(0.01)
	

if __name__== "__main__":

	app=Dedale(40,50,20,2)
	app.title("PyMaze_v2")
	app.mainloop()

	
