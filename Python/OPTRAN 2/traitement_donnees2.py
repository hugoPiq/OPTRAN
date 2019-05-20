#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OPTRAN.traitement_donnees2
(C) Hugo Piquard, 2018-2019 <piquardhugo@yahoo.fr>

Module permetant d'obtenir les données nécessaires au programme 
à partir d'un fichier Json remplit par l'utilisateur 
ainsi qu'ajouter les coordonnées de chaque lieux (magasins, décharges).
"""

import json
import requests




def importation_donnees(nom_fichier):
    """Importe les données à partir d'un fichier Json et resortant une bibliothèque sous la forme 
    "adresse","matériaux"[{"nom","prix"}]
    """
    with open(nom_fichier) as Donnees_specifique:
        donnees=json.load(Donnees_specifique)
    return donnees


def ajout_coordonnéesAPI(donnees,APIkey):
    """ Ajoute à chaque adresse les coordonneés géographiques correspondantes.
        Remarque: cette fonction utilise une API Key Google earth.
    """
    if APIkey=="None":  #Pour les tests sans APIkeys, les coordonnées sont déjà renseignées
        return donnees
    else:
        
        for i in range(len(donnees["decharges"])): #Utilisation d'une API key pour obtenir les coordonnées des décharges
            adresse = str(donnees["decharges"][i]["adresse"])
            rep = requests.get("http://maps.googleapis.com/maps/api/geocode/json?key="+ str(APIkey)+ "address="+ adresse+"%s&sensor=false")
            coordonnees = rep.json()
            donnees["decharges"][i]["coordonnees"] = coordonnees
        
        for i in range(len(donnees["depots"])): #Utilisation d'une API key pour obtenir les coordonnées des dépots
            adresse = str(donnees["depots"][i]["adresse"])
            rep = requests.get("http://maps.googleapis.com/maps/api/geocode/json?key="+ str(APIkey)+ "address="+ adresse+"%s&sensor=false")
            coordonnees = rep.json()
            donnees["depots"][i]["depots"] = coordonnees
        
        adresse = str(donnees["adresse chantier"]) #Utilisation d'une API key pour obtenir les coordonnées du chantier
        rep = requests.get("http://maps.googleapis.com/maps/api/geocode/json?key="+ str(APIkey)+ "address="+ adresse + "%s&sensor=false")
        coordonnees = rep.json()
        donnees["adresse chantier"] = coordonnees

    return donnees
    

def ecriture_json(nom_fichier,cles,donnees_a_ecrire):
    """
    Permet d'écrire dans un fichier json.
    """
    with open(str(nom_fichier)) as f_read:
        dico = json.load(f_read)
    dico[str(cles)] = donnees_a_ecrire
    with open(str(nom_fichier), "w") as f_write:
        json.dump(dico, f_write)

def ecriture_json_liste(nom_fichier,cles1, cles2,donnees_a_ecrire,i):
    """
    Permet d'écrire dans une liste de la cles 1 dans l'élément i de cles 2 d'un fichier json.
    """
    with open(str(nom_fichier)) as f_read:
        dico = json.load(f_read)
    n = len(dico[str(cles1)])
    
    if i >= n :
        ajout_vide = []
        dico[str(cles1)].append(ajout_vide)
        
    ajout = {str(cles2) : donnees_a_ecrire}
    dico[str(cles1)][i].append(ajout)
    with open(str(nom_fichier), "w") as f_write:
        json.dump(dico, f_write)
        
def clear_json(nom_fichier,cles):
    """
    Transforme une liste pleine en une liste vide.
    """
    with open(str(nom_fichier)) as f_read:
        dico = json.load(f_read)
    dico[str(cles)] = []
    
    with open(str(nom_fichier), "w") as f_write:
        json.dump(dico, f_write)
    
    


    




if __name__ == "__main__":
    nom_fichier="Donnees rentrees par utilisateur2.json"
    donnees=importation_donnees(nom_fichier)
    print(ajout_coordonnéesAPI(donnees,donnees["APIkey"]))
    
