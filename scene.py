from ovito.io import import_file
from ovito.modifiers import CreateBondsModifier, PythonScriptModifier
from ovito.vis import TextLabelOverlay
from PyQt5 import QtCore
import ovito

import sys
import numpy as np

def setDefaultColorsAndRadii(data):
	H = data.particle_properties["Particle Type"].types[0]
	Mg = data.particle_properties["Particle Type"].types[1]
	O2 = data.particle_properties["Particle Type"].types[2]
	O1 = data.particle_properties["Particle Type"].types[3]
	H.name = "H"
	O1.name = "O1"
	O2.name = "O2"
	Mg.name = "Mg"

	H.radius = 0.25
	O1.radius = 0.35
	O2.radius = 0.35
	Mg.radius = 0.5
	H.color = (1.0, 1.0, 1.0)
	O1.color = (1.0, 0.0, 0.0)
	O2.color = (1.0, 0.0, 0.0)
	Mg.color = (0.9411764705882353, 0.7843137254901961, 0.6274509803921569)

fileName = "trajectory.bin"
if len(sys.argv) > 1:
	fileName = sys.argv[1]

pipeline = import_file(fileName, columns=["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z"], multiple_frames = True)
pipeline.add_to_scene()
setDefaultColorsAndRadii(pipeline.source)

data = np.loadtxt("cube.z.txt")

def tempModifierFunction(frame, input, output):
	print("Finding pressure for frame %d: %f" % (frame, data[frame*100][1]))
	output.attributes['pressure'] = data[frame*100][1]

bonds = CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise)
bonds.bonds_display.width = 0.3
bonds.set_pairwise_cutoff("H", "O2", 2.0)
pipeline.modifiers.append(bonds)
pipeline.modifiers.append(PythonScriptModifier(function=tempModifierFunction))

# Create an overlay.
overlay = TextLabelOverlay(
    text = 'P=[pressure] MPa', 
    alignment = QtCore.Qt.AlignHCenter ^ QtCore.Qt.AlignBottom,
    offset_x = -0.3,
    offset_y = -0.01,
    font_size = 0.05,
    text_color = (1,1,1))

# Attach overlay to the active viewport.
viewport = ovito.dataset.viewports.active_vp
viewport.overlays.append(overlay)

pipeline.compute()