#! ##Structural unit converters

from strupy.units import *
from unum import Unum as __Unum

# Unum customization
tmp = __Unum.VALUE_FORMAT
precision_list = [1, 2, 3, 4, 5, 6]
precision = precision_list[1] #<<<< >calculation precision -
__Unum.VALUE_FORMAT = '%5.' + str (precision) + 'f'


#!----
unit_list = ['--metric--', 'kg', 't', '--imperial--', 'lb']
description = {}
description['kg'] = 'mass: metric kilogram'
description['t'] = 'mass: metric ton'
description['lb'] = 'mass: imperial pound'
show = False #<<< Mass conversion (mass)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[4] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[4] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'um', 'mm', 'cm', 'dm', 'm', 'km', '--imperial--', 'inch', 'ft', 'yd', 'mile']
description = {}
description['um'] = 'length: metric micrometer'
description['mm'] = 'length: metric millimeter'
description['cm'] = 'length: metric centimeter'
description['dm'] = 'length: metric decimeter'
description['m'] = 'length: metric meter'
description['km'] = 'length: metric kilometer'
description['inch'] = 'length: imperial inch'
description['ft'] = 'length: imperial foot'
description['yd'] = 'length: imperial yard'
description['mile'] = 'length: imperial mile'
show = False #<<< Length conversion (length)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[5] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[9] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'mm2', 'cm2', 'm2' , 'ha', '--imperial--', 'inch2', 'ft2', 'yd2']
description = {}
description['mm2'] = 'area: metric square millimeter'
description['cm2'] = 'area: metric square centimeter'
description['m2'] = 'area: metric square meter'
description['ha'] = 'area: metric hectare'
description['inch2'] = 'area: imperial square inch'
description['ft2'] = 'area: imperial square foot'
description['yd2'] = 'area: imperial square yard'
show = False #<<< Area conversion (length^2)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[3] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[8] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
l = dm3
unit_list = ['--metric--', 'mm3', 'cm3', 'dm3', 'l', 'm3', '--imperial--', 'inch3', 'ft3']
description = {}
description['mm3'] = 'volume: metric cubic millimeter'
description['cm3'] = 'volume: metric cubic centimeter'
description['dm3'] = 'volume: metric cubic decimeter'
description['l'] = 'volume: metric liter'
description['m3'] = 'volume: metric cubic meter'
description['inch3'] = 'volume: imperial cubic inch'
description['ft3'] = 'volume: imperial cubic foot'
show = False #<<< Volume conversion (length^3)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[3] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[8] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'mm4', 'cm4', 'm4', '--imperial--', 'inch4', 'ft4']
description = {}
description['mm4'] = 'moment of interia: metric millimeter to the fourth power'
description['cm4'] = 'moment of interia: metric centimeter to the fourth powerr'
description['m4'] = 'moment of interia: metric meter to the fourth power'
description['inch4'] = 'moment of interia: imperial inch to the fourth power'
description['inch4'] = 'moment of interia: imperial foot to the fourth power'
show = False #<<< Moment of interia conversion (length^4)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[2] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[5] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'N', 'kN', '--imperial--', 'lbf', 'kip']
description = {}
description['N'] = 'force: metric newton'
description['kN'] = 'force: metric kilonewton'
description['lbf'] = 'force: imperial pound-force'
description['kip'] = 'force: imperial kilopound-force'
show = False #<<< Force conversion (force)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[2] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[5] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'Nm', 'kNm', '--imperial--', 'lbfinch', 'lbfft', 'kipinch', 'kipft']
description = {}
description['Nm'] = 'moment of force: metric newton at meter arm'
description['kNm'] = 'moment of force: metric kilonewton at meter arm'
description['lbfinch'] = 'moment of force: imperial pound-force at inch arm'
description['lbfft'] = 'moment of force: imperial pound-force at foot arm'
description['kipft'] = 'moment of force: imperial kip at foot arm'
description['kipinch'] = 'moment of force: imperial kip at inch arm'
show = False #<<< Moment of force conversion (force * length)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[2] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[7] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'Pa', 'kN/m2', 'kPa', 'MPa', 'bar', 'GPa', '--imperial--', 'psi', 'ksi', 'psf', 'ksf']
description = {}
description['Pa'] = 'pressure: metric pascal'
description['kN/m2'] = 'pressure: metric kilonewton per squar meter'
description['kPa'] = 'pressure: metric kilopascal'
description['MPa'] = 'pressure: metric megapascal'
description['bar'] = 'pressure: metric bar'
description['GPa'] = 'pressure: metric gigapascal'
description['psi'] = 'pressure: imperial pound-force per square inch'
description['ksi'] = 'pressure: imperial kilopound-force per square inch'
description['psf'] = 'pressure: imperial pound-force per square foot'
description['ksf'] = 'pressure: imperial kilopound-force per square foot'
show = False #<<< Pressure conversion (force / lenght^2)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[4] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[9] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'kN/m', '--imperial--', 'lbf/ft', 'plf', 'kip/ft']
description = {}
description['kN/m'] = 'force per length: imperial kilonewton per meter'
description['lbf/ft'] = 'force per length: imperial pound-force per foot'
description['plf'] = 'force per length: imperial pound-force per foot'
description['kip/ft'] = 'force per length: imperial kilopound-force per foot'
show = False #<<< Force per lenght conversion (force / length)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[1] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[5] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'kN/m3', '--imperial--', 'lbf/inch3', 'pci', 'kip/ft3']
description = {}
description['kN/m3'] = 'subgrade modulus: metric kilonewton per cubic meter'
description['lbf/inch3'] = 'subgrade modulus: imperial pound-force per cubic foot'
description['pci'] = 'subgrade modulus: imperial pound-force per cubic inch'
description['kip/ft3'] = 'subgrade modulus: imperial kilopound-force per cubic foot'
show = False #<<< Unit weight conversion (force  / length^3)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[1] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[4] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value

#!----
unit_list = ['--metric--', 'kg/m3', 't/m3', '--imperial--', 'lb/ft3']
description = {}
description['kg/m3'] = 'density: metric kilogram per cubic meter'
description['t/m3'] = 'density: metric ton per cubic meter'
description['lb/ft3'] = 'density: imperial pound per cubic foot'
show = False #<<< Unit mass conversion (mass / length^3)
if show:
	input_quantity = 100 #<<< - input quantity
	input_unit = unit_list[1] #<<< - input unit
	input_unit_description = description[input_unit]
	#! (val_input_unit_description)

	input_value = input_quantity * eval(input_unit)
	#! >###val_input_value
	output_unit = unit_list[4] #<<<< convert to -
	output_unit_description = description[output_unit]
	#! (val_output_unit_description)
	output_value = input_value.asUnit(eval(output_unit))
	#! >###val_output_value
	#! ##val_input_value = val_output_value
#!--------

#! ###Need more features? Try [kipsiCalc](https://github.com/lukaszlaba/kipsiCalc) - simple calculator supporting unit calculations!
#! ###Download kipsiCalc for Windows [here](https://github.com/lukaszlaba/kipsiCalc/releases).

__Unum.VALUE_FORMAT = tmp




'''
SeeID : 887011
SeeCodeIsLocked
SeeField : XbeamStructure
SeeCategory : General 
SeeName : Unit converter
SeeDescription : Convert common units used for structural calculations. Metric and imperial units included.
'''















