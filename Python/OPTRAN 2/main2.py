#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OPTRAN2.main
(C) Hugo Piquard, 2018-2019 <piquardhugo@yahoo.fr>
Fichier principal du programme OPTRAN 2.
"""
import traitement_donnees as traitement



def OPTRAN2(nom_fichier):
    ''' Programme complet recevant un fichier Json de toutes les données (adresses magasins, prix produits, planning ...) 
    et retournant les trajets à effectuer (adresse, produit et prix) pour chaque date afin de respecter un planning
    selon les critères spécifiés dans le fichier données.
    '''

    donnees=traitement.importation_donnees(nom_fichier) 
    donnees=traitement.ajout_coordonnéesAPI(donnees,donnees["APIkey"])   
    
    
    


        


if __name__ == "__main2__":
    print(OPTRAN2("Donnees rentrees par utilisateur  sans APIkey.json"))