import socket
import pyfiglet
import sys
from datetime import datetime

ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)


target = input("Enter valid IP Address: ")


print("_" * 50)
print(f"Scanning Target: {target}")
print("Scanning Target at:" + str(datetime.now()))
print("_" * 50)

try:

    # will scan ports between 1 to 65,535
    for port in range(1, 1049):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        # returns error indicator
        result = s.connect_ex((target, port))
        if result == 0:
            print(("Port {}, is open".format(port)))
        s.close()

except KeyboardInterrupt:
        print("\n Exitting Program !!!!")
        sys.exit()
except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
except socket.error:
        print("\ Server not responding !!!!")




# TGF1cmVsIFNjb3R0
