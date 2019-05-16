# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 20:40:07 2019

@author: Hugo
"""
import API as api


prixtransport=0    #prix chauffeur, assurance etc...
Prixmat=[]  #Prixmat: [[prixmatos1station1,....][prixmatos1station2,....]]
Prixdecharge=[]  #[prixstation1,prixstation2,]
A=0   #Coordonnées du chantier
Ldecharges=[] #liste de toutes les décharges (coordonnées), premier élément: idd  WWWWW
Lmagasin=[] #Liste de tous les magasins (coordonées), premier élément: idd  WWWWWWWW
pourcentprix=0
pourcentpoids=0




"Pour chaque matériaux"
idd=0
idmat=0
prixtransport=0

"Détermination de poidsmax,poidsmin,prixmax,prixmin"
Lprix=[]        #Liste qui stocke tous les prix de la somme des trajets AB et BC
for i in range(len(Ldecharges)):
    for j in range(len(Lmagasin)):
        distance=api.long(A,Ldecharges[i])
        distance2=api.long(Ldecharges[i],Lmagasin[j])
        Lprix.append(prixtransport*distance + Prixdecharge[i]+prixtransport*distance2 + Prixmat[j][idmat])

prixmin=min(Lprix)
prixmax=max(Lprix)

Lpoids=[]        #Liste qui stocke tous les poids des trajets AB et BC
for i in Ldecharges:
    for j in Lmagasin:
        distance=api.long(A,i)
        distance2=api.long(i,j)
        Lpoids.append(distance+ distance2)

poidsmin=min(Lpoids)
poidsmax=max(Lpoids)

"Fonction coût V2 "

def coutV2(A,B,idmat,iddecharge,pourcentprix,pourcentpoids,idmagasin): #idmagasin: numéros du magasin
    distance=api.long(A,B) ####à modifier, distance est proportionnelle à l'impact carbone.
    if iddecharge==0:
        prix=prixtransport*distance + Prixmat[idmagasin][idmat]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
        points=pourcentprix*(prix-prixmin)/(prixmax-prixmin)+pourcentpoids*(distance-poidsmin)/(poidsmax-poidsmin)
    else:
        prix=prixtransport*distance + Prixdecharge[iddecharge]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
        points=pourcentprix*(prix-prixmin)/(prixmax-prixmin)+pourcentpoids*(distance-poidsmin)/(poidsmax-poidsmin)
    return [distance,prix,points,A,B]                              #points: classement 


"Création des listes"
TabB=[ coutV2(A,Ldecharges[i],0,pourcentprix,pourcentpoids,0) for i in range(len(Ldecharges)) ]   #coût des trajets de A à B ( Chantier à décharge)
TabC=[ coutV2(A,Lmagasin[i],idmat,0,pourcentprix,pourcentpoids,i) for i in range(len(Lmagasin)) ]     #coût des trajets de C à A  (magasin à chantier)

"Trier liste par ordre croissant"
#Quicksort triée en fonction des points.


TabBtriée=[]    #liste triée par odre croissantes: [distance,prix,points,coordonées de départ, coordonées d'arrivée]
TabCtriée=[]

"Détermination du mini et cout totale"

mint=10**10     #Minimum global
continueB=True
continueC=True
indexB=0
indexC=0
minC=TabC[0]

while continueB:                #On fait varier dans un premier temps C.
    indexC=0                    #Comme on change de B, on recommence les testes avec tous les autres C
    B=TabBtriée[indexB][2]
    if B + minC>mint:  #si chemin déja supérieur au minimum actuel, on laisse tomber. 
        continueB=False
    else:
        while continueC:           # On texte pour toute les localisations de C.
            C=TabCtriée[indexC][2]
            if C+B >mint:     #si chemin déja supérieur au minimum actuel, on laisse tomber.
                continueC=False
            elif C + B +coutV2(TabBtriée[4][indexB],TabCtriée[4][indexC],0,pourcentprix,pourcentpoids,0)<mint:  #attention, ici les coordonnes de B et C sont ceux de la liste triées TabBtriée et TabCtriée et ne correspondet plus à Ldécharge et Lmagasin.
                mint= C + B +coutV2(indexB,indexC,idmat)[2]
            indexC+=1           
    indexB+=1                   #On incrémente pour tester les autres valeurs de B (comme on ajoute B, lorsque que bonne valeur de B, prendre la précédente
    
