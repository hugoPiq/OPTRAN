# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 11:27:08 2019

@author: Hugo
"""
##import API as api
prixtransport=0
Prixmat=[]

def coutV1(A,B,idmat):      #Renvoie une liste [distance,prix ]
    #distance=api.long(A,B,) ####à modifier, distance est proportionnelle à l'impact carbone.
    prix=prixtransport*distance + Prixmat[idmat]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
    return [distance,prix]

idmat=0 #identifiant du matériaux ou prix décharge
A=0   #Coordonnées chantier
LtrajetsAB=[] #distances de tous les trajets de A à B (décharges)
LtrajetsABCA=[] #distances de tous les trajets de A à B à C à A (chantier)
Ldecharges=[] #liste de toutes les décharges (coordonnées)
Lmagasin=[] #Liste de tous les magasins (coordonées)


"Détermination du coût de chaque trajet ABCA"
for i in range(len(Ldecharges)):        #Cout de chaque trajet A à B pour chaque décharges
    LtrajetsAB.append(coutV1(A,Ldecharges[i],idmat))
for j in range(len(LtrajetsAB)):
    for i in range(len(Lmagasin)):                          #Pour chaque trajet AB, on ajoute chaque trajet BC possible et CA correspondant
        a=LtrajetsAB(j)+coutV1(Ldecharges[j],Lmagasin[i],idmat)+coutV1(Lmagasin[i],A,0)
        LtrajetsABCA.append(a)

"Tris du meilleur trajet en fonction des paramètres"
#Détermination du poids/ prix max et min.
def maxi(L,rg):    #fonction maxi spécifique pour calculer max liste du type L=[x,[x,y]]
    if rg==0:
        maxi=L[0][0]
        for i in range(1,len(L)):
            if L[i][0]>maxi:
                maxi=L[i][0]
    else :
       maxi=L[0][1]
       for i in range(1,len(L)):
            if L[i][0]>maxi:
                maxi=L[i][1]
    return maxi


def mini(L,rg):    #fonction mini spécifique pour calculer max liste du type L=[x,[x,y]]
    if rg==0:
        mini=L[0][0]
        for i in range(1,len(L)):
            if L[i][0]<mini:
                mini=L[i][0]
    else :
       mini=L[0][1]
       for i in range(1,len(L)):
            if L[i][0]<mini:
                mini=L[i][1]
    return mini


prixmax=maxi(LtrajetsABCA,0)
prixmin=mini(LtrajetsABCA,0)
poidsmin=maxi(LtrajetsABCA,1)
poidsmax=mini(LtrajetsABCA,1)

pourcentprix=0         #Déterminé par l'utilisateur
pourcentpoids=0


def points(L,pourcentprix,pourcentpoids):      #attribution des points en fonction des paramètres
    a,b=L     #a=prix, b=poids CO2
    return pourcentprix*(a-prixmin)/(prixmax-prixmin)+pourcentpoids*(b-poidsmin)/(poidsmax-poidsmin)

Lnontriée=[]
for i in range(len(LtrajetsABCA)):
    a=points(LtrajetsABCA[i])
    Lnontriée.append(a)

#Quicksort #ressort une liste triée.

          
#Séléction du premier        
    
