#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OPTRAN.bilan
(C) Hugo Piquard, 2018-2019 <piquardhugo@yahoo.fr>

Module permet d'afficher  les trajets à effectuer et leurs nombres ainsi que le prix et la masse de C02 émise au total.
"""
import traitement_donnees as traitement


def nombre_trajet(materiaux, donnees):
    """
    Détermine le nombre de trajet à effectuer pour un matériaux donné 
    selon la masse nécéssaire renseigner par l'utilisateur.
    """
    contenance_camion = donnees["contenance"]
    quantite = 0
    
    for i in range(len(donnees["materiaux necessaires"])):
        if donnees["materiaux necessaires"][i]["nom"] == str(materiaux):
            quantite = float(donnees["materiaux necessaires"][i]["quantite"])
    if quantite%contenance_camion ==0:
        nombre_trajet = quantite//contenance_camion
    else:
        nombre_trajet = quantite//contenance_camion + 1
    return nombre_trajet


def total(donnees,L,fichier_json):
    """
    Prend en argument une liste contenant le meilleur trajet (numéros lieux), le matériaux et les coûts et
    renvoie un fichier json contenant les trajets à effectuer, leurs nombre te le cout total.
    """
    traitement.clear_json(fichier_json,"trajets") #réinitialise le fichier json resultat
    n = len(L)
    prix_total = 0
    emission_CO2_totale = 0
    for i in range(n):
        traitement.ecriture_json_liste(fichier_json,"trajets","numero trajet",i,i) # ajout numero trajet
        
        numero_decharge = L[i][2]
        adresse1 = donnees["decharges"][numero_decharge]["adresse"]
        traitement.ecriture_json_liste(fichier_json,"trajets","adresse depart",adresse1,i) # ajout adresse décharge
        
        numero_depot = L[i][3]
        adresse2 = donnees["depots"][numero_depot]["adresse"]
        traitement.ecriture_json_liste(fichier_json,"trajets","adresse arrivee",adresse2,i) #ajout adresse depot
        
        materiaux = L[i][4]
        traitement.ecriture_json_liste(fichier_json,"trajets","materiaux",materiaux,i)
        
        nbre_trajet = nombre_trajet(materiaux, donnees)
        traitement.ecriture_json_liste(fichier_json,"trajets","nombre de trajet",nbre_trajet,i) #ajout nombre de trajet
        
        for j in range(len(donnees["depots"][numero_depot]["materiaux"])):
            if donnees["depots"][numero_depot]["materiaux"][j]["nom"] == materiaux:
                prix_materiaux = donnees["depots"][numero_depot]["materiaux"][j]["prix"]
        traitement.ecriture_json_liste(fichier_json,"trajets","prix materiaux",prix_materiaux,i) #ajout prix materiaux
        
        prix_trajet = L[i][0]
        traitement.ecriture_json_liste(fichier_json,"trajets","prix trajet + materiaux",prix_trajet,i) #ajout prix trajet
        
        emission_CO2 = L[i][1]
        traitement.ecriture_json_liste(fichier_json,"trajets","emission CO2",emission_CO2,i) #ajout emission CO2 trajet
        
        prix_total += prix_trajet
        emission_CO2_totale += emission_CO2
    
    traitement.ecriture_json(fichier_json,"prix total",prix_total)
    traitement.ecriture_json(fichier_json,"emission CO2 totale",emission_CO2_totale)
    

    
        
        
    