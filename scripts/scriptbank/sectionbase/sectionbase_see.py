# -*- coding: utf-8 -*-
from strupy import units as u
from strupy.steel.SectionBase import SectionBase
from strupy.steel.MaterialSteel import MaterialSteel
from strupy.x_graphic.SvgCreator2D import SvgCreator2D
import svgwrite

base = SectionBase()
steel = MaterialSteel()

#! ##Baza profili

#!--------------------------------------------------------------------------------

basename = 'EU'

basenam_list = base.get_available_databasenames()
basename = basenam_list[0] #<<< - wybierz baze profili

base.set_databasename(basename)

full_basename = base.get_database_name()
#! ####Baza profili - val_basename / val_full_basename

types = base.get_database_sectiontypes()
family = types[0] #<<< - wybierz rodzine profilu
names = base.get_database_sectionlistwithtype(family)
name = names[2] #<<< - wybierz przekroj

active = False #<<<  Parametry profilu
if active:
	prep = base.get_sectionparameters(name)
	prepdescription = base.get_parameters_description()
	selectedtype_description = base.get_database_sectiontypesdescription()[prep['figure']]
	#----------
	text=selectedtype_description + '\n'
	text+=  'Properites of  '+ prep['sectionname'] + '  section: \n'
	preptodisplay=('Ax', 'Ay', 'Az', 'Iomega', 'Ix', 'Iy', 'Iz', 'Wply', 'Wplz', 'Wtors', 
	'b', 'ea', 'es', 'gamma', 'h', 'mass', 'surf', 'Wy', 'Wz', 'vpy', 'vpz', 'vy', 'vz')
	for i in prep :
		if i in preptodisplay:
			text = i + '='+ str(prep[i])+' - '+ prepdescription[i]
			#! val_text 

active = False #<<<  Ksztalt profilu
if active:
	svg_scene = SvgCreator2D()
	svg_scene.scene = svgwrite.Drawing(size = ('300', '300'))
	scale_list = [10*u.mm, 25*u.mm, 50*u.mm, 75*u.mm, 100*u.mm]
	scale = scale_list[1] #<<< - set scale of view
	svg_scene.set_unit(scale / 20)
	svg_scene.setvievbox(center=[0.0*u.mm, 0.0*u.mm], width = 300, high=300, boarder = True)
	base.draw_sectiongeometry(svg_scene, name, 1)
	grid = 20.0 * svg_scene.unit
	svg_scene.addLine([5*grid, -3*grid], [6*grid, -3*grid])
	svg_scene.addLine([5*grid, -2.8*grid], [5*grid, -3.2*grid])
	svg_scene.addLine([6*grid, -2.8*grid], [6*grid, -3.2*grid])      
	svg_scene.addText(str(1*grid), [4.4*grid, -3*grid])
	svg_document = svg_scene.scene  #%svg


'''
SeeName : Sectionbase
SeeCategory : Structure

SeeDescription : Sectionbase of steel profile.
'''