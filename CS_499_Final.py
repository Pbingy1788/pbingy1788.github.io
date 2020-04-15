#!/usr/bin/env python
#

from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan

import time
import grovepi
import json
import sys
import getpass

# connect the DHt sensor to port 7
dht_sensor_port = 7

# use 0 for the blue-colored sensor and 1 for the white-colored sensor
dht_sensor_type = 0

# Connect the Grove Button to digital port D4
# SIG,NC,VCC,GND
button = 4
grovepi.pinMode(button, "INPUT")

# Connect the LED to digital port D2,D3
# SIG,NC,VCC,GND
ledG = 2
ledB = 3
grovepi.pinMode(ledG, "OUTPUT")
grovepi.pinMode(ledB, "OUTPUT")

# Connect the Grove Buzzer to digital port D8
# SIG,NC,VCC,GND
buzzer = 8
grovepi.pinMode(buzzer, "OUTPUT")

# declare how to write to json file
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(dat_file, fp)


path = './'
fileName = 'CS_499_Final_Data_Output'

# Empty array list
dat_file = []


#  User information function
def readUserInfo():
    # prompt user to enter name
    name = raw_input("Enter username : ")

    # prompt user to enter password & quit program if incorrect
    password = raw_input("Enter password : ")

    if name == 'William' and password == 'admin1':
        print "\nWelcome " + name

    elif name == 'Breunna' and password == 'admin2':
        print "\nWelcome " + name

    else:
        print "\nIncorrect username and or password.\nPlease try again."
        quit()

    return name


# List admin data
def adminData():
    adminMessage = "\nAdmins: Please watch for temperature spikes that are above 95 degrees\nYou may also watch the LCD display screeen for the same results and color changes\n\nTemperature Gauge:\nGreen is temperature above 60 and below 85\nBlue is temperature above 85 and below 95\nRed is temperature above 95"

    # Specific Message for user William
    adminWilliam = ["Admins: Hello William, Please be sure to note any changes in temp manually"]

    # Specfic Message for user Breunna
    adminBreunna = ["Admins: Hello Breunna, Please be sure to note any changes in temp manually"]

    name = readUserInfo()
    if name == "William":
        print adminWilliam

    if name == "Breunna":
        print adminBreunna

    print adminMessage


adminData()


def readData():
    # While the button is not pressed logic
    while grovepi.digitalRead(button) == 0:
        try:

            # get the temperature and Humidity from the DHT sensor
            [temp, hum] = dht(dht_sensor_port, dht_sensor_type)
            if math.isnan(temp) or math.isnan(hum):
                continue
            # temperature conversion from Celsius to Fahrenheit
            temp = (temp * (9.0 / 5.0) + 32)

            # array list .appending temp and hum values
            dat_file.append([temp, hum])

            # write the dat_file array list to json
            writeToJSONFile(path, fileName, dat_file)

            # compute data readings every (5 seconds)
            time.sleep(5)

            # Display Temperature and Humidity Data to LCD screen
            setText_norefresh("Temp:" + str(temp) + "F\n" + "Humidity :" + str(hum) + "%")

            # If button is pressed stop the reading and exit program
            if grovepi.digitalRead(button) == 1:
                print "\nButton pressed: Sensor reading has stopped"

                # set RGB screen to purple
                setRGB(245, 66, 227)
                setText_norefresh("Data Stopped")
                sys.exit()

            # Send HIGH to switch on Green LED
            if temp > 60 and temp < 85 and hum < 80:
                grovepi.digitalWrite(ledG, 1)

                # set RGB screen to green
                setRGB(75, 245, 66)

            # Send HIGH to switch on Blue LED
            elif temp > 85 and temp < 95 and hum < 80:
                grovepi.digitalWrite(ledB, 1)

                # set RGB screen to blue
                setRGB(0, 255, 247)

            # Send HIGH to switch on Green and Blue LED
            elif hum > 80:
                grovepi.digitalWrite(ledG, 1)
                grovepi.digitalWrite(ledB, 1)

            # Send HIGH to switch on Buzzer for 1 second
            elif temp > 95:
                grovepi.digitalWrite(buzzer, 1)
                print('\nWarning: Temperature is at 95 degrees or higher')
                time.sleep(1)

                # Stop buzzing for 1 second and repeat
                grovepi.digitalWrite(buzzer, 0)
                time.sleep(1)

                # set RGB screen to red
                setRGB(245, 66, 66)

            else:
                # Send LOW to switch off LED & Buzzer
                grovepi.digitalWrite(buzzer, 0)

                grovepi.digitalWrite(ledG, 0)

                grovepi.digitalWrite(ledB, 0)

            # check if we have nans
            # if so, then raise a type error exception
            if isnan(temp) is True or isnan(hum) is True:
                raise TypeError('nan error')

            print "\ntemp =", temp, "F\thumidity =", hum, "%"

        except IOError:
            print("Error")


readData()
