import requests as req
import json
from pprint import pprint
from datetime import datetime
from time import sleep
import os

url="http://127.0.0.1:5000/"
current_hour= int(datetime.now().strftime("%H"))
simulated_hour=json.loads(req.get(url+"info").text)["sim_time_hour"]

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def connecting_battery():
    for _ in range(5):
        print("Connecting battery.")
        sleep(.5)
        clear()
        print("Connecting battery..")
        sleep(.5)
        clear()
        print("Connecting battery...")
        sleep(0.5)
        clear()

def simulate_charging(building_consumtion, total_energy_consumption, when_price_is, percent=None):
    flag=False
    
    connecting_battery()
    
    print("Battery connected")
    print("")
    sleep(1)
    print("Charging battery")
    
    charge = json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"on"})).text)
    while flag is not True:
        if float(json.loads(req.get(url+"charge").text)) == 111.9:
            flag=True
        print(json.loads(req.get(url+"charge").text),"%")
        sleep(1)
    sleep(2)
    clear()
    print("Battery fully charged\n")
    sleep(1)
    charging_off = json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"off"})).text)
    print("Charging has been turned", charging_off["charging"])
    print("Battery is at:", json.loads(req.get(url+"charge").text),"%")

def set_battery_status():
# hushållets förbrukning är som lägst och 
# /baseload
# json.loads(req.get(url+"baseload").text)
# total energiförbrukning skall understiga 11kW (3 fas , 16 A)
# /info
    lowest_consumption_point=min(json.loads(req.get(url+"baseload").text))
    current_load=json.loads(req.get(url+"info").text)["base_current_load"]
    percent=float(json.loads(req.get(url+"charge").text))
    if percent > 79.90 and percent <= 80.00:
        json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"off"})).text)
        print("Battery percentage:", json.loads(req.get(url+"charge").text),"%")
        return True
    if current_load > 10.9 and json.loads(req.get(url+"baseload").text)[simulated_hour] != lowest_consumption_point:
        json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"off"})).text)
    else:
        json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"on"})).text)
        print("Baseload according to simulated hour:", json.loads(req.get(url+"baseload").text)[simulated_hour])
        print("base_current_load:",json.loads(req.get(url+"info").text)["base_current_load"])

def main():
# 1. Hämta prisinformation elområde 3 Stockholm.
    res = json.loads(req.get(url+"priceperhour").text)
    msg="Current price: " + str(res[current_hour])+" öre/kWh"
    print("="*len(msg))
    print(msg)
    print("="*len(msg))
    sleep(1)

# 2. Hämta information om hushållets energiförbrukning under ett dygn
    res = json.loads(req.get(url+"baseload").text)
    msg="Daily consumtion: "+ str(sum(res))+"kWh"
    print("="*len(msg))
    print(msg)
    print("="*len(msg))
    sleep(5)
    clear()

# 3. Skicka kommando för att starta och stoppa laddningen av EVs batteri.
# under laddning skall batteriets laddning avläsas och omvandlas till antal procent.
    
    flag=False
    
    connecting_battery()
    
    print("Battery connected")
    print("")
    sleep(1)
    print("Charging battery")
    
    req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"on"}))
    while flag is not True:
        if float(json.loads(req.get(url+"charge").text)) > 99.90 and float(json.loads(req.get(url+"charge").text)) <= 100.00:
            req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"off"}))
            print("Battery percentage:", json.loads(req.get(url+"charge").text),"%")
            flag=True
        print(json.loads(req.get(url+"charge").text),"%")
        sleep(1)
    sleep(5)
    clear()
    print("Battery fully charged\n")
    sleep(1)
    req.post(url+"discharge", headers={"Content-Type":"application/json"}, data=json.dumps({"discharging":"on"}))
    print("Charging has been turned off and discharged")

    
# 4. Batteriet skall laddas från 20% till 80%
# Deluppgift 1. Batteriet skall laddas när hushållets förbrukning är som lägst och total energiförbrukning
# skall understiga 11kW (3 fas , 16 A)

    flag=False
    
    connecting_battery()
    
    print("Battery connected")
    print("")
    sleep(1)
    print("Charging battery")
    
    while flag is not True:
        if set_battery_status():
            flag=True
        print(json.loads(req.get(url+"charge").text),"%")
        sleep(1)
    sleep(5)
    clear()
    print("Battery fully charged\n")
    sleep(1)
    req.post(url+"discharge", headers={"Content-Type":"application/json"}, data=json.dumps({"discharging":"on"}))
    print("Charging has been turned off and discharged")

# 5. Deluppgift 2. Batteriet skall laddas när elpriset är som lägst och total energiförbrukning för inte
# överstiga 11 kW (3 fas, 16A)
    flag=False
    current_load=json.loads(req.get(url+"info").text)["base_current_load"]
    
    connecting_battery()
    
    print("Battery connected")
    print("")
    sleep(1)
    print("Charging battery")
    
    while flag is not True:
        if float(json.loads(req.get(url+"charge").text)) > 99.90 and float(json.loads(req.get(url+"charge").text)) <= 100.00:
            json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"off"})).text)
            print("Battery percentage:", json.loads(req.get(url+"charge").text),"%")
            flag=True
        if json.loads(req.get(url+"priceperhour").text)[simulated_hour] != min(json.loads(req.get(url+"priceperhour").text)) and current_load > 10.9:
            json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"off"})).text)
        else:
            json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"on"})).text)
        
        print(json.loads(req.get(url+"charge").text),"%")
        sleep(1)
    sleep(5)
    clear()
    print("Battery fully charged\n")
    sleep(1)
    req.post(url+"discharge", headers={"Content-Type":"application/json"}, data=json.dumps({"discharging":"on"}))
    print("Charging has been turned off and discharged")


# 6. Klienten skall visa tidpunkter på dygnet och den totala energiåtgången samt visa på vilket sätt
# laddningen är optimerad.
    flag=False
    current_load=json.loads(req.get(url+"info").text)["base_current_load"]
    lowest_consumption_point=min(json.loads(req.get(url+"baseload").text))
    sim_min=str(json.loads(req.get(url+"info").text)["sim_time_min"])
    sim_hour=str(simulated_hour)

    connecting_battery()
    
    print("Battery connected")
    print("")
    sleep(1)
    print("Charging battery")
    print("")
    print("Charging at lowest price and lowest residential load")
    
    while flag is not True:
        if float(json.loads(req.get(url+"charge").text)) > 99.90 and \
            float(json.loads(req.get(url+"charge").text)) <= 100.00:
                json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"off"})).text)
                print("Battery percentage:", json.loads(req.get(url+"charge").text),"%")
                flag=True
        elif current_load > 10.9 and \
            json.loads(req.get(url+"baseload").text)[simulated_hour] != lowest_consumption_point and \
            json.loads(req.get(url+"priceperhour").text)[simulated_hour] != min(json.loads(req.get(url+"priceperhour").text)):
                json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"off"})).text)
        else:
            json.loads(req.post(url=url+"charge", headers={"Content-Type":"application/json"}, data=json.dumps({"charging":"on"})).text)
            print("Current time:", sim_hour+":"+sim_min)
            print("Current load:",current_load)
            print("Consumption point:", json.loads(req.get(url+"baseload").text)[simulated_hour])
            print("Current price:", json.loads(req.get(url+"priceperhour").text)[simulated_hour])
            print(json.loads(req.get(url+"charge").text),"%")
        
        sleep(1)
    sleep(5)
    clear()
    print("Battery fully charged\n")
    sleep(1)
    req.post(url+"discharge", headers={"Content-Type":"application/json"}, data=json.dumps({"discharging":"on"}))
    print("Charging has been turned off and discharged")

if __name__ == "__main__":
    main()