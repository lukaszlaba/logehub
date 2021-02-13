# -*- coding: utf-8 -*-
import math

from strupy import units as u
from strupy.steel.SectionBase import SectionBase
from strupy.steel.MaterialSteel import MaterialSteel
import strupy.steel.database_sections.sectiontypes as sectiontypes

base = SectionBase()
steel = MaterialSteel()


#! ##Obliczenie rozstawu steżeń dla belki zginanaj przy użyciu uproszczonej oceny wg pkt 6.6.2.4 PN-EN 1993-1-1 

#! Elementy, w których pas ściskany jest stężony punktowo w kierunku bocznym, nie są narażone na zwichrzenie, jeśli rozstaw pomiędzy stężeniami Lc i wynikająca z niego smukłość zastępczego pasa ściskanego spełnia warunek 6.6.2.4 jak ponizej.

#%img warunek.png

show = False #<<< Rysunek poglądowy
if show:
	#%img beam.png

#--------------------------------------------------------------------
#!###1. Dane wejściowe

#--------------------------------------------------------------------
#!####1.1. Przekrój belki
types = []
for i in base.get_database_sectiontypes():
    if i in sectiontypes.figuregrouplist[10]:
        types.append(i)
family = types[6] #<<<<Rodzina profilu dwuteowego-
names = base.get_database_sectionlistwithtype(family)
name = names[8] #<<<<Profil przekroj-

h = base.get_sectionparameters(name)['h']
b = base.get_sectionparameters(name)['b']
t_w = base.get_sectionparameters(name)['ea']
t_f = base.get_sectionparameters(name)['es']
r = base.get_sectionparameters(name)['ra']

show = False #<<< Geometria przekroju
if show:
    #%img profil.png
    h #! - wysokość przekroju
    b #! - szerokość przekroju
    t_w #! - grubość środnika
    t_f #! - grubość stopki
    r #! - promień wyokrąglenia

A = base.get_sectionparameters(name)['Ax']
I_y = base.get_sectionparameters(name)['Iy']
I_z = base.get_sectionparameters(name)['Iz']
I_t = base.get_sectionparameters(name)['Ix']
I_w = base.get_sectionparameters(name)['Iomega']
W_ely = base.get_sectionparameters(name)['Wy']
W_ply = base.get_sectionparameters(name)['Wply']

show = False #<<< Parametry przekroju
if show:
    A #! - pole przekroju poprzecznego
    I_y #! - moment bezwładności przekroju wzgl. osi y
    I_z #! - moment bezwładności przekroju wzgl. osi z
    I_t #! - moment bezwładności przy skręcaniu
    I_w #! - wycinkowy moment bezwładności
    W_ely #! - sprężysty wskażnik wytrzymałości
    W_ply #! - wskażnik oporu plastycznego

#--------------------------------------------------------------------
#!####1.2 . Materiał
materials = steel.get_availablesteelgrade()
material = materials[2] #<<<<Gatunek stali-
steel.set_steelgrade(material)
E = steel.E
G = steel.G
f_u = steel.f_u(max(t_w, t_f))
f_y = steel.f_y(max(t_w, t_f))

show = False #<<< Parametry materiału
if show:
    E #! - moduł sprężystości
    G #! - moduł spręzystości przy ścinaniu
    f_u #! - wytrzymalość na rozciąganie
    f_y #! - granica plastyczności

#--------------------------------------------------------------------
#!###2. Obliczenia

#--------------------------------------------------------------------
#!####2.1 . Klasyfikacja przekroju
def findclass (value = 20, maxclassvalues=[20, 40, 50]):
    classlist = [1, 2, 3, 4]
    if (value <= maxclassvalues[0]):
        return classlist[0]
    if (maxclassvalues[0] < value <= maxclassvalues[1]):
        return classlist[1]
    if (maxclassvalues[1] < value <= maxclassvalues[2]):
        return classlist[2]
    if (maxclassvalues[2] < value):
        return classlist[3]

ε  = (235.0*u.MPa/f_y )**0.5 #%requ

#! Klasa pasa:
c = (b - t_w - 2*r) / 2 #%requ
c / t_f #%requ
[9*ε, 10*ε, 14*ε] #%requ - graniczne smukłość dla  klas 1,2,3,4
flange_class = findclass(c/t_f, [9*ε, 10*ε, 14*ε])
#! >>*Klasa pasa - val_flange_class* 

#! Klasa środnika:
c = h - 2*t_f - 2.0 * r #%requ
c / t_w #%requ
[72*ε, 83*ε, 124*ε] #%requ - graniczne smukłości dla  klas 1,2,3,4
web_class = findclass(c/t_w, [72*ε, 83*ε, 124*ε])
#! >>*Klasa środnika - val_web_class*
section_class = max(flange_class, web_class)

#!*Klasa przekroju dwuteowego przy zginaniu  - val_section_class*

#--------------------------------------------------------------------
#!####2.2 . Nośność przekroju klasy val_section_class przy zginaniu
if section_class in [1, 2]:
	γ_M0 = 1.0 #!
	M_plRd = (W_ply * f_y / γ_M0).asUnit(u.kNm) #%requ
	M_cRd = M_plRd #%requ - obliczeniowa nosność przekroju na zginanie

if section_class in [3]:
	γ_M0 = 1.0 #!
	M_elRd = (W_ely * f_y / γ_M0).asUnit(u.kNm) #%requ
	M_cRd = M_elRd #%requ - obliczeniowa nosność przekroju na zginanie

if section_class in [4]:
	#%img ico_warning.png
	#! >>>!!!! uwaga przekrój klasy 4 - wyniki szacunkowe !!!!
	γ_M0 = 1.0 #!
	W_eff = 0.5 * W_ely #%requ - szacunkowe założenie (!!!!!!)
	M_elRd = (0.5 * W_ely * f_y / γ_M0).asUnit(u.kNm) #%requ
	M_cRd = M_elRd #%requ - obliczeniowa nosność przekroju przy zginaniu dla klasy val_section_class

#--------------------------------------------------------------------
#! ####2.3 Parametry zwichrzeniowe
k_c = 1.0 #<< - współczynnik poprawkowym uwzględniającym rozkład momentu zginającego pomiędzy stęzeniami, PN-EN 1993-1-1 Tablica 6.6
show = False #<<< Tablica 6.6
if show:
    #%img kc.png
λ_LT0 = 0.4 #! - dla kształtowników walcowanych
λ_c0 =  λ_LT0 + 0.1 #%requ - smukłość graniczna pasa
λ_1 = 93.9 * ε #%requ
I_fz = t_f*b**3 / 12 + (h - t_f)/3 * t_w**3 / 12 #%requ
A_fz = t_f*b + (h - t_f)/3 * t_w #%requ
i_fz = (I_fz / A_fz)**0.5 #%requ - promienień bezwładności przekroju pasa zastępczego, składającego się z pasa ściskanego i 1/3 ściskanej części środnika, względem osi y-y

#--------------------------------------------------------------------
#!####2.4 . Obliczenie rozstawu stezeń

option_list=[	'sprawdzenie_rozstawu_dla_zadanego_momentu',
			 	'wyznaczenie_wymaganego_rozstawu_dla_zadanego_momentu',
				'wyznaczenie_wymaganego_rozstawu_dla_zadanego_wytężenia']
option = option_list[0] #<<<< Opcja obliczeń -  

#--- OPTION 0
if option == option_list[0]:
	M_yEd = 150*u.kNm #<< - masymalny moment pomiędzy stężeniami
	L_c = 1*u.m #<< - rozstaw pomiędzy stężeniami
	if M_yEd > M_cRd:
		#%img ico_failed.png
		#! !!!!Podany moment jest większy niż nośność przekroju var_M_cRd - zmniejsz wartość momentu lub zwiększ profil!!!
	else:
		λ_f = k_c*L_c/(i_fz*λ_1) #%requ
		λ_c0*M_cRd/M_yEd #%requ
		if λ_f < λ_c0*M_cRd/M_yEd:
			(λ_f < λ_c0*M_cRd/M_yEd) #%requ - warunek 6.6.2.4
			#%img ico_pass.png
			#! Warunek 6.6.2.4 PN-EN 1993-1-1 jest spełniony
			#! Dla profilu val_name / val_material i momentu var_M_yEd rozstaw steżeń var_L_c jest wystarczający.
		else:
			(λ_f < λ_c0*M_cRd/M_yEd) #%requ - warunek 6.6.2.4
			#%img ico_failed.png
			#! !!! Warunek 6.6.2.4 PN-EN 1993-1-1 nie spełniony !!!
			#! !!! Dla profilu val_name / val_material i momentu var_M_yEd rozstaw steżeń var_L_c nie jest zbyt duży !!!

#--- OPTION 1
if option == option_list[1]:
	M_yEd = 150*u.kNm #<< - maksymalny moment pomiędzy stężeniami
	if M_yEd > M_cRd:
		#%img ico_failed.png
		#! !!!!Podany moment jest większy niż nośność przekroju var_M_cRd - zmniejsz wartość momentu lub zwiększ profil!!!
	else:
		L_crequ = (λ_c0*M_cRd/M_yEd * (i_fz*λ_1)).asUnit(u.m) / k_c #%requ - przekształcony warunek 6.6.2.4
		#! Dla profilu val_name / val_material i momentu var_M_yEd rozstaw steżeń powienien być nie wiekszy niż var_L_crequ .

#--- OPTION 2
if option == option_list[2]:
	utl_list = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
	utl = utl_list[4] #<< - przewidywany masymalny poziom wytężenia przekroju na zginanie
	L_crequ = (λ_c0*(1/utl) * (i_fz*λ_1) / k_c).asUnit(u.m) #%requ - przekształcony warunek 6.6.2.4
	#! Dla profilu val_name / val_material i wytężenia val_utl rozstaw steżeń powienien być nie wiekszy niż var_L_crequ .


'''
SeeID : 200094
SeeField : Structure
SeeCategory : Steel 
SeeName : Rozstaw stężeń dla belki wg EC
SeeDescription : Obliczenie rozstawu steżeń dla belki zginanaj przy uzyciu uproszczonej oceny wg pkt. 6.6.2.4 PN-EN 1993-1-1
'''