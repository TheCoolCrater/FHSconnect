from operator import truediv
import os 
from datetime import datetime


lap = 1
# resp = os.popen("ping -n 1 192.168.1.1")


while lap <= 5:
    TIME = datetime.now() #.strftime('%y-%m-%d %H_%M_%S')
    resp = os.popen("ping -n 100 192.168.1.1")
    with open(f"ping_report_{lap}.txt", "w") as file:
        file.write(f'Ping Time: {TIME}\n')
        for x in resp:
            file.write(f'Ping Response: {x}')

    lap += 1
