from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
import subprocess, os
import numpy as np
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-x", type=int, default=40)
parser.add_argument("-y", type=int, default=40)
parser.add_argument("-z", type=int, default=5)
parser.add_argument("--waterz", type=float, default=9)
parser.add_argument("--numwater", "-w", type=int, default=9700)
args = parser.parse_args()

mass_H = 1.6737236*10**-27 #kg
mass_O = 2.6566962*10**-26 #kg
mass = (mass_O + (2*mass_H))* args.numwater
volume = (args.waterz*(args.x*4.217)*(args.y*4.217))*10**-30
density = mass / volume
print(density)


unitCellSize = 4.217
finalLx = unitCellSize*args.x
finalLy = unitCellSize*args.y
finalLz = unitCellSize*args.z + args.waterz + 60 # some extra space

#
# Create periclase slab
#



pipeline = import_file("pc_unitcell.xyz", columns = ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
pipeline.add_to_scene()
cell = pipeline.source.expect(SimulationCell)
with cell.modify() as mat:
	mat[0,0] = unitCellSize
	mat[1,1] = unitCellSize
	mat[2,2] = unitCellSize

pipeline.modifiers.append(ReplicateModifier(num_x=args.x, num_y=args.y, num_z=args.z, adjust_box=True))
pipeline.compute()
cell = pipeline.output.expect(SimulationCell)

export_file(pipeline, "pc_slab.xyz", "xyz", columns = ["Particle Type", "Position.X", "Position.Y", "Position.Z"])

lx = cell[0,0]
ly = cell[1,1]
lz = cell[2,2]
cellCopy = np.copy(cell)



#
# Create periclase cube
#



pipeline = import_file("pc_unitcell.xyz", columns = ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
pipeline.add_to_scene()
cell = pipeline.source.expect(SimulationCell)
with cell.modify() as mat:
	mat[0,0] = 4.217
	mat[1,1] = 4.217
	mat[2,2] = 4.217

pipeline.modifiers.append(ReplicateModifier(num_x=9, num_y=9, num_z=6, adjust_box=True))
pipeline.compute()
cell = pipeline.output.expect(SimulationCell)

export_file(pipeline, "pc_cube.xyz", "xyz", columns = ["Particle Type", "Position.X", "Position.Y", "Position.Z"])

l_cube = mat[0,0]*(9/2)



#
# Create packmol file
#



interface_inp_template = """tolerance 2.0
filetype xyz
output interface.xyz 

structure water.xyz
  number %d
  inside box 0. 0. %f %f %f %f
end structure 

structure pc_slab.xyz
  number 1
  inside box 0. 0. 1. %f %f %f
  end structure

structure pc_cube.xyz
  number 1
  constrain_rotation x 0. 0.
  constrain_rotation y 0. 0.
  constrain_rotation z 0. 0.
  inside box %f %f %f %f %f %f
end structure"""

with open("interface.inp", "w") as outfile:
	outputFileContent = interface_inp_template % (args.numwater, lz, lx, ly, 1+lz+args.waterz, lx, ly, 1+lz, (lx/2) - l_cube, (ly/2) - l_cube, 1+lz+args.waterz+10, (lx/2) + l_cube, (ly/2) + l_cube, 1+lz+args.waterz+10+(2*l_cube))
#	outputFileContent = interface_inp_template % ( (lx/2) - l_cube, (ly/2) - l_cube, 1+lz+args.waterz+10, (lx/2)+ l_cube, (ly/2) + l_cube, 1+lz+args.waterz+10+(2*l_cube))
	outfile.write(outputFileContent)
	
subprocess.call("packmol < interface.inp", shell=True)


#
# Adding bonds
#


pipeline.remove_from_scene()

pipeline = import_file("interface.xyz", columns = ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
pipeline.add_to_scene()

hydrogenOxygenDistance = 1.5

bondsModifier = CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise)
bondsModifier.set_pairwise_cutoff("O", "H", hydrogenOxygenDistance )
pipeline.modifiers.append(bondsModifier)

bonds = pipeline.compute().expect(Bonds)
cell = pipeline.source.expect(SimulationCell)

with cell.modify() as mat:
	for i in range(2):
		for j in range(4):
			print("Old [", i, ", ", j, ": ", mat[i,j])
			print("New [", i, ", ", j, ": ", cellCopy[i,j])
			mat[i,j] = cellCopy[i,j]
	mat[0,3] = 0.0  # Move x origin to 0.0
	mat[1,3] = 0.0  # Move y origin to 0.0
	mat[2,3] = -1.0  # Move z origin to 0.0
	mat[2,2] = finalLz

export_file(pipeline, "slab_and_water_without_angles.data", "lammps/data", atom_style="full")
pipeline.remove_from_scene()



#
# Adding angles
#



pipeline = import_file("slab_and_water_without_angles.data")
data = pipeline.compute()

triplets = []
for i in range(0,len(bonds), 2):
	identifiers = data.particle_properties["Particle Identifier"]
	bond1 = bonds[i]
	bond2 = bonds[i+1]

	oxygen    = identifiers[ bond1[1] ] 
	hydrogen1 = identifiers[ bond1[0] ]
	hydrogen2 = identifiers[ bond2[0] ]
	triplets.append([ hydrogen1, oxygen, hydrogen2 ])

with open("slab_and_water_without_angles.data", "r") as infile:
	lines = infile.readlines()
	with open("slab_and_water.data", "w") as outfile:
		for line in lines:
			outfile.write(line)
			if "bond types" in line:
				outfile.write("%d angles\n" % len(triplets))
				outfile.write("1 angle types\n")
		outfile.write("\n")
		outfile.write("Angles\n")
		outfile.write("\n")
		for i, triplet in enumerate(triplets):
			outfile.write("%d %d %d %d %d \n" % (i+1, 1, triplet[0], triplet[1], triplet[2]))
		outfile.write("\n")


# mass_H = 1.6737236*10**-27 #kg
# mass_O = 2.6566962*10**-26 #kg
# mass = (mass_O + (2*mass_H))* args.numwater
# volume = (args.waterz*(args.x*4.217)*(args.y*4.217))*10**-30
# density = mass / volume
# print(density)

