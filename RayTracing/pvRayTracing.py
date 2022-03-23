# Created by
#
# Dr. Jean M. Favre, Swiss National Supercomputing Centre
# Senior Visualization Software Engineer
#
# Tested with ParaView 5.10.1 and ospray 2.8.0
# Wed Mar 23 01:08:21 PM CET 2022

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

mf1 = "/users/jfavre/Projects/ParaView/ospray_mats.json"
materialLibrary1 = GetMaterialLibrary()
print("using materials: {:}".format(mf1))
materialLibrary1.LoadMaterials = mf1

Batch = True
OptiXEnabled = False
ImageCount = 0

OSPRay_Version = "OSPRay2.8.0"
OptiX_Version  = "Optix6.5"

if Batch:
  ProgressivePasses = 0
  SamplesPerPixel = 40
else:
  ProgressivePasses = 100
  SamplesPerPixel = 1

# Create a new 'Light'
light1 = CreateLight()
light1.Position = [50.0, 50.0, -150.0]

light2 = CreateLight()
light2.Position = [0.0, 0.0, 1.0]
light2.Intensity = .3

# create light
# Create a new 'Render View'
renderView1 = GetRenderView()
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.OrientationAxesVisibility = 0
renderView1.CenterOfRotation = [0.0, 0.4856886910475378, 0.0]
renderView1.UseLight = 0
renderView1.StereoType = 0
renderView1.CameraPosition = [-2.0845170131514843, 1.251255184574042, 1.885297086960957]
renderView1.CameraFocalPoint = [38.85293334447471, -12.375838003738075, -31.700665545414243]
renderView1.CameraViewUp = [0.20406248231693128, 0.9682879470153982, -0.14414213462883688]
renderView1.CameraParallelScale = 14.151484590759953
renderView1.Background = [0.1803921568627451, 0.20392156862745098, 0.21176470588235294]
renderView1.EnableRayTracing = 0 # Classic OpenGL
renderView1.SamplesPerPixel = SamplesPerPixel
renderView1.AdditionalLights = [light1, light2]
renderView1.OSPRayMaterialLibrary = materialLibrary1

imageRes = [1024, 1024]
#renderView1.ViewSize = imageRes
SetActiveView(renderView1)

# client side
#info = GetOpenGLInformation()
#print("Vendor:   %s" % info.GetVendor())
#print("Version:  %s" % info.GetVersion())
#print("Renderer: %s" % info.GetRenderer())

# server side
info = GetOpenGLInformation(servermanager.vtkSMSession.RENDER_SERVER)
print("Vendor:   %s" % info.GetVendor())
print("Version:  %s" % info.GetVersion())
print("Renderer: %s" % info.GetRenderer())

# create a new 'Programmable Source'
Mirrors = ProgrammableSource(guiName="Mirrors")
Mirrors.OutputDataSetType = 'vtkUnstructuredGrid'
Mirrors.Script = """
import vtk
from vtk import VTK_WEDGE
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
XYZ = np.array([ 1.0, 0.0, -1.0,
               3.0, 0.0, -5.0,
               2.0, 0.0,  5.0,
               1.0,  1.0, -1.0,
               3.0,  1.0, -5.0,
               2.0,  1.0,  5.0 ])
nnodes = XYZ.shape[0]//3
CONNECTIVITY = np.array([6, 0,1,2,3,4,5])
nelts = 1
CELL_TYPES = np.full((nelts), VTK_WEDGE, np.ubyte)
CELL_OFFSETS = np.arange(nelts)
CELL_OFFSETS = 0 * CELL_OFFSETS
output.SetCells(CELL_TYPES, CELL_OFFSETS, CONNECTIVITY)
output.Points = XYZ.reshape((nnodes,3))
"""
Mirrors.ScriptRequestInformation = ''
Mirrors.PythonPath = ''

# create a new 'Cylinder'
cylinder2 = Cylinder(guiName="straw")
cylinder2.Resolution = 128
cylinder2.Height = 0.75
cylinder2.Radius = 0.015
cylinder2.Center = [0.0, 0.35, 0.0]

# create a new 'Cylinder'
cylinder1 = Cylinder(guiName="Water")
cylinder1.Resolution = 2000
cylinder1.Height = 0.5
cylinder1.Radius = 0.253 # small scale up suggested by Tim Biedert to "fix" refraction
cylinder1.Center = [0.0, 0.2501, 0.0] # small offset suggested by Tim Biedert to resolve depth fighting with ground plane

# create a new 'Plane'
plane1 = Plane()
plane1.Origin = [-10.0, 0.0, -10.0]
plane1.Point1 = [-10.0, 0.0, 10.0]
plane1.Point2 = [10.0, 0.0, -10.0]
plane1.XResolution = 200
plane1.YResolution = 200

# show data from plane1
plane1Display = Show(plane1, renderView1)

# trace defaults for the display properties.
plane1Display.Representation = 'Surface With Edges'
plane1Display.ColorArrayName = ['POINTS', '']
plane1Display.LineWidth = 0.1
plane1Display.Ambient = 0.2
plane1Display.Diffuse = 0.8

# show data from cylinder1
cylinder1Display = Show(cylinder1, renderView1)

# trace defaults for the display properties.
cylinder1Display.Representation = 'Surface'
cylinder1Display.AmbientColor = [0.0, 0.0, 0.0]
cylinder1Display.ColorArrayName = ['POINTS', '']
cylinder1Display.Ambient = 1.0
cylinder1Display.Diffuse = 0.8

# show data from cylinder2
cylinder2Display = Show(cylinder2, renderView1)


# trace defaults for the display properties.
cylinder2Display.Representation = 'Surface'
cylinder2Display.ColorArrayName = [None, '']
cylinder2Display.Orientation = [-20.0, 0.0, 0.0]

########  added to replace the glass container with hexahedral grid

Res = 2000
outercylinder = Cylinder()
outercylinder.Resolution = Res
outercylinder.Height = 0.6
outercylinder.Radius = 0.27
outercylinder.Center = [0.0, 0.2501, 0.0]
outercylinder.Capping = 0

# create a new 'Cylinder'
innercylinder = Cylinder()
innercylinder.Resolution = Res
innercylinder.Height = 0.6
innercylinder.Radius = 0.25
innercylinder.Center = [0.0, 0.2501, 0.0]
innercylinder.Capping = 0

# create a new 'Append Datasets'
appendDatasets1 = AppendDatasets(Input=[innercylinder, outercylinder])

# create a new 'Programmable Filter'
NewGlass = ProgrammableFilter(Input=appendDatasets1, guiName="NewGlass")
NewGlass.Script = """import vtk
from vtk import VTK_HEXAHEDRON
import numpy as np
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)

output.Points = inputs[0].Points
nelts = output.Points.shape[0]//4
CELL_OFFSETS = np.arange(nelts)
CELL_OFFSETS = (8+1) * CELL_OFFSETS

CELL_TYPES = np.full((nelts), VTK_HEXAHEDRON, np.ubyte)

l0 = l0 = np.append(np.array([2*i for i in range(nelts)]), 0)
l2 = 2*nelts + l0

connectivity=8*np.ones((9*nelts), dtype='int')

for i in range(nelts):
  connectivity[1+9*i  ] = l2[i]
  connectivity[1+9*i+1] = l2[i+1]
  connectivity[1+9*i+2] = l2[i+1]+1
  connectivity[1+9*i+3] = l2[i]+1
  connectivity[1+9*i+4] = l0[i]
  connectivity[1+9*i+5] = l0[i+1]
  connectivity[1+9*i+6] = l0[i+1]+1
  connectivity[1+9*i+7] = l0[i]+1

output.SetCells(CELL_TYPES, CELL_OFFSETS, connectivity)
"""

NewGlassDisplay = Show(NewGlass, renderView1)
NewGlassDisplay.Representation = 'Surface'
NewGlassDisplay.OSPRayMaterial = 'glass'
##########################
# show data from Mirrors
MirrorsDisplay = Show(Mirrors, renderView1)
MirrorsDisplay.Representation = 'Surface With Edges'
MirrorsDisplay.ColorArrayName = [None, '']

# First do classic OpenGL rendering with Ambient Light only
MirrorsDisplay.Ambient = 1.0
MirrorsDisplay.Diffuse = 0.0
if Batch:
  SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OSPRay_Version, ImageCount)), ImageResolution=imageRes)
  ImageCount += 1

# Second do classic OpenGL rendering with Ambient and Diffuse light
MirrorsDisplay.Ambient = 0.2
MirrorsDisplay.Diffuse = 0.8
if Batch:
  SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OSPRay_Version, ImageCount)), ImageResolution=imageRes)
  ImageCount += 1

print("Switching to OSPRay 'sci-vis' Rendering")
# Third do OSPRay rendering without shadows
renderView1.EnableRayTracing = 1
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.LightScale = 1
renderView1.Shadows = 0
renderView1.AmbientSamples = 1
renderView1.Denoise = 1
renderView1.ProgressivePasses = ProgressivePasses  # must launch with --enable-streaming

if Batch:
  SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OSPRay_Version, ImageCount)), ImageResolution=imageRes)
  ImageCount += 1
  
# Fourth do OSPRay rendering with shadows
renderView1.Shadows = 1
if Batch:
  SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OSPRay_Version, ImageCount)), ImageResolution=imageRes)
  ImageCount += 1

print("Switching to OSPRay 'pathtracer' Rendering")
# Fifth do OSPRay rendering with *soft* shadows
renderView1.BackEnd = 'OSPRay pathtracer'
light1.Radius = 5
if Batch:
  SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OSPRay_Version, ImageCount)), ImageResolution=imageRes)
  ImageCount += 1

# Sixth do OSPRay rendering with shadows and a reflective material
MirrorsDisplay.OSPRayMaterial = 'copper'
if Batch:
  SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OSPRay_Version, ImageCount)), ImageResolution=imageRes)
  ImageCount += 1

# Seventh do OSPRay rendering. A wood material
cylinder1Display.OSPRayMaterial = 'wood'
if Batch:
  SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OSPRay_Version, ImageCount)), ImageResolution=imageRes)
  ImageCount += 1

# Eigth do OSPRay rendering. A refractive material
cylinder1Display.OSPRayMaterial = 'water'
if Batch:
  SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OSPRay_Version, ImageCount)), ImageResolution=imageRes)
  ImageCount += 1

###############################################################################

if OptiXEnabled:
  ImageCount = 4
  print("Switching to OptiX 'pathtracer' Rendering")

  renderView1.BackEnd = 'OptiX pathtracer'
  cylinder1Display.OSPRayMaterial = 'None'
  MirrorsDisplay.OSPRayMaterial = 'None'
  if Batch:
    SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OptiX_Version, ImageCount)), ImageResolution=imageRes)
    ImageCount += 1

  # Tenth do OptiX rendering with shadows and a reflective material
  MirrorsDisplay.OSPRayMaterial = 'copper'
  if Batch:
    SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OptiX_Version, ImageCount)), ImageResolution=imageRes)
    ImageCount += 1

  # Eleventh OptiX rendering. A wood material
  cylinder1Display.OSPRayMaterial = 'wood'
  if Batch:
    SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OptiX_Version, ImageCount)), ImageResolution=imageRes)
    ImageCount += 1

  # 12-th do Optix rendering. A refractive material
  cylinder1Display.OSPRayMaterial = 'water'
  if Batch:
    SaveScreenshot(format("RayTracing-%s-tutorial.%02d.png" % (OptiX_Version, ImageCount)), ImageResolution=imageRes)
    ImageCount += 1

