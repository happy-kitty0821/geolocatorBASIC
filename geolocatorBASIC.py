# This script is licensed under the MIT License.

"""
This script demonstrates geolocation using the Geopy library.
It prompts the user to enter an IP address and retrieves the geolocation information for that IP address.
The geolocation information includes the address, latitude, longitude, and raw location details.
"""

import os
import ipaddress
from tabulate import tabulate
from geopy.geocoders import Nominatim
from datetime import datetime

# Check if the script is run as a superuser
if os.geteuid() != 0:
    print("You need to be a superuser to run this script.")
    exit()
    

print(r"""
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⢬⣧⠀⠙⣆⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⠛⠉⠀⠀⠀⠈⠀⠀⠙⠉⠉⠛⠳⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⣩⠀⠀⠀⠀⠀⠀⢿⣿⠛⣿⣶⣶⣤⣤⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡼⠋⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡆⠀⠀⠀⠀⠀⠈⣿⣇⠉⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⣾⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⢳⠀⠀⠀⠀⠀⡄⠘⢿⣆⢨⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣠⣾⠏⠀⠀⠀⡇⠀⠀⠀⠀⠀⢠⠀⠀⢹⡀⠀⠘⣧⠀⠀⠀⠀⢹⡀⠈⢻⣷⣜⠛⡿⠀⠀⠀⠀⠀⠀⠀
⠀⣴⣿⣿⣿⠏⠀⡀⠀⠀⣷⠀⠀⠀⠀⠀⢸⡄⠀⠈⣧⠀⠀⠘⣆⠀⠀⠀⠘⡇⠀⠀⠙⡿⣿⣷⡀⠀⠀⠀⠀⠀⠀
⠀⢻⣿⣿⡏⠀⠀⡇⠀⠀⢸⡄⠀⠀⠀⠀⠈⣷⣄⠀⠘⣷⡀⠀⠘⣆⠀⠀⠀⣧⠀⠀⠀⢧⠈⠻⣷⡀⠀⠀⠀⠀⠀
⠀⠈⣿⡿⠀⢰⠀⣧⠀⠀⢸⠻⣆⠀⠀⠀⠀⣷⠘⢦⡀⠘⣿⣤⡀⠹⣄⠀⠀⢹⠀⠀⠀⠘⣧⠀⠙⣷⡀⠀⠀⠀⠀
⠀⠀⢸⠇⠀⠸⢠⡿⣄⠀⢸⠀⠈⠛⠦⣤⣀⣹⣶⡶⠿⠲⠮⢯⣽⣦⣻⡀⠀⢸⠀⠀⠀⠀⢹⡆⠀⠸⣧⠀⠀⠀⠀
⠀⠀⣿⠀⠀⢀⣾⠁⠙⣦⣸⡦⠖⠉⠀⠀⠈⠉⠈⠃⠀⠀⠀⠀⠀⠀⠈⣯⠀⢸⠀⠀⠀⠀⠀⢻⠀⠀⢹⣇⠀⠀⠀
⠀⣸⡏⠀⠀⢸⠇⠀⠀⠈⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⡶⢲⣿⠀⢸⠀⠀⠀⠀⠀⠘⡇⠀⢸⢹⣆⠀⠀
⠀⣿⣇⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡯⠿⠛⠋⠉⠉⠁⠘⡄⢸⠀⠀⠀⠀⠀⠀⢷⠀⢸⢀⣿⡄⠀
⢀⡟⢸⠀⠀⢸⡇⠀⣀⡤⣶⣾⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⢀⢀⡀⣤⠀⡇⢸⠀⠀⠀⠀⠀⠀⢸⠀⢸⢸⠙⣇⠀
⢸⡇⠸⡄⠀⠘⣧⠼⠷⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠘⠋⠉⠉⠀⡇⣼⠀⠀⠀⠀⠀⠀⢸⠀⡼⣼⠀⢻⠀
⢸⡧⡀⣧⠀⠀⢿⠀⠀⢰⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠀⠀⠀⠀⠀⣧⡇⠀⠀⠀⠀⠀⠀⢸⠀⢣⠇⠀⢸⡄
⢸⡇⢧⠘⣆⠀⠸⣇⠀⠈⠀⠀⠀⣀⣀⣀⠤⠴⢒⣒⠽⠛⠁⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⡜⢠⡟⠀⠀⢸⡇
⢸⡇⠈⢧⠹⡄⠀⢻⡀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⣀⡴⠆⣿⠀⠀⠀⠀⠀⠀⠀⣧⡞⠀⠀⠀⢸⠇
⠈⣧⠀⠈⢷⡹⣄⠈⠷⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⠛⢉⡤⢾⠃⠀⠀⠀⠀⠀⠀⢸⠏⠀⠀⠀⠀⣼⠀
⠀⠹⣆⠀⢀⠳⡌⢢⡀⠀⠈⠉⣹⠙⠛⣚⠛⣟⡛⠻⣿⠟⢁⡤⠞⠉⠀⡟⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⣼⠃⠀
⠀⠀⢻⡄⢸⡄⠙⢦⡀⠀⠀⠀⢸⣆⠀⠈⠳⣄⡙⢲⣽⠞⠉⠀⠀⢀⣼⠃⠀⠀⠀⠀⢀⣤⠞⠃⠀⠀⣠⡾⠋⠀⠀
⠀⠀⠀⠹⣦⣿⣦⡀⠙⠳⢤⣀⡘⣿⠛⠶⢤⣤⣉⣟⠁⠀⠀⣠⣾⣿⡏⠀⠀⢀⣠⣶⣿⣧⠤⠤⠶⠛⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠈⢻⣦⡙⠳⠦⢤⣄⣁⣹⣆⠀⠀⠀⡼⣻⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀

      

""")


print("\n************************************************************************************************************")
print("\n* Copyright of Happy-kitty                                                                                 *")
print("\n* For educational purposes only                                                                            *")
print("\n* I will not be held responsible if you are caught using this script for malicious intents                 *")
print("\n* Do not track the location of others without their consent                                               *")
print("\n* github.com/happy-kitty0921                                                                               *")
print("\n************************************************************************************************************")

geolocator = Nominatim(user_agent="happy-kitty0821")

ip_input = input("Enter IP address: ")

try:
    ip = ipaddress.ip_address(ip_input)
    if ip.is_private:
        print("You have entered a private IP address. Please enter a public IP address.")
    else:
        # Get the location based on the IP address
        location = geolocator.geocode(ip_input)

        if location:
            table = [
                ["Address:", location.address],
                ["Latitude:", location.latitude],
                ["Longitude:", location.longitude],
                ["Raw Location:", location.raw]
            ]
            print("")
            print("Would you like to see the result in the terminal? (y/n)")
            print("")
            OUTPUT = input(">>>")
            if OUTPUT.lower() == "y":
                print(tabulate(table))
            elif OUTPUT.lower() == "n":
                # Save the report in a text file with the date and time
                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"geolocation_report_{timestamp}.txt"

                with open(filename, "w") as file:
                    for row in table:
                        file.write(row[0] + " " + str(row[1]) + "\n")

                print(f"Geolocation report saved in file: {filename}")
            else:
                print("Please enter a valid command (y/n).")
        else:
            print("Could not retrieve geolocation information.")
except ValueError:
    print("Invalid IP address format.")
