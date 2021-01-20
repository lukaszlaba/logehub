from data_zwykle import zaciski_sruby_zwykle
from data_sprezone import zaciski_sruby_sprezone

def _znajdz_dostepne_sruby(dane = zaciski_sruby_zwykle):
    wynik = []
    for i in dane.keys():
        wynik.append(i[0])
    wynik = list(set(wynik))
    return wynik

def _znajdz_dostepne_ilosci_podkladek(dane = zaciski_sruby_zwykle):
    wynik = []
    for i in dane.keys():
        wynik.append(i[1])
    wynik = list(set(wynik))
    return wynik

def _znajdz_zakres_zasisku(wymiar_sruby='M12', ilosc_podkladek = 1, dane = zaciski_sruby_zwykle):
    wartosci = []
    try:
        dane[(wymiar_sruby, ilosc_podkladek)]
    except:
        return []
    for i in dane[(wymiar_sruby, ilosc_podkladek)].values():
        if not i == (0, 0):
            wartosci += i
    zacisk_maksymalny = max(wartosci)
    zacisk_minimalny = min(wartosci)
    return zacisk_minimalny, zacisk_maksymalny

def _znajdz_zacisk_sruby(wymiar_sruby='M12', dlugosc_sruby=40, ilosc_podkladek = 1, dane = zaciski_sruby_zwykle):
    try:
        return dane[(wymiar_sruby,ilosc_podkladek)][dlugosc_sruby]
    except:
        return []

def _znajdz_dlugosc_sruby(wymiar_sruby = 'M12', ilosc_podkladek = 1, wymagany_zacisk = 15, dane = zaciski_sruby_zwykle):
    wynik = []
    try:
        dane[(wymiar_sruby, ilosc_podkladek)]
    except:
        return []
    for i in dane[(wymiar_sruby, ilosc_podkladek)].keys():
        zacisk = dane[(wymiar_sruby, ilosc_podkladek)][i]
        if zacisk[0]<=wymagany_zacisk<=zacisk[1]:
            wynik.append(i)
    return wynik

def _znajdz_srube(wymiar_sruby = 'M12', ilosc_podkladek = 1, wymagany_zacisk = 15,  dane = zaciski_sruby_zwykle):
    dlugosci = znajdz_dlugosc_sruby_zwyklej(wymiar_sruby, ilosc_podkladek, wymagany_zacisk)
    wynik = []
    for i in dlugosci:
        wynik.append('%sx%s'%(wymiar_sruby, i))
    return wynik

#--------------------------------------------------------------------------------------

def znajdz_dostepne_srub_zwykle():
    return _znajdz_dostepne_sruby(dane = zaciski_sruby_zwykle)

def znajdz_dostepne_ilosci_podkladek_zwykle():
    return _znajdz_dostepne_ilosci_podkladek(zaciski_sruby_zwykle)

def znajdz_zakres_zasisku_zwykle(wymiar_sruby='M12', ilosc_podkladek = 1):
    return _znajdz_zakres_zasisku(wymiar_sruby, ilosc_podkladek, dane = zaciski_sruby_zwykle)
    
def znajdz_zacisk_sruby_zwyklej(wymiar_sruby='M12', dlugosc_sruby=40, ilosc_podkladek = 1):
    return _znajdz_zacisk_sruby(wymiar_sruby, dlugosc_sruby, ilosc_podkladek, dane = zaciski_sruby_zwykle)

def znajdz_dlugosc_sruby_zwyklej(wymiar_sruby = 'M12', ilosc_podkladek = 1, wymagany_zacisk = 15):
    return _znajdz_dlugosc_sruby(wymiar_sruby, ilosc_podkladek, wymagany_zacisk, dane = zaciski_sruby_zwykle)
    
def znajdz_srube_zwykla(wymiar_sruby = 'M12', ilosc_podkladek = 1, wymagany_zacisk = 15,  data = zaciski_sruby_zwykle):
    return _znajdz_srube(wymiar_sruby, ilosc_podkladek, wymagany_zacisk,  dane = zaciski_sruby_zwykle)
    
#--------------------------------------------------------------------------------------

def znajdz_dostepne_srub_sprezone():
    return _znajdz_dostepne_sruby(dane = zaciski_sruby_sprezone)

def znajdz_dostepne_ilosci_podkladek_sprezone():
    return _znajdz_dostepne_ilosci_podkladek(zaciski_sruby_sprezone)

def znajdz_zakres_zasisku_sprezone(wymiar_sruby='M12', ilosc_podkladek = 2):
    return _znajdz_zakres_zasisku(wymiar_sruby, ilosc_podkladek, dane = zaciski_sruby_sprezone)
    
def znajdz_zacisk_sruby_sprezone(wymiar_sruby='M12', dlugosc_sruby=40, ilosc_podkladek = 2):
    return _znajdz_zacisk_sruby(wymiar_sruby, dlugosc_sruby, ilosc_podkladek, dane = zaciski_sruby_sprezone)

def znajdz_dlugosc_sruby_sprezonej(wymiar_sruby = 'M12', ilosc_podkladek = 2, wymagany_zacisk = 15):
    return _znajdz_dlugosc_sruby(wymiar_sruby, ilosc_podkladek, wymagany_zacisk, dane = zaciski_sruby_sprezone)
    
def znajdz_srube_sprezona(wymiar_sruby = 'M12', ilosc_podkladek = 1, wymagany_zacisk = 15,  data = zaciski_sruby_zwykle):
    return _znajdz_srube(wymiar_sruby, ilosc_podkladek, wymagany_zacisk,  dane = zaciski_sruby_zwykle)


# Testowanie
if __name__ == '__main__':
    print ('++++++++++++sruby wykle+++++++++++++++++')
    print (znajdz_dostepne_srub_zwykle())
    print (znajdz_dostepne_ilosci_podkladek_zwykle())
    print (znajdz_zakres_zasisku_zwykle())
    print (znajdz_zacisk_sruby_zwyklej())
    print (znajdz_dlugosc_sruby_zwyklej())
    print (znajdz_srube_zwykla())
    print ('++++++++++++sruby sprezpone+++++++++++++++++')
    print (znajdz_dostepne_srub_sprezone())
    print (znajdz_dostepne_ilosci_podkladek_sprezone())
    print (znajdz_zakres_zasisku_sprezone())
    print (znajdz_zacisk_sruby_sprezone())
    print (znajdz_dlugosc_sruby_sprezonej())
    print (znajdz_srube_sprezona())