#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OPTRAN.main
(C) Hugo Piquard, 2018-2019 <piquardhugo@yahoo.fr>

Module permet de déterminer le meilleur trajet.
"""

import trajet 



def trajet_pour_materiaux(donnees,materiaux):
    """
    Détermine le meilleur trajet pour un  matériaux en fonctions des préférences de l'utilisateur et 
    renvoie une liste contenant le coût du trajet (prix et CO2), la décharge choisie (numéro), le magasin choisi (numéro) et le matériaux.
    """
    
    pourcentage_carbone = donnees["pourcentage carbone"]
    pourcentage_prix = donnees["pourcentage prix"]
    D=None   #numéro de décharge correspondant aux préférances de l'utilisateur
    M=None   #numéro de magasin correspondant aux préférances de l'utilisateur
    cout_fictif=float("inf")
    
    for i  in range(len(donnees["decharges"])): #pour les décharges
        for j in range(len(donnees["depots"])): #pour les magasins
            for h in range(len(donnees["depots"][j]["materiaux"])): #pour les matériaux présents dans le magasin
                
                cout_reel_prix = cout_trajet(donnees["decharges"][i]["coordonnees"],donnees["adresse chantier"],donnees)[0] + cout_trajet(donnees["decharges"][i]["coordonnees"],donnees["depots"][j]["coordonnees"],donnees)[0] + cout_trajet(donnees["decharges"][j]["coordonnees"],donnees["adresse chantier"],donnees)[0] + donnees["decharges"][i]["prix"] + prix_materiaux(j,h,donnees, materiaux)
                cout_reel_CO2 = cout_trajet(donnees["decharges"][i]["coordonnees"],donnees["adresse chantier"],donnees)[1] + cout_trajet(donnees["decharges"][i]["coordonnees"],donnees["depots"][j]["coordonnees"],donnees)[1] + cout_trajet(donnees["decharges"][j]["coordonnees"],donnees["adresse chantier"],donnees)[1]
                c = (cout_reel_prix*pourcentage_prix + cout_reel_CO2*pourcentage_carbone)/(cout_reel_prix + cout_reel_CO2)
                
                if cout_fictif > c:
                    cout_fictif = c
                    cout_reel_prix_retour = cout_reel_prix
                    cout_reel_CO2_retour = cout_reel_CO2
                    D=i
                    M=j
    
    return [cout_reel_prix_retour,cout_reel_CO2_retour,D,M, materiaux]



def cout_trajet(coordonnees1,coordonnees2,donnees):
    """
    Calcule le prix et l'émission de carbone d'un trajet des coordonnées 1 aux coordonnées 2 
    en prenant en compte les critères utilisateurs. 
    """
    
    prix_transport = donnees["cout km"]
    APIkey = donnees["APIkey"]
    emission_carbone = donnees["emission carbone"]
    
    prix = trajet.cacul_km_trajetAPI(coordonnees1,coordonnees2,APIkey)*prix_transport 
    prix_carbone = trajet.cacul_km_trajetAPI(coordonnees1,coordonnees2,APIkey)*emission_carbone  
    
    return [prix, prix_carbone]



def prix_materiaux(j,h,donnees, materiaux):
    """
    Calcule le prix du matériaux h  présent dans le magasin j.
    Cette fonction vérifie également la présence du produit dans le magasin, si le produit n'y est pas présent, le prix est "infinie".
    """
    if donnees["depots"][j]["materiaux"][h]["nom"] != materiaux:
        prix = float("inf")
    else:
        prix=donnees["depots"][j]["materiaux"][h]["prix"]
    return prix




if __name__ == "__main__":
    import traitement_donnees as traitement
    donnees = traitement.importation_donnees("Donnees rentrees par utilisateur  sans APIkey.json")
    print(trajet_pour_materiaux(donnees,"metal"))




