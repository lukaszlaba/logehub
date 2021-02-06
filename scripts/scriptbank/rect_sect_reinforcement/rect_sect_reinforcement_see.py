# -*- coding: utf-8 -*-
from strupy.concrete.MaterialConcrete import MaterialConcrete
from strupy.concrete.MaterialRcsteel import MaterialRcsteel
from strupy.concrete.fas import calc as fas
from strupy import units as u

#! ##Kalkulator zbrojenia dla przekroju prostokątnego pod działaniem ściskania/rozciągania mimośrodwoego wg EC2

#%img rc_section.png

#! ####1. Geometria przekroju
b = 400*u.mm #<< - szerokość przekroju
h = 800*u.mm #<< - wysokość przekroju
ap = 5*u.cm #<< - odlegosc srodka zbrojenia p od powierzchni
an=5*u.cm #<< - odlegosc srodka zbrojenia p od powierzchni

#! ####2. Parametry zbrojenia
default_diameterlist=[4.5*u.mm,6*u.mm, 10*u.mm, 12*u.mm, 14*u.mm, 16*u.mm, 18*u.mm, 20*u.mm, 25*u.mm, 32*u.mm]
fip = default_diameterlist[5] #<< - srednica zbrojenia po stronie p
fin = default_diameterlist[7] #<< - srednica zbrojenia po stronie n

#! ####3. Ograniczenie zarysowania
wlimp=0.3*u.mm
wlimn=0.3*u.mm
wlim_list = [0.1*u.mm, 0.15*u.mm, 0.20*u.mm, 0.25*u.mm, 0.3*u.mm, 0.5*u.mm]
rysAp = False #<<< - kontrola zbrojenia po stronie p
if rysAp:
	rysAp = 1.0
	wlimp = wlim_list[4] #<< - dopuszczalna szerokosc rysy po stronie p
else:
	rysAp = 0.0

rysAn = False #<<< - kontrola zbrojenia po stronie n
if rysAn:
	rysAn = 1.0
	wlimn = wlim_list[4] #<< - dopuszczalna szerokosc rysy po stronie n
else:
	rysAn = 0.0

#! ####4. Materiały
#! Beton:
concrete = MaterialConcrete()
concrete_class_list = concrete.get_availableconcreteclass()
concrete_class = concrete_class_list[1] #<<< - klasa betonu
concrete.set_concreteclass(concrete_class)
fcd = concrete.fcd
fctm = concrete.fctm 
#! Wytrzynalosci betony var_fcd , var_fctm

#! Stal:
steel = MaterialRcsteel()
steel_class_list = steel.get_availablercsteelclass()
steel_class = steel_class_list[2] #<<< - klasa stali
steel.set_rcsteelclass(steel_class)
fyd = steel.fyd
#! Wytrzynalosci stali var_fyd

#! ####5. Obiążenie
Nsd = 0*u.kN #<< - moment
Msd = 120*u.kNm #<< - siła



#! ####6. Potrzebne zbrojenie
results = fas(Nsd, Msd, h, b, ap, an, fip, fin, rysAp, rysAn, wlimp, wlimn, fcd, fctm, fyd)
Ap = results['Ap'].asUnit(u.cm2) #! - zbrojenie po stronie p
An = results['An'].asUnit(u.cm2) #! - zbrojenie po stronie n

'''
SeeID : 58664383
SeeField : Structure
SeeName : Zbrojenie EC
SeeCategory : Concrete
SeeDescription : Zbrojenie przekroju prostokatnego
'''