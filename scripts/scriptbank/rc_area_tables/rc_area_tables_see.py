import strupy.units as u
from strupy.concrete.rcsteel_area import area_diameter, area_diameter_quantity, area_diameter_spaceing_perdist

print(area_diameter)
from tabulate import tabulate

#! ##Tabele powierzchni zbrojenia

#%img rcbars.png

default_diameterlist=[4.5*u.mm,6*u.mm, 10*u.mm, 12*u.mm, 14*u.mm, 16*u.mm, 18*u.mm, 20*u.mm, 25*u.mm, 32*u.mm]
default_quantitylist=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
default_spaceinglist=[50*u.mm, 75*u.mm, 100*u.mm, 125*u.mm, 150*u.mm, 175*u.mm, 200*u.mm, 250*u.mm, 300*u.mm, 350*u.mm, 400*u.mm]


req_area = 0.01*u.cm**2
offset = float('+inf')

use_filter = False #<<< - użyj filtrów dla wymaganej powierzchni
if use_filter:
	req_area = 15*u.cm**2 #<<< - wymagane minimalne zbrojenie
	offset = 25 #<<< - dopuszczalna nadwyżka [procent]

#! -----------
show_per_number = False #<<< - powierzchnia dla ilości prętów
if show_per_number:
	headers = ['fi\nn'] + default_diameterlist
	table = []
	for number in default_quantitylist:
		data = [number]
		for d in default_diameterlist:
			area = area_diameter_quantity(d, number)
			if (100+offset)/100*req_area >= area >= req_area:
				data.append(area)
			else:
				data.append('-')
		table.append(data)
	tabulate_tab = tabulate(table, headers, tablefmt="fancy_grid") #%tab
#! -----------
show_per_spacing = False #<<< - powierzchnia dla rozstawu prętów na [mb]
if show_per_spacing:
	headers = ['fi\ns'] + default_diameterlist
	table = []
	for space in default_spaceinglist:
		data = [space]
		for d in default_diameterlist:
			area = area_diameter_spaceing_perdist(diameter=d, perdist=100.0*u.cm, spaceing=space)
			if (100+offset)/100*req_area >= area >= req_area:
				data.append(area)
			else:
				data.append('-')
		table.append(data)
	tabulate_tab = tabulate(table, headers, tablefmt="fancy_grid") #%tab
#! -----------

'''
SeeID : 88949230
SeeField : Structure
SeeName : Tabele zbrojenia
SeeCategory : Concrete
SeeDescription : Interaktywne tablice powierzchni zbrojenia.
'''