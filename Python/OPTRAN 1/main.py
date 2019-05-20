#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OPTRAN.main
(C) Hugo Piquard, 2018-2019 <piquardhugo@yahoo.fr>
Fichier principal du programme.
"""
import traitement_donnees as traitement
import meilleur_trajet as mtrajet
import bilan


def OPTRAN(nom_fichier):
    ''' Programme complet recevant un fichier Json de toutes les données (adresses magasins, prix produits, ...) 
    et retournant les trajets à effectuer (adresse, produit et prix) 
    selon les critères spécifiés dans le fichier données.
    '''
    Liste_meilleur_trajet_pour_chaque_materiaux=[]
    
    
    donnees=traitement.importation_donnees(nom_fichier) #ok
    donnees=traitement.ajout_coordonnéesAPI(donnees,donnees["APIkey"])   #ok
    
    for i in range(len(donnees["materiaux necessaires"])):
        Liste_meilleur_trajet_pour_chaque_materiaux.append(mtrajet.trajet_pour_materiaux(donnees,donnees["materiaux necessaires"][i]["nom"]))
    
    bilan.total(donnees,Liste_meilleur_trajet_pour_chaque_materiaux,"resultat.json")
    print(traitement.importation_donnees("resultat.json"))

        


if __name__ == "__main__":
    print(OPTRAN("Donnees rentrees par utilisateur  sans APIkey.json"))