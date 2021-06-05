# -*- coding: utf-8 -*-
from datetime import datetime 
import random 

name = "data{}.txt"
for x in range(1,5):
    fd = open(name.format(x),"w")
    for n in range(50):
        hour = datetime.now().strftime('%H:%M')
        temperature = str(random.randint(10,30))
        humidity = str(random.randint(0, 100))
        data = hour + " - " + temperature + " - " + humidity + "\n"
        fd.writelines(data)
    fd.close()
    
    