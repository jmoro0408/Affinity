#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 21:42:10 2020
@author: James
"""
#This cell sets up the program and plots the 100% curve

import matplotlib.pyplot as plt
import numpy as np
plt.style.use('classic')

print("Please enter filepath of your CSV and hit enter")
#fileD = r"/Users/James/Documents/GitHub/TutorialCodes/ExampleCurve.csv"
fileD = input()

csv_file = np.genfromtxt(fileD, delimiter=',', dtype=float,encoding='utf-8-sig') #Import from csv file. 
flow = csv_file[:,0].tolist() #grabs first column and imports as list
head= csv_file[:,1].tolist() #grabs 2nd column and imports as list

fig1 = plt.plot(flow,head, label = "100%") #plotting orignial curves
plt.legend(loc="upper right")
plt.title('Pump Curves for Various Speeds')
plt.xlabel("Flow")
plt.ylabel("Head")
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

#%% Affinity law cell
"""
q1 / q2 = (n1 / n2) (d1 / d2)
where
q = volume flow capacity (m3/s, gpm, cfm, ..)
n = wheel velocity - revolution per minute - (rpm)
d = wheel diameter (m, ft)

we are expressing speed as a percentage and solving for new flow 
based on 100% speed. Wheel diameter is constant 

q2 = q1 * (n2*0.01) where n2 is the inputted speed in percentage

dp1/dp2 = (n1/n2)2 
dp2 = dp1 * ((n2/10)**2)

"""
for n in range(50,100,10): #standard flow speeds
    n2 = n * 0.01 #required speed in percentage
    q2 = [n2*i for i in flow] #applying speed reduction to flow
    dp2 = [j/((1/n2)**2) for j in head] #applying speed reduction to head
    fig2 = plt.plot(q2, dp2, label = str(n) + "%") #plotting reduced curves curves
    plt.legend()
                    
print("Would you like to plot a specific speed? (y/n)") #ask user if they would like to plot a specific speed
ss= input()
if ss == "n":
    print ("")
else:
    print("Please enter the speed curve required (%)") #custom speed curve plotting - must be integer
    reqSpeedPercent = int(input())
    reqSpeed =reqSpeedPercent * 0.01
    q3 = [(reqSpeed)*i for i in flow]
    dp3 = [j/((1/(reqSpeed))**2) for j in head]
    fig3 = plt.plot(q3, dp3, label = str(reqSpeedPercent) + "%")
    plt.legend(loc="upper right")

#%% This cell find the specific speed reqd for an inputed  head and flow

coeff = np.polyfit(x=flow, y=head, deg=2) #this find the equation of the line - 2nd order polynomial
linefit = np.poly1d(coeff)

a0 = float(linefit.c[2:3]) # assigning poly coefficients to constants
a1 = float(linefit.c[1:2])
a2 = float(linefit.c[0:1])

print("Would you like to determine what speed relates to a specific flow and head? (y/n)")

hh = input()
if hh == "y":
    print("Input desired flow")
    qd = float(input())
    print("Input desired head")
    pd = float(input())
    
    nb = 100 # known speed (100%)
    nd = (nb*qd)*((-a1 + ((a1**2)+ (4*a0*((pd/(qd**2))-a2)))**0.5)/(2*a0))
    print("Your desired head and flow will occur at a pump speed of approximately %s percent" % str(int(nd)))
        
    reqSpeed1=nd * 0.01
    q4 = [(reqSpeed1)*i for i in flow]
    dp4 = [j/((1/(reqSpeed1))**2) for j in head]
    fig3 = plt.plot(q4, dp4, label = str(int(nd)) + "%")
    plt.legend(loc="upper right")
    print("Graph has been saved as curves.svg in the local directory")
else:
    print("Graph has been saved as curves.svg in the local directory")
    
plt.savefig('curves.svg') #saves plot to svg in directory
plt.show()

