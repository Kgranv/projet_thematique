# -*- coding: utf-8 -*-
"""
Created on Thu May 25 20:49:53 2023

@author: elisa


PROBLEME : 
    si prelevement !!
    si volume > au reservoir

DIRE a l'utilisateur : 
    - le 1er jour est de toute facon a 100% nutriment 
    - il doit donc mettre 10ml dans le reservoir
"""

import pandas as pd

#met les donnees de concentration imposé dans un dictionnaire
def donnees (nom_fichier):
    data = pd.read_csv(nom_fichier, delimiter=";")
    jour=data['jour'].tolist()
    h1=data['c1']
    h2=data['c2']
    concentration_h1 = []
    concentration_h2 = []                    
    concentration_nut = []
    
    for i in range(len(h1)):
        concentration_h1.append(h1[i]/100)
        concentration_h2.append(h2[i]/100)
        somme = 1-(concentration_h1[i] + concentration_h2[i])
        concentration_nut.append(somme)
        
    concentration_impose = {"jour": jour, "c1":concentration_h1, "c2":concentration_h2, "nut":concentration_nut}
    
    return concentration_impose


#permet de calcules le nouveau volume du circuit quand on change le volume des cellules
def after_cellules(vol_c1,vol_c2, vol_cellule_c1,vol_cellule_c2):
    
    new_c1=((vol_c1+vol_cellule_c1)/volume_total[j+1])
    new_c2=((vol_c2+vol_cellule_c2)/volume_total[j+1])
    
    return new_c1,new_c2

#permet d'ajouter les nouvelles valeur de concentration dans le dictionnaire de concentration réel (varable global :/)
def add_concentration (c1, c2):
    jour=len(concentration_reel["jour"])+1
    concentration_reel["jour"].append(jour)
    concentration_reel["c1"].append(c1)
    concentration_reel["c2"].append(c2)
    concentration_reel["nut"].append(1-c1-c2)





#appel fonction
concentration_impose = donnees("concentra.csv")

# déclaration variables
volume_depart=10-1.4 #ml
volume_min=5 #ml (prevoir prelevement ? )
volume_cellule=1.4 #ml (dans la partie cellules)

volume_total=[]
volume_total.append(volume_depart)

volume_purge=[]
volume_add_nut = []
volume_add_h1 = []
volume_add_h2 = []

#dictionnaire des concentration sur le circuit et ajoute la première concentration
concentration_reel = {"jour": [], "c1":[], "c2":[], "nut":[]}
add_concentration(concentration_impose["c1"][0], concentration_impose["c2"][0])    


for j in range(len(concentration_impose["nut"])-1):
    print(j)
    
    #si les nutiment diminue => pas besoin de purge
    if (concentration_impose["nut"][j+1]<=concentration_reel["nut"][j]):
        ajout_nut = 0
        ajout_h1 = ((-concentration_impose["nut"][j+1]*concentration_reel["c1"][j]*volume_total[j])+(concentration_reel["nut"][j]*concentration_impose["c1"][j+1]*volume_total[j])+(concentration_impose["c1"][j+1]*ajout_nut))/concentration_impose["nut"][j+1]
        ajout_h2 = -(((concentration_impose["c1"][j+1]-1)*((concentration_reel["nut"][j]*volume_total[j])+ajout_nut))/concentration_impose["nut"][j+1])+(concentration_reel["c1"][j]-1)*(volume_total[j]-ajout_nut)
        ajout_h1 = round(ajout_h1,2)
        ajout_h2 = round(ajout_h2,2)
        volume_total.append(volume_total[j]+ajout_nut+ajout_h1+ajout_h2)
        volume_purge.append(0)
        volume_add_nut.append(ajout_nut)
        volume_add_h1.append(ajout_h1)
        volume_add_h2.append(ajout_h2)
        print("Pas besoin de purge")
        print("Volume à ajouter (en ml) de h1 est", ajout_h1)
        print("Volume à ajouter (en ml) de h2 est", ajout_h2)
    
        
        
    #si les nutiment augmente =>  besoin de purge
    elif (concentration_impose["nut"][j+1]>concentration_reel["nut"][j]):
        volume_mtn_nut = concentration_reel["nut"][j]*volume_total[j]
        volume_mtn_h1 = concentration_reel["c1"][j]*volume_total[j]
        volume_mtn_h2 = concentration_reel["c2"][j]*volume_total[j]
        
        volume_apres_nut = concentration_impose["nut"][j+1]*volume_min
        volume_apres_h1 = concentration_impose["c1"][j+1]*volume_min
        volume_apres_h2 = concentration_impose["c2"][j+1]*volume_min
        
        volume_pour_purge=0
        
        volume_reste_purge_nut = volume_mtn_nut-(volume_pour_purge*concentration_reel["nut"][j])
        volume_reste_purge_h1 = volume_mtn_h1-(volume_pour_purge*concentration_reel["c1"][j])
        volume_reste_purge_h2 = volume_mtn_h2-(volume_pour_purge*concentration_reel["c2"][j])
        volume_tot_reste_purge = volume_total[j]-volume_pour_purge
        
        
        while (volume_reste_purge_nut>volume_apres_nut or volume_reste_purge_h1>volume_apres_h1 or volume_reste_purge_h2>volume_apres_h2):
            volume_pour_purge=volume_pour_purge+1
            volume_reste_purge_nut = volume_mtn_nut-(volume_pour_purge*concentration_reel["nut"][j])
            volume_reste_purge_h1 = volume_mtn_h1-(volume_pour_purge*concentration_reel["c1"][j])
            volume_reste_purge_h2 = volume_mtn_h2-(volume_pour_purge*concentration_reel["c2"][j])
            volume_tot_reste_purge = volume_total[j]-volume_pour_purge
        
        if (volume_tot_reste_purge<volume_min):
            volume_pour_purge=volume_total[j]-volume_min
            
        ajout_nut = round(volume_apres_nut-volume_reste_purge_nut,2)
        ajout_h1 = round(volume_apres_h1-volume_reste_purge_h1,2)
        ajout_h2 = round(volume_apres_h2-volume_reste_purge_h2,2)
        volume_pour_purge = round(volume_pour_purge,2)
        
        volume_purge.append(volume_pour_purge)
        volume_add_nut.append(ajout_nut)
        volume_add_h1.append(ajout_h1)
        volume_add_h2.append(ajout_h2)
        
        volume_total.append(volume_total[j])
            
        print("besoin de purge")
        print("Volume à purger (en ml) ", volume_pour_purge)
        print("Volume à ajouter (en ml) de h1 est", ajout_h1)
        print("Volume à ajouter (en ml) de h2 est", ajout_h2)
        print("Volume à ajouter (en ml) de nut est", ajout_nut)
        
        
    else :
        print("ERROR")
        
    #ouverture et remplissage cellules 
    #Donc nouveau volume : 
    vol_c1 = (volume_total[j+1]-volume_cellule)*concentration_impose["c1"][j+1]
    vol_c2 = (volume_total[j+1]-volume_cellule)*concentration_impose["c2"][j+1]
    vol_cellule_c1 = volume_cellule*concentration_impose["c1"][j]
    vol_cellule_c2 = volume_cellule*concentration_impose["c2"][j]
    c1, c2 = after_cellules(vol_c1, vol_c2, vol_cellule_c1, vol_cellule_c2)
    add_concentration(c1, c2)
            
            
print("le volume total de nutiment est en ml :",(sum(volume_add_nut)+volume_depart))
print("le volume total de h1 est en ml :",(sum(volume_add_h1)))
print("le volume total de h2 est en ml :",(sum(volume_add_h2)))
