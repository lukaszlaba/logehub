# -*- coding: utf-8 -*-
import math

from strupy import units as u
from strupy.steel.SectionBase import SectionBase
from strupy.steel.MaterialSteel import MaterialSteel
import strupy.steel.database_sections.sectiontypes as sectiontypes

base = SectionBase()
steel = MaterialSteel()
#---------------------------------------------------------
#---------------------------------------------------------
#!###1 . Przekrój belki
types = []
for i in base.get_database_sectiontypes():
    if i in sectiontypes.figuregrouplist[10]:
        types.append(i)
family = types[6] #<<<<Rodzina profilu dwuteowego-
names = base.get_database_sectionlistwithtype(family)
name = names[11] #<<<<Profil przekroj-
#--------------------
h = base.get_sectionparameters(name)['h']
b = base.get_sectionparameters(name)['b']
t_w = base.get_sectionparameters(name)['ea']
t_f = base.get_sectionparameters(name)['es']
r = base.get_sectionparameters(name)['ra']
#------
show = False #<<< Geometria przekroju
if show:
    #%img profil.png

    h #! - wysokość przekroju
    b #! - szerokość przekroju
    t_w #! - grubość środnika
    t_f #! - grubość stopki
    r #! - promień wyokrąglenia
#--------------------
A = base.get_sectionparameters(name)['Ax']
I_y = base.get_sectionparameters(name)['Iy']
I_z = base.get_sectionparameters(name)['Iz']
I_t = base.get_sectionparameters(name)['Ix']
I_w = base.get_sectionparameters(name)['Iomega']
W_ely = base.get_sectionparameters(name)['Wy']
W_ply = base.get_sectionparameters(name)['Wply']
#------
show = True #<<< Parametry przekroju
if show:
    A #! - pole przekroju poprzecznego
    I_y #! - moment bezwładności przekroju wzgl. osi y
    I_z #! - moment bezwładności przekroju wzgl. osi z
    I_t #! - moment bezwładności przy skręcaniu
    I_w #! - wycinkowy moment bezwładności
    W_ely #! - sprężysty wskażnik wytrzymałości
    W_ply #! - wskażnik oporu plastycznego
#---------------------------------------------------------
#---------------------------------------------------------
#!###2 . Materiał
materials = steel.get_availablesteelgrade()
material = materials[0] #<<<<Gatunek stali-
steel.set_steelgrade(material)
E = steel.E
G = steel.G
f_u = steel.f_u(max(t_w, t_f))
f_y = steel.f_y(max(t_w, t_f))
#------
show = False #<<< Parametry materiału
if show:
    E #! - moduł sprężystości
    G #! - moduł spręzystości przy ścinaniu
    f_u #! - wytrzymalość na rozciąganie
    f_y #! - granica plastyczności
#---------------------------------------------------------
#---------------------------------------------------------
#!###3 . Geometria belki
L = 5.7 * u.m   #<< - rozpietość belki
#---------------------------------------------------------
#---------------------------------------------------------
#!###4 . Obciążenie belki
p_k = 15.81 * u.kN / u.m #<< - obciążenie charakterystyczne
#---------------------------------------------------------
#---------------------------------------------------------
#!###5 . Siły wewnętrzne
gamma_f = 1.5 #<< - wspólczynnik dla obciążęń
M_yEd = gamma_f * p_k * L**2 / 8.0 #%requ - obliczeniowy moment zginający w środku przęsła
V_zEd = gamma_f * 0.5 * p_k * L #%requ - najwieksza sił`a poprzeczna przy podporze
#---------------------------------------------------------
#---------------------------------------------------------
#!###6 . Klasyfikacja przekroju
ε = ((235.0*u.MPa)/(f_y) )**0.5 #%requ - ε
c = (b - t_w - 2*r) / 2 #%requ
c / t_f #%requ
((c / t_f) < 9*ε) #%requ
#!####Przekrój klasy 1
#---------------------------------------------------------
#---------------------------------------------------------
#!###7 . Nosność przekroju przy zginaniu
gamma_M0 = 1.0 #%requ
M_plRd = (W_ply * f_y / gamma_M0).asUnit(u.kNm) #%requ
M_cRd = M_plRd #%requ - obliczeniowa nosność przekroju przy zginaniu

M_yEd / M_cRd #%requ

if (M_yEd / M_cRd) < 1.0:
    None
    #! Warunek spełniony
else:
    None
    #! !!!!!Warunek nie spełniony!!!!!!
#---------------------------------------------------------
#---------------------------------------------------------
#!###8 . Współczynnik zwichrzenia
#--------------------
#! ####*8.1 Moment krytyczny przy zwichrzeniu*
k = 1 #! współczynnik ...
k_w = 1 #! współczynnik ...
C_1 = 1.127 #! - współczynnik zależny od rozkładu momenty zginającego
C_2 = 0.454 #! - współczynnik zależny od rozkładu momenty zginającego
z_g = h / 2 #%requ - odległość pomiędzy punktem przyłożenia obciążenia a środkiem ścinania
B = ( (k/k_w)**2*I_w/I_z + (k*L)**2*G*I_t/(math.pi**2*E*I_z) + (C_2*z_g)**2 )**0.5 #%requ - wartość pomocnicza
M_cr = ( C_1*(math.pi**2 * E * I_z)/(k * L)**2 * (B - C_2*z_g) ).asUnit(u.kNm) #%requ - wartość momentu krytycznego przy zwichrzeniu
#--------------------
#! ####*8.2 Smukłość względna*
λ_LT0 = 0.4 #!
λ_LT = max( (W_ply*f_y/M_cr)**0.5, λ_LT0 )  #%requ - smukłość względna
#--------------------
#! ####*8.3 Współczynnik zwichrzenia*
alpha_LT = 0.49 #! - parametr imprefekcji (dla duteownikó krzywa c)
beta = 0.75 #!
phi_LT = 0.5 * (1 + alpha_LT*(λ_LT-λ_LT0) + beta*λ_LT**2) #%requ
CHI_LT = 1.0 / (phi_LT + (phi_LT**2 - beta*λ_LT**2)**0.5) #%requ
CHI_LT = min(CHI_LT , 1.0, 1/CHI_LT**2)#%requ - wartość wpółczynnika
#--------------------
#!Korekta wartosci wspólczynika ze względu na rozkład momentów
k_c = 0.94 #!
f = min( 1.0 - 0.5 * (1-k_c) * (1.0-2*(CHI_LT-0.8)**2), 1.0) #%requ
CHI_LTmod = CHI_LT / f #%requ - finalna wartość współczynnika na zwichrzenie
#---------------------------------------------------------
#---------------------------------------------------------
#!###9 . Obliczeniowa nośnośc na zwichrzenie
gamma_M1 = 1.0 #!
M_bRd = ( CHI_LTmod * W_ply * f_y / gamma_M1 ).asUnit(u.kNm) #%requ
M_yEd / M_bRd #%requ

if (M_yEd / M_bRd) < 1.0:
    None
    #! Warunek spełniony
else:
    None
    #! !!!!!Warunek nie spełniony!!!!!!
#---------------------------------------------------------
#---------------------------------------------------------
#!###9 . Obliczeniowa nośnośc przy ścinaniu
#! W przypadku braku skręcania, nośność plastyczna przy ściananiu zależy od pola przekroju czynnego przy ścinaniu.
A_vz = A - 2*b*t_f + (t_w+2*r) * t_f #%requ
V_plzRd = ( A_vz * (f_y/3**0.5) / gamma_M0 ).asUnit(u.kN) #%requ - nośnośc plastyczna przy ścinaniu
V_zEd / V_plzRd #%requ

if (V_zEd / V_plzRd) < 1.0:
    None
    #! Warunek spełniony
else:
    None
    #! !!!!!Warunek nie spełniony!!!!!!
#--------------------
#!Sprawdzenie warunku stateczności środnika przy szaiłaniu siły poprzecznej nie jest wymagane gdy:
eta = 1.0
h_w = h - 2*t_f
(h_w/t_w < 72*ε/eta) #%requ
#---------------------------------------------------------
#---------------------------------------------------------
#!###10 . Sprawdzenie stanu granicznego ugięć (SGU)
w = ( 5 * p_k * L**4 / (384.0*E*I_y) ).asUnit(u.mm) #%requ
w_lim = (L / 250.0).asUnit(u.mm) #%requ

#!###11 . Podsunowanie

M_yEd

#!
'''
Belka z profilu val_name o rozpietości val_L obciążona var_p_k.

Moment obliczeniowy var_M_yEd / nośność na zwichrzeie var_M_bRd.

Siła poprzeczna  obliczeniowa var_V_zEd / nosność na ścinaie var_V_plzRd

Ugiecie var_w / dopuszcalne var_w_lim
'''


'''
SeeID : 999845
SeeField : Structure
SeeCategory : Steel
SeeName : Belka wg EC
SeeDescription : Obliczenia dwuteowej belki wolnopodpartej pod obciązeniem ciągłym.
'''
