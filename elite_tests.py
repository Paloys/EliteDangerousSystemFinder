import requests
import json
import os
import pyperclip
import tkinter as tk
from tkinter import ttk

states = ["Investment", "Boom", "None", "Bust", "Famine", "Civil Liberty", "None", "Civil Unrest", "Lockdown", "Expansion", "Retreat", "Outbreak", "Elections", "Civil War", "War", "Exiled", "Infested", "Incursion", "Pirate Attack", "Blight", "Drought", "Infrastructure Failure", "Natural Disaster", "Public Holiday", "Terrorist Attack"]

def get_current_system():
    os.chdir(os.environ['USERPROFILE'] + r'\Saved Games\Frontier Developments\Elite Dangerous')
    all_logs = [x for x in os.listdir() if x.startswith("Journal.")]
    all_logs.sort(reverse=True)
    with open(all_logs[0]) as f:
        system = [json.loads(x)["StarSystem"] for x in f.readlines()[::-1] if json.loads(x)["event"] in ["FSDJump", "Location"]][0]
    return system

class System:
    def __init__(self, **entries):
        for k,v in entries.items():
            if isinstance(v,dict):
                self.__dict__[k] = System(**v)
            else:
                self.__dict__[k] = v
    def __str__(self):
        return self.name
    def __int__(self):
        return self.distance
    def __lt__(self, other):
        if isinstance(other, System):
            return self.distance < other.distance
        return False
    def __le__(self, other):
        if isinstance(other, System):
            return self.distance <= other.distance
        return False
    def __eq__(self, other):
        if isinstance(other, System):
            return self.distance == other.distance
        return False
    def __ne__(self, other):
        if isinstance(other, System):
            return self.distance != other.distance
        return False
    def __gt__(self, other):
        if isinstance(other, System):
            return self.distance > other.distance
        return False
    def __ge__(self, other):
        if isinstance(other, System):
            return self.distance >= other.distance
        return False

def start():
    Variable.set("Searching...")
    state = comboExample.get()
    try:
        system = get_current_system()
    except:
        system = input("Nom du système : ")
    headers = {"content-type": "application/json"}
    payload = {'systemName':system, 'showInformation' : 1, 'radius' : 75}
    print(payload)
    r=requests.get("https://www.edsm.net/api-v1/sphere-systems", headers=headers, params=payload)
    _list = [System(**dic) for dic in r.json()]
    if len(_list) == 0:
        print("Aucun système trouvé")
    _list.sort()
    for i in _list:
        try:
            if i.information.factionState == state:
                print(i)
                pyperclip.copy(i.__str__())
                Variable.set(str(i) + " : Distance : " + str(i.distance))
                return
        except AttributeError:
            pass
    Variable.set("No System Found.")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Elite Dangerous System Finder")

    Variable = tk.StringVar(root)
    Variable.set("Please select a state")

    root.geometry("300x100")
    frmMain = tk.Frame(root)

    labelTop = tk.Label(frmMain, text = "Choose a state")
    labelTop.grid(column=0, row=0)

    comboExample = ttk.Combobox(frmMain, values=states, state="readonly")
    comboExample.grid(column=0, row=1)
    comboExample.current(1)

    button = tk.Button(frmMain, text="Get a system", command=start)
    button.grid(column=0, row=2)

    labelBottom= tk.Label(frmMain, textvariable=Variable)
    labelBottom.grid(column=0, row = 3)

    frmMain.grid(row=0, column=0, sticky="NESW")
    frmMain.grid_columnconfigure(0, weight=1)
    frmMain.grid_rowconfigure(0, weight=1)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()
    #start()