# -*- coding: utf-8 -*-
import zaciski
import info

#%img sruby.png

text = info.info_wprowadzenie
showInfo = False #<<< Info
if showInfo:
    #! %(text)s
    None
#!--------------------------------------------

#! ###*Zestaw do połączenia zwykłego według PN-EN 15048*
text = info.info_zwykle
showInfo = False #<<< Info
if showInfo:
    #! %(text)s
    None

showZwykla = True #<<< Dobierz długość sruby w połaczeniu zwykłym
if showZwykla:
    #%img zwykle.png
    sizes = zaciski.znajdz_dostepne_srub_zwykle()
    asksize = sizes[0] #<<<< Wymiar sruby -
    teenumber = zaciski.znajdz_dostepne_ilosci_podkladek_zwykle()
    askteenumber = teenumber[0] #<<<< Ilosc podkladek [szt.] -
    zakres = zaciski.znajdz_zakres_zasisku_zwykle(asksize, askteenumber)
    askclipodim = 15   #<<<< Wymagany zacisk (w zakresie val_zakres) [mm] -
    out = zaciski.znajdz_dlugosc_sruby_zwyklej(asksize, askteenumber, askclipodim)
    #! ###Wynik dla val_asksize i val_askteenumber podkladek  - val_out

#!--------------------------------------------

#! ###*Zestaw do połączenia spęzanego*
text = info.info_sprezone
showInfo = False #<<< Info
if showInfo:
    #! %(text)s
    None

showSprezona = False #<<< Dobierz długość sruby w połaczeniu sprężonym
if showSprezona:
    #%img sprezone.png
    sizes = zaciski.znajdz_dostepne_srub_sprezone()
    asksize = sizes[0] #<<<< Wymiar sruby
    teenumber = zaciski.znajdz_dostepne_ilosci_podkladek_sprezone()
    askteenumber = teenumber[0] #<<<< Ilosc podkladek
    zakres = zaciski.znajdz_zakres_zasisku_sprezone(asksize, askteenumber)
    askclipodim = 15   #<<<< Wymagany zacisk (w zakresie val_zakres) [mm] -
    out = zaciski.znajdz_dlugosc_sruby_sprezonej(asksize, askteenumber, askclipodim)
    #! ###Wynik dla val_asksize i val_askteenumber podkladek  - val_out

#!--------------------------------------------

#! ###Powłkoki ochronne
text = info.info_powloki
showInfo = False #<<< Info
if showInfo:
    #! %(text)s
    None


'''
SeeName : Zaciski
SeeCategory : Steel

SeeDescription : Dobiera zacisk
'''