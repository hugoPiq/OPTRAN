#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OPTRAN.main
(C) Hugo Piquard, 2018-2019 <piquardhugo@yahoo.fr>

Module permetant de calculer les distances entre les différents lieux.
"""
from math import sin, cos, acos, pi , sqrt
#import googlemaps





def cacul_km_trajetAPI(coordonnees1,coordonnees2,APIkey):
    """"
    Calcul la distance à parcourir entre l'adresse 1 et l'adresse 2
    Remarque: ce programme utilise une API key
    """
    if APIkey == "None":
        distance = sqrt(2)*distance_sans_APIkey(float(coordonnees1["lat"]),float(coordonnees1["long"]),float(coordonnees2["lat"]),float(coordonnees2["long"]))/1000
    
    else:
        gmaps = googlemaps.Client(APIkey)  #renseigne la API key
        trajet = gmaps.direstions(str(coordonnees1["lat"]) + "," + str(coordonnees1["long"]), str(coordonnees2["lat"]) + "," + str(coordonnees2["long"]), mode = "driving")
        distance = 1,60934*int(trajet[0]['legs'][0]['distance']['text'])     # *1,60934 pour conversion en km
    return distance

 

 

def convertisseur_deg_rad(angle):
    """Convertit un angle "degrés décimaux" en "radians"
    """
    return angle/180*pi
 

def distance_sans_APIkey(latA, longA, latB, longB):
    """
    Retourne la distance en mètres entre les 2 points A et B connus grâce à
    leurs coordonnées GPS (en radians) sans utilisé d'APIkey
    Remarque: il s'agit de la distance à "vol d'oiseau".
    """
    latA=convertisseur_deg_rad(latA)        #Conversion en rad
    longA=convertisseur_deg_rad(longA)
    latB=convertisseur_deg_rad(latB)
    longB=convertisseur_deg_rad(longB)
    
    rayon_terre = 6378137   # Rayon de la terre en mètres (sphère IAG-GRS80)
            
    angle= acos(sin(latA)*sin(latB) + cos(latA)*cos(latB)*cos(abs(longB-longA))) # angle en radians entre les 2 points
    
    return angle*rayon_terre   # distance entre les 2 points, comptée sur un arc de grand cercle
 














if __name__ == "__main__":
    coordonnees1 = { "lat" : 47.390668, "long" : 0.689319}
    coordonnees2 = { "lat" : 45.826516, "long" : 1.260290}
    APIkey = "None"
    print(cacul_km_trajetAPI(coordonnees1,coordonnees2,APIkey))  