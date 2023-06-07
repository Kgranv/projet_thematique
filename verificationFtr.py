import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

path = ".\\Data\\"
print("Quelle fichier voulez vous vérifier ?")
file = input()
try:
    test = pd.read_feather(path+file)
    time = test["Time"]
    conc1 = test["Conc1"]
    conc2 = test["Conc2"]

    plt.plot(time/(24*3600),conc1,label="Concentration 1")
    plt.plot(time/(24*3600),conc2, label="Concentration 2")
    plt.xlabel("Temps en jour")
    plt.ylabel("Concentration en %")
    plt.legend()
    plt.show()
except:
    print("Je n'ai pas compris")
# %%
