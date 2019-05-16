# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 09:04:06 2019

@author: Hugo
"""
import numpy as np
import API as api
prixtransport=0
Prixmat=[]

"Version 1 pour premier programme"
def coutV1(A,B,idmat):
    distance=api.long(A,B) ####à modifier, distance est proportionnelle à l'impact carbone.
    prix=prixtransport*distance + Prixmat[idmat]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
    return [distance,prix]

"Version 2 pour programme optimisé"

prixmin=0
prixmax=0
poidsmax=0
poidsmin=0

def coutV2(A,B,idmat,iddecharge,pourcentprix,pourcentpoids,idmagasin): #idmagasin: numéros du magasin
    distance=api.long(A,B) ####à modifier, distance est proportionnelle à l'impact carbone.
    if iddecharge==0:
        prix=prixtransport*distance + Prixmat[idmagasin][idmat]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
        points=pourcentprix*(prix-prixmin)/(prixmax-prixmin)+pourcentpoids*(distance-poidsmin)/(poidsmax-poidsmin)
    else:
        prix=prixtransport*distance + Prixdecharge[iddecharge]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
        points=pourcentprix*(prix-prixmin)/(prixmax-prixmin)+pourcentpoids*(distance-poidsmin)/(poidsmax-poidsmin)
    return [distance,prix,points,A,B]                              #points: classement 

"Version 3 pour ajout de la pente"
prixmin=0
prixmax=0
poidsmax=0
poidsmin=0
Prixdecharge=0

a=0
b=0
n=0
ro=0
S=0
Cx=0
delta=0
M=0
Cm=0



def f(x,ro,S,Cx,delta,M,alpha,Cm):  #Fonction vitesse pente
    Rroue=0,5715  #22,7 pouces
    g=9.81
    return x**3*0.5*ro*S*Cx+x*(delta*np.cos(alpha)/Rroue+M*g*np.sin(alpha)-Cm/Rroue)



def Dichotomie(f,a,b,n,ro,S,Cx,delta,M,alpha,Cm):
    m=(a+b)/2
    for i in range(n):
        if f(a,ro,S,Cx,delta,M,alpha,Cm)*f(m,ro,S,Cx,delta,M,alpha,Cm)>0:
            a=m
        else:
            b=m
    return (a+b)/2


def coutV3(A,B,idmat,iddecharge,pourcentprix,pourcentpoids,idmagasin,rejet): #idmagasin: numéros du magasin
    vitesseconstante=80     #Vitesse constante du véhicule sur plat
    distance=api.long(A,B) ####à modifier, distance est proportionnelle à l'impact carbone.
    emissionsanspente=distance*rejet  #emission de CO2 g utilisation dans "sans pente"
    alpha=api.rad(A,B)  #angle de la pente
    if alpha<5:     #Si pas de pente ou très faible, cout identique a coutV2. 
        "Détermination sans pente"
        if iddecharge==0:
            prix=prixtransport*distance + Prixmat[idmagasin][idmat]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
            points=pourcentprix*(prix-prixmin)/(prixmax-prixmin)+pourcentpoids*(emissionsanspente-poidsmin)/(poidsmax-poidsmin)
        else:
            prix=prixtransport*distance + Prixdecharge[iddecharge]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
            points=pourcentprix*(prix-prixmin)/(prixmax-prixmin)+pourcentpoids*(distance-poidsmin)/(poidsmax-poidsmin)
        return [distance,prix,points,A,B]
    else:
        "Détermination émission avec pente"
        t=distance*rejet/vitesseconstante #temps trajet pour trajet sans pente
        vitessevariable=Dichotomie(f,a,b,n,ro,S,Cx,delta,M,alpha,Cm)  #Vitesse si pente
        emission=t*distance*rejet/vitessevariable  #G CO2 émis avec pente.
        if iddecharge==0:
            prix=prixtransport*distance + Prixmat[idmagasin][idmat]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
            points=pourcentprix*(prix-prixmin)/(prixmax-prixmin)+pourcentpoids*(emission-poidsmin*rejet)/(rejet*(poidsmax-poidsmin))
        else:
            prix=prixtransport*distance + Prixdecharge[iddecharge]   #Prix pour un trajet de A à B correspond au prix du trajet (salaire cauffeur, cout assurance evntuelle)*la distance du trajet + le prix du matériaux (prix ramené à la quantité prise par le camion).
            points=pourcentprix*(prix-prixmin)/(prixmax-prixmin)+pourcentpoids*(emission-poidsmin*rejet)/(rejet*(poidsmax-poidsmin))
        return [emission,prix,points,A,B]                              #points: classement 