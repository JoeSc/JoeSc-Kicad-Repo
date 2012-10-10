#!/usr/bin/python
#import urllib
import sys
import re

if len(sys.argv) < 2:
	print "Usage " + sys.argv[0] + "[res|cap|led]"

def yesno():
	# raw_input returns the empty string for "enter"
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])
	
	choice = raw_input().lower()
	if choice in yes:
		return True
	elif choice in no:
		return False
	else:
		sys.stdout.write("Please respond with 'yes' or 'no'")
	

# Long_name Long_name Long_name PN Val Package Tol Voltage Package
Cap_String='#\n# %s\n#\nDEF ~%s C 0 10 N Y 1 F N\nF0 "C" 50 100 50 H V L CNN\nF1 "%s" 100 -200 50 H I L CNN\nF4 "%s" 500 -300 60 H I C CNN "PN"\nF5 "%s" -125 50 39 H V R BNN "Val"\nF6 "%s" -125 -100 39 H V R BNN "Package"\nF7 "%s" -125 0 39 H V R BNN "Tol"\nF8 "%s" -125 -50 39 H V R BNN "Voltage"\n$FPLIST\n SM%s\n$ENDFPLIST\nDRAW\nP 2 0 1 20  -100 -30  100 -30 N\nP 2 0 1 20  -100 30  100 30 N\nX ~ 1 0 200 170 D 40 40 1 1 P\nX ~ 2 0 -200 170 U 40 40 1 1 P\nENDDRAW\nENDDEF'

# Long_name Long_name Long_name PN Val Package Tol power Package
Res_String='#\n# %s\n#\nDEF ~%s R 0 0 N Y 1 F N\nF0 "R" 105 0 50 V V C CNN\nF1 "%s" -525 150 50 H I C CNN\nF4 "%s" -620 225 60 H I C CNN "PN"\nF5 "%s" -70 50 39 H V R BNN "Val"\nF6 "%s" -70 -100 39 H V R BNN "Package"\nF7 "%s" -70 0 39 H V R BNN "Tol"\nF8 "%s" -70 -50 39 H V R BNN "Power"\n$FPLIST\n SM%s\n$ENDFPLIST\nDRAW\nP 10 0 1 0  0 200  0 150  50 125  -50 75  50 25  -50 -25  50 -75  -50 -125  0 -150  0 -200 N\nX ~ 1 0 250 50 D 60 60 1 1 P\nX ~ 2 0 -250 50 U 60 60 1 1 P\nENDDRAW\nENDDEF'

# Long_name Long_name Long_name PN color package package
LED_String='#\n# %s\n#\nDEF ~%s D 0 40 Y N 1 F N\nF0 "D" 0 100 50 H V C CNN\nF1 "%s" 0 200 50 H I C CNN\nF4 "%s" -350 250 61 H I L BNN "PN"\nF5 "%s" -200 -150 39 H V L BNN "Val"\nF6 "%s" -200 -100 39 H V L BNN "Package"\n$FPLIST\n LED-%s\n$ENDFPLIST\nDRAW\nP 2 0 1 0  50 50  50 -50 N\nP 3 0 1 0  -50 50  50 0  -50 -50 F\nP 3 0 1 0  65 -40  110 -80  105 -55 N\nP 3 0 1 0  80 -25  125 -65  120 -40 N\nX A 1 -200 0 150 R 40 40 1 1 P\nX K 2 200 0 150 L 40 40 1 1 P\nENDDRAW\nENDDEF'


if 'cap' in sys.argv[1].lower():
	print "Inputting CAP"
	while True:
		digikey_pn = raw_input("Digi-key Part Number: ")
		value = raw_input("Capacitor value [0.1uF]: ")
		package = raw_input("Package Size [0805]: ")
		tolerance = raw_input("Tolerance [10%]:")
		temp_coef = raw_input("Temperature Coefficient [x7r]: ")
		voltage = raw_input("Voltage [50V]: ")
		print "Was the above entered correctly? (y/n)",
		if yesno():
			break
	value_p =value.replace('.','p')
	tolerance_p =tolerance.replace('%','p')
	longname = 'cap_%s_%s_%s_%s_%s'%(value_p.lower(), tolerance_p, voltage.lower(), temp_coef.lower(), package)
	new_sym = Cap_String%(longname,longname,longname,digikey_pn,value,package,tolerance,voltage.upper(), package)



elif 'res' in sys.argv[1].lower():
	print "Inputting RES"
	while True:
		digikey_pn = raw_input("Digi-key Part Number: ")
		value = raw_input("Resistance [4.7K]: ")
		package = raw_input("Package Size [0805]: ")
		tolerance = raw_input("Tolerance [1%]:")
		power = raw_input("Power [1/8W]: ")
		print "Was the above entered correctly? (y/n)",
		if yesno():
			break
	value_p =value.replace('.','p')
	tolerance_p =tolerance.replace('%','p')
	power_v=power.replace('/','v')
	longname = 'res_%s_%s_%s_%s'%(value_p.lower(), tolerance_p, power_v.lower(), package)
	new_sym = Res_String%(longname,longname,longname,digikey_pn,value,package,tolerance,power.upper(), package)

elif 'led' in sys.argv[1].lower():
	print "Inputting LED"
	while True:
		digikey_pn = raw_input("Digi-key Part Number: ")
		color = raw_input("Color [Green]: ")
		package = raw_input("Package Size [0805]: ")
		print "Was the above entered correctly? (y/n)",
		if yesno():
			break
	longname = 'led_%s_%s'%(color.lower(), package)
	new_sym = LED_String%(longname,longname,longname,digikey_pn,color.lower().capitalize(),package, package)



# put it in a lib define by argv[2]
f = open(sys.argv[2])
file_list = f.readlines()
f.close()
f = open(sys.argv[2]+".tmp", 'w')
for x in file_list:
	f.write(x)
f.close()

for i,x in enumerate(file_list):
	if 'DEF ' in x:
		cur_name = file_list[i-2].strip('# ').strip()
		if cmp(longname,cur_name) < 0:
			break

		if cmp(cur_name,longname) == 0:
			print "Error: Symbol already added to library!"
			exit()
# Here i should be set to 3 greater than the start of the symbol

new_sym = new_sym.split("\n")
new_sym.reverse()
for x in new_sym:
	file_list.insert(i-3, x+'\n')

f = open(sys.argv[2],'w')
for x in file_list:
	f.write(x)

