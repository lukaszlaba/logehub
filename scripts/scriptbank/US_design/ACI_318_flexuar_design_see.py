# -*- coding: utf-8 -*-
from strupy import units as u
from unum import Unum
Unum.VALUE_FORMAT = "%15.2f"


#! ##ACI 318-19 SINGLY REINFORCED RECTANGULAR SECTION FLEXURE DESIGN 
#! (beta version for testing)

#-----------------------------------------------------------
#! ##1. Input data
#! ####Materials:
fy_list = [40*u.ksi, 50*u.ksi, 60*u.ksi, 75*u.ksi, 80*u.ksi]
fy = fy_list[2] #<< - specified yield strength of reinfoecement steel
fʹc_list = [3*u.ksi, 4*u.ksi, 5*u.ksi, 6*u.ksi, 7*u.ksi, 8*u.ksi, 9*u.ksi]
fʹc = fʹc_list[1] #<< - specified compressive strength of reinfoecement concrete
#! ####Section:
show = False #<<< show figure 
if show:
	#%img geometry.png
b = 12*u.inch #<< - section width
h = 20*u.inch #<< - section depth
#! ####Reinforcement:
db_list = ['#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#14', '#18' ]
db_dia = {'#3':3/8*u.inch, '#4':4/8*u.inch, '#5':5/8*u.inch,
          '#6':6/8*u.inch, '#7':7/8*u.inch, '#8':8/8*u.inch,
          '#9':9/8*u.inch, '#10':10/8*u.inch , '#11':11/8*u.inch, 
          '#14':14/8*u.inch, '#18':18/8*u.inch}
db_A =   {'#3':0.11*u.inch2, '#4':0.20*u.inch2, '#5':0.31*u.inch2,
          '#6':0.44*u.inch2, '#7':0.60*u.inch2, '#8':0.79*u.inch2,
          '#9':1.00*u.inch2, '#10':1.27*u.inch2, '#11':1.56*u.inch2, 
          '#14':2.25*u.inch2, '#18':4.00*u.inch2}
db = db_list[6] #<< - diameter of bars
db_selected = db
db = db_dia[db]

option = ['direct As area', 'bar quantity']
selected = option[1] #<<<< Reinforcement area defined by 
if selected == 'direct As area':
	As = 5.95*u.inch2 #<< - area of reinforcement
if selected == 'bar quantity':
	n_list =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 
	n = n_list[2] #<< - number of val_db_selected bars
	As = n * db_A[db_selected] #! - area of reinforcement
cc = 2*u.inch #<< - clear cover of reinforcement
#! ####Required factored moment:
Mu = 120*u.kipft #<< 

#-----------------------------------------------------------
#! ##2. Ratio of steel check
d = h - cc - db/2 #%requ - effective section depth
Unum.VALUE_FORMAT = "%15.4f"
ρ = As/(b*d) #%requ - current ratio of steel
#! ####Minimum ACI steel ratio requirement acc. ACI 9.6.1.1
ρmin1 = 3*(fʹc/u.psi)**0.5 / (fy/u.psi) #%requ
ρmin2 = 200 / (fy/u.psi) #%requ
ρmin = max(ρmin1, ρmin2) #%requ
Unum.VALUE_FORMAT = "%15.2f"
Asmin = ρmin*b*d #!
Unum.VALUE_FORMAT = "%15.4f"
#! For var_ρ the confition is:
if ρ > ρmin:
	ρ > ρmin #%equ (OK)
	#%img ico_pass.png
else:	
	ρ < ρmin #%equ (!!!)
	#%img ico_warning.png
	#! The reinforcement ratio is too small. Consider to increase the reinforecment area.
	
#! ####Maximum steel ratio acc. ACI 9.3.3
Unum.VALUE_FORMAT = "%15.2f"
#! The ACI requrement is that beams shall be tension-controled section and have net tensile strains as low as εt>εty+0.003
Es = 29000*u.ksi #!
Unum.VALUE_FORMAT = "%15.4f"
εty = fy / Es #%requ - steel tension yield strain (acc. ACI 21.2.2.1)
Unum.VALUE_FORMAT = "%15.2f"
fʹc #!
if 2500*u.psi<=fʹc<=4000*u.psi: 
	β1 = 0.85 #%requ - acc. ACI Tab 22.2.2.4.3(a)
if 4000*u.psi<fʹc<8000*u.psi:
	β1 = 0.85 - 0.05*(fʹc/u.psi - 4000)/1000 #%requ - acc. ACI Tab 22.2.2.4.3(b)
if fʹc>8000*u.psi:
	 β1 = 0.65 #%requ - acc. ACI Tab 22.2.2.4.3(c)
Unum.VALUE_FORMAT = "%15.4f"
ρmax = 0.85*β1*fʹc/fy * 0.003/(0.003+εty+0.003) #%requ
Asmax = ρmax*b*d #!
#! For var_ρ the confition is:
if ρ < ρmax:
	ρ < ρmax #%equ (OK)
	#%img ico_pass.png
else:	
	ρ > ρmax #%equ (!!!)
	#%img ico_warning.png
	#! The reinforcement ratio is higher than the ACI recommendation. If possibe consider to decrease the reinforcement since the steel area can not be fully counted in to section strength.
#! ####Calculation of reinforcement ratio ρb limit that producing balanced strain conditions and make section compession-control
ρb = 0.85*β1*fʹc/fy * 0.003/(0.003+εty) #%requ
Unum.VALUE_FORMAT = "%15.2f"
Ab = ρb*b*d #%requ 

#-----------------------------------------------------------
#! ##3. Nominal flexuar strength
Unum.VALUE_FORMAT = "%15.2f"
#! ####Depth of equivalent rectangular stress block calculation
a = As*fy / (0.85*fʹc*b) #%requ - equivalent depth assuming steel yield
c = a/β1 #%requ
Unum.VALUE_FORMAT = "%15.4f"
εt = 0.003 * (d-c)/c #%requ

Unum.VALUE_FORMAT = "%15.2f"
if εt >= εty:
	εt > εty #%equ - steel yilding
	fs = fy #%requ - steel stress at ultimate
	#%img ico_pass.png
if εt < εty:
	εt < εty #%equ
	#%img ico_warning.png
	#! Steel not yield. Note that this section is compression-control! Equivalent depth and steel stress need to be recalculated from the equation
	#! *0.85×β1×fʹc×b×c =As×0.003×Es×(d-c)/c*
	aa = 0.85*β1*fʹc*b
	bb = As*0.003*Es
	cc = -As*0.003*Es*d
	Δ = bb**2 - 4*aa*cc
	c = (-bb+Δ**0.5)/(2*aa)#! - recalculated compression depth from above equation
	a = β1*c #%requ - recalculated equivalent compression depth
	Unum.VALUE_FORMAT = "%15.4f"
	εt = 0.003*(d-c)/c #%requ - recalculated steel strain
	fs = εt*Es #%requ - recalculated steel stress

Unum.VALUE_FORMAT = "%15.2f"
#! ####Nominal flexuar strength caclulation
Mn = (As*fs*(d-a/2)).asUnit(u.kipft) #%requ
#-----------------------------------------------------------
#! ##4. Design flexuar strength
#! ####Reduction factor caclulation
Unum.VALUE_FORMAT = "%15.4f"
εt #! - ultimate state steel strain
εty #! - steel yield strin
if εt < εty:
	εt < εty #%equ
	#! compresion control range acc. 21.2.2
	control_type = 'compresion control'
	Φ = 0.65 #!
elif εt > εty+0.003:
	εt > εty+0.003 #%equ
	#! tension control range acc. 21.2.2
	control_type = 'tension control'
	Φ = 0.9 #!
else:
	εty > εt > εty+0.003 #%equ
	#! traansition  range acc. 21.2.2
	control_type = 'traansition'
	Φ = 0.65 + 0.25*(εt-εty)/0.003 #%requ


#! ####Design flexuar strength
ΦMn = Φ * Mn#%requ
#! ##5. Flexuar strength check
Mu #!
ΦMn #!
if Mu <= ΦMn:
	Mu < ΦMn #%equ (OK)
	#%img ico_pass.png
	#! Section is correct.
else:
	Mu > ΦMn #%equ (!!)
	#%img ico_failed.png
	#! Section failed!

Ur = Mu / ΦMn #%requ - utilization ratio for flexural ultimate strength
#!-----------------------------------------------------------
show = True #<<< summary extract
if show:
	Unum.VALUE_FORMAT = "%15.2f"
	#! ACI 318-19 SINGLE REINFORCED BEAM FLEXUAR DESIGN
	#! Materials: var_fʹc, var_fy
	#! Section size: var_b, var_h
	#! Reinforcement: var_db, var_cc, var_As
	Unum.VALUE_FORMAT = "%15.4f"
	#! Steel ratio: var_ρ Steel ratio limits: var_ρmin, var_ρmax
	Unum.VALUE_FORMAT = "%15.2f"
	#! Required factored strength: var_Mu
	#! Nominale strength: var_Mn
	#! Design Strength var_Φ, var_ΦMn (val_control_type) 
	#! Utilization ratio:  Mu / ΦMn = val_Ur

'''
SeeID : 833523
SeeField : XbeamStructure
SeeCategory : Concrete 
SeeName : ACI 318-19 Flexuar design
SeeDescription : Flexural design of singly reinforced rectangular section according ACI 318-19 code.
'''



