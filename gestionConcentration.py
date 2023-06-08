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


concentration_c1_mtn = 0.05 # c'est la concentration actuel sur le circuit 
concentration_c2_mtn = 0.1
concentration_c1_apres = 0.05 #c'est la nouvelle concentration que l'on veut
concentration_c2_apres = 0.0
volume_circuit = 39.3 # le volume en ml sur le circuit avec le volume de la cellule


def purge(concentration_c1_mtn,concentration_c2_mtn, concentration_c1_apres, concentration_c2_apres, volume_circuit ):
    concentration_nut_mtn=1-concentration_c1_mtn-concentration_c2_mtn
    concentration_nut_apres=1-concentration_c1_apres-concentration_c2_apres
    volume_min = 3 # le volume mini a avoir sur le circuit
    purge=False
    volume_purge=0.0
    if (concentration_nut_apres <=concentration_nut_mtn):
       purge=False
       volume_purge=0.0 
    elif (concentration_nut_apres > concentration_nut_mtn):
        volume_mtn_nut = concentration_nut_mtn*volume_circuit
        volume_mtn_c1 = concentration_c1_mtn*volume_circuit
        volume_mtn_c2 = concentration_c2_mtn*volume_circuit
        
        volume_apres_nut = concentration_c1_apres*volume_min
        volume_apres_c1 = concentration_c2_apres*volume_min
        volume_apres_c2 = concentration_nut_apres*volume_min
        
        volume_pour_purge=0
        
        volume_reste_purge_nut = volume_mtn_nut-(volume_pour_purge*concentration_nut_mtn)
        volume_reste_purge_c1 = volume_mtn_c1-(volume_pour_purge*concentration_c1_mtn)
        volume_reste_purge_c2 = volume_mtn_c2-(volume_pour_purge*concentration_c2_mtn)
        volume_tot_reste_purge = volume_circuit-volume_pour_purge
        
        
        while (volume_reste_purge_nut>volume_apres_nut or volume_reste_purge_c1>volume_apres_c1 or volume_reste_purge_c2>volume_apres_c2):
            
            volume_reste_purge_nut = volume_mtn_nut-(volume_pour_purge*concentration_nut_mtn)
            volume_reste_purge_c1 = volume_mtn_c1-(volume_pour_purge*concentration_c1_mtn)
            volume_reste_purge_c2 = volume_mtn_c2-(volume_pour_purge*concentration_c2_mtn)
            volume_tot_reste_purge = volume_circuit-volume_pour_purge
            volume_pour_purge=volume_pour_purge+1
            
        
        if (volume_tot_reste_purge<volume_min):
            volume_pour_purge=volume_circuit-volume_min
            print("aiii")
        
        purge=True
        volume_purge=volume_pour_purge
            
    return purge, volume_purge

def ajout(concentration_c1_mtn,concentration_c2_mtn, concentration_c1_apres, concentration_c2_apres, volume_circuit, volume_purge):
    concentration_nut_mtn=1-concentration_c1_mtn-concentration_c2_mtn
    concentration_nut_apres=1-concentration_c1_apres-concentration_c2_apres
    volume=3
    volume_max=50
    add=[]
    if (volume_purge==0):
        add_nut=0
        add_c1 = ((-concentration_nut_apres*concentration_c1_mtn*volume_circuit)+(concentration_nut_mtn*concentration_c1_apres*volume_circuit)+(concentration_c1_apres*add_nut))/concentration_nut_apres
        add_c2 = -(((concentration_c1_apres-1)*((concentration_nut_mtn*volume_circuit)+add_nut))/concentration_nut_apres)+(concentration_c1_mtn-1)*(volume_circuit-add_nut)
    elif (volume_purge!=0):
        volume_mtn_nut = concentration_nut_mtn*volume_circuit
        volume_mtn_c1 = concentration_c1_mtn*volume_circuit
        volume_mtn_c2 = concentration_c2_mtn*volume_circuit
        
        volume_apres_nut = concentration_nut_apres*volume
        volume_apres_c1 = concentration_c1_apres*volume
        volume_apres_c2 = concentration_c2_apres*volume
        
        volume_pour_purge=volume_purge
        
        volume_reste_purge_nut = volume_mtn_nut-(volume_pour_purge*concentration_nut_mtn)
        volume_reste_purge_c1 = volume_mtn_c1-(volume_pour_purge*concentration_c1_mtn)
        volume_reste_purge_c2 = volume_mtn_c2-(volume_pour_purge*concentration_c2_mtn)
        
        
        add_nut = round(volume_apres_nut-volume_reste_purge_nut,2)
        add_c1 = round(volume_apres_c1-volume_reste_purge_c1,2)
        add_c2 = round(volume_apres_c2-volume_reste_purge_c2,2)
        volume_pour_purge = round(volume_pour_purge,2)
        
        #si une concentration arrive a 0 : purge le max et rajoute le max?
        if (volume_apres_nut==0 or volume_apres_c1==0 or volume_apres_c2==0):
            volume = volume_max
            volume_apres_nut = concentration_nut_apres*volume
            volume_apres_c1 = concentration_c1_apres*volume
            volume_apres_c2 = concentration_c2_apres*volume
            
            add_nut = round(volume_apres_nut-volume_reste_purge_nut,2)
            add_c1 = round(volume_apres_c1-volume_reste_purge_c1,2)
            add_c2 = round(volume_apres_c2-volume_reste_purge_c2,2)
        else : 
            while (add_nut<0 or add_c1<0 or add_c2<0):
                volume+=1
                volume_apres_nut = concentration_nut_apres*volume
                volume_apres_c1 = concentration_c1_apres*volume
                volume_apres_c2 = concentration_c2_apres*volume
                
                add_nut = round(volume_apres_nut-volume_reste_purge_nut,2)
                add_c1 = round(volume_apres_c1-volume_reste_purge_c1,2)
                add_c2 = round(volume_apres_c2-volume_reste_purge_c2,2)
            
            
        print("vol",volume)
        volume_pour_purge = round(volume_pour_purge,2)
    
    add=[add_nut,add_c1,add_c2]
    
    return add # nutriment, c1, c2

p,v = purge(concentration_c1_mtn, concentration_c2_mtn, concentration_c1_apres, concentration_c2_apres, volume_circuit)
print(p)
print(v)
tableau = ajout(concentration_c1_mtn, concentration_c2_mtn, concentration_c1_apres, concentration_c2_apres, volume_circuit, v)
print(tableau)
            
        
    
