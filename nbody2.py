## Harry Goldstein and Shalin Patel
## nbody2 Gravitaion module
## Provdes tools for the creation of and animation of
## planets in a vPython display.

# Requires vPython

from visual import *
import random
import os

G = 6.67E-11

scene = display(x=800, ambient=color.gray(0.4))

def makePlanet (p, r, c, v, m):
	"""
	Makes a planet with given position,
	radius, color, velocity, and mass
	"""
	planet = sphere (pos=p, radius=r, color=c, make_trail=True, retain=1000)
	planet.velocity = v
	planet.vtemp=v
	planet.mass = m
	planet.force = vector (0,0,0)
	planet.vempt = vector (0,0,0)
	planet.mtemp = vector(0,0,0)
	planet.ds = vector (0,0,0)
	planet.momentum = v * m
	planet.rkv = [vector(),vector(),vector(),vector()]
	planet.rkf = [vector(),vector(),vector(),vector()]
	planet.rkx = [vector(),vector(),vector(),vector()]
	return planet
	
def createList (filePath):
	"""
	Makes a new planet_list with parameters from a file
	"""
	if os.path.exists(filePath):
		file = open(filePath)
	else:
		print "failed to open file"
		return
	lines = file.readlines()
	p = [] #px, py, pz, r, c1, c2, c3, vx, vy, vz, m
	planet_list = []
	for line in lines:
		if line[0] != '.':
			p.append(float(line))
		else:
			planet_list.append(p)
			p = []
	return planet_list
	
def saveState (planet_list, newname):
	"""
	Writes current list of planets to a file
	"""
	file = open(os.getcwd()+ '\\saves\\' + newname, 'w+')
	for p in planet_list:
		file.write(str(p.pos.x) + '\n')
		file.write(str(p.pos.y) + '\n')
		file.write(str(p.pos.z) + '\n')
		file.write(str(p.radius) + '\n')
		file.write(str(p.color[0]) + '\n')
		file.write(str(p.color[1]) + '\n')
		file.write(str(p.color[2]) + '\n')
		file.write(str(p.velocity.x) + '\n')
		file.write(str(p.velocity.y) + '\n')
		file.write(str(p.velocity.z) + '\n')
		file.write(str(p.mass) + '\n')
		file.write('.\n')
	
def animate (planet_list, dt):
	"""
	Sets the planets of planet_list in motion based
	on the laws of universal gravitation and thetimestep 
	given by the parameter.
	"""
	scene.autoscale = False
	cpos = vector(0,0,0)
	masstot = 0
	for p in planet_list:
		cpos += p.pos*p.mass
		masstot += p.mass
	cpos = cpos/masstot
	center = sphere(pos=cpos, radius=1.0E5, color=color.white)
		
	while True:
		# Limit update rate
		rate(200)
		
		# Center of mass
		cpos = vector(0,0,0)
		masstot = 0
		for p in planet_list:
			cpos += p.pos*p.mass
			masstot += p.mass
		cpos = cpos/masstot
		center.pos = cpos
		scene.center = cpos
	
		# find ds
		for p in planet_list:
			# Find net force
			p.force = vector (0,0,0)
			for other in planet_list:
				if p != other:
					r = p.pos - other.pos
					p.force += (-G * p.mass * other.mass)/(mag(r)**2) * norm(r)
			#find k2
			p.mtemp = p.momentum + p.force*0.5*dt
			p.rkv[0] = (p.mtemp)/p.mass
			p.rkx[0] = p.pos + 0.5*dt*p.velocity
			
		for p in planet_list:
			# Find net force at midpoint using k2
			p.rkf[0]= vector (0,0,0)
			for other in planet_list:
				if p != other:
					r = p.rkx[0] - other.rkx[0]
					p.rkf[0] += (-G * p.mass * other.mass)/(mag(r)**2) * norm(r)		
			
		# Integrate and find k3
		for p in planet_list:
			p.mtemp = p.momentum + p.rkf[0]*0.5*dt
			p.rkv[1] = p.mtemp/p.mass
			p.rkx[1] = p.pos + 0.5*dt*p.rkv[0]
			
			
		for p in planet_list:
			# Find net force at midpoint with k3
			p.rkf[1] = vector (0,0,0)
			for other in planet_list:
				if p != other:
					r = p.rkx[1] - other.rkx[1]
					p.rkf[1] += (-G * p.mass * other.mass)/(mag(r)**2) * norm(r)
		
		# Integrate- find k4 then find change in position
		for p in planet_list:
			p.mtemp= p.momentum + dt*p.rkf[1]
			p.rkv[2] = p.mtemp/p.mass
			p.rkx[2] = p.pos + dt*p.rkv[1]
			
		for p in planet_list:
			# Find net force at midpoint with k4
			p.rkf[2] = vector (0,0,0)
			for other in planet_list:
				if p != other:
					r = p.rkx[2] - other.rkx[2]
					p.rkf[2] += (-G * p.mass * other.mass)/(mag(r)**2) * norm(r)			
		
		for p in planet_list:
			p.ds = (dt/6)*(p.velocity + 2*p.rkv[0] + 2*p.rkv[1] + p.rkv[2])		
			p.mtemp = (dt/6)*(p.force + 2*p.rkf[0] + 2*p.rkf[1] + p.rkf[2])
			p.momentum += p.mtemp
			p.velocity += p.mtemp/p.mass
		
		# Update position
		for p in planet_list:
			p.pos += p.ds
		
		# Collision detection
		for p in planet_list:
			for other in planet_list:
				if p != other and mag(p.pos - other.pos) < p.radius+other.radius:
					planet_list.append(makePlanet((p.pos+other.pos)/2, (p.radius**3+other.radius**3)**(1.0/3.0), 
										(p.color[0]+other.color[0]/2,p.color[1]+other.color[1]/2,p.color[2]+other.color[2]/2), 
										((p.mass*p.velocity+other.mass*other.velocity)/(p.mass+other.mass)), p.mass+other.mass))
					other.visible = False
					other.trail_object.visible = False
					planet_list.remove(other)
					del other
					p.visible = False
					p.trail_object.visible = False
					planet_list.remove(p)
					del p
					break 