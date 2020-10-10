from paraview.simple import *
import npimporters
import numpy as np

# create a regular cartesian grid, a.k.a. vtkImageData

dims = [64,64,64]
bounds = (-10.0, 10.0, -10.0, 10.0,-10.0, 10.0)
xaxis = np.linspace(bounds[0], bounds[1], dims[0])
yaxis = np.linspace(bounds[2], bounds[3], dims[1])
zaxis = np.linspace(bounds[4], bounds[5], dims[2])
[xc,yc,zc] = np.meshgrid(zaxis,yaxis,xaxis, indexing="ij")
data = xc**2 + yc**2 + zc**2

from vtk.util.vtkImageImportFromArray import vtkImageImportFromArray
iD = vtkImageImportFromArray()
iD.SetArray(data)
iD.SetDataOrigin((bounds[0], bounds[2], bounds[4]))
iD.SetDataSpacing(((bounds[1]-bounds[0])/(dims[0]-1),
                   (bounds[3]-bounds[2])/(dims[0]-1),
                   (bounds[5]-bounds[4])/(dims[0]-1)))
iD.Update()
iD.GetOutput().GetPointData().SetActiveScalars("scalars")

print("mesh dimensions = ", iD.GetOutput().GetDimensions())
assert iD.GetOutput().GetPointData().GetArray(0).GetName() == 'scalars'
datarange = iD.GetOutput().GetPointData().GetArray(0).GetRange()
print("data scalar range = ", datarange)

# create a new 'PVTrivialProducer'
pVTrivialProducer0 = PVTrivialProducer(guiName="UniformGrid")
obj = pVTrivialProducer0.GetClientSideObject()
obj.SetOutput(iD.GetOutput())
pVTrivialProducer0.UpdatePipeline()

rep0=Show(pVTrivialProducer0)
rep0.Representation = 'Surface With Edges'

################################################################################
# create a rectilinear grid
#dims = [64,64,64] # Radius dimension, Theta dimension, Z dimension
xaxis = np.linspace(0., 1., dims[0])
xaxis = xaxis**2
yaxis = np.linspace(0., 1., dims[1])
yaxis = np.sqrt(yaxis)
zaxis = np.linspace(0., 1., dims[2])

[xc,yc,zc] = np.meshgrid(zaxis,yaxis,xaxis, indexing="ij")
data = np.sqrt(xc**2 + yc**2 + zc**2)

rG = npimporters.vtkRectGridFromArrays()
rG.SetCoordinates(xaxis, yaxis, zaxis)
rG.AddArray(data, "scalars")

print("RectilinearGrid dimensions = ", rG.GetDimensions())
assert rG.GetOutput().GetPointData().GetArray(0).GetName() == 'scalars'
datarange = rG.GetOutput().GetPointData().GetArray("scalars").GetRange()
print("RectilinearGrid  data scalar range = ", datarange)

# create a new 'PVTrivialProducer'
pVTrivialProducer1 = PVTrivialProducer(guiName="RectilinearGrid")
obj = pVTrivialProducer1.GetClientSideObject()
obj.SetOutput(rG.GetOutput())
pVTrivialProducer1.UpdatePipeline()

rep1=Show(pVTrivialProducer1)
rep1.Representation = 'Surface With Edges'

################################################################################
# create a cylindrical - structured grid
#dims = [13,27,15] # Radius dimension, Theta dimension, Z dimension
Raxis = np.linspace(1., 2., dims[0])
Thetaaxis = np.linspace(0.,np.pi*1.5, dims[1])
Zaxis = np.linspace(0., 2.0, dims[2])
Z, t, r = np.meshgrid(Zaxis, Thetaaxis, Raxis, indexing="ij")
X = r * np.cos(t)
Y = r * np.sin(t)

NsG = npimporters.vtkStructuredGridFromArrays()
NsG.SetCoordinates(X, Y, Z)
NsG.AddArray(r.ravel(), "radius")
NsG.AddArray(Z.ravel(), "z-elevation")
NsG.AddArray(t.ravel(), "angle")

print("StructuredGrid mesh dimensions = ", NsG.GetDimensions())
print("StructuredGrid mesh bounds = ", NsG.GetOutput().GetBounds())
assert NsG.GetOutput().GetPointData().GetArray(1).GetName() == 'z-elevation'
datarange = NsG.GetOutput().GetPointData().GetArray("z-elevation").GetRange()
print("StructuredGrid data scalar range = ", datarange)

# create a new 'PVTrivialProducer'
pVTrivialProducer2 = PVTrivialProducer(guiName="StructuredGrid")
obj = pVTrivialProducer2.GetClientSideObject()
obj.SetOutput(NsG.GetOutput())
pVTrivialProducer2.UpdatePipeline()

rep2=Show(pVTrivialProducer2)
rep2.Representation = 'Surface With Edges'

###############################################################################
# create a point cloud

nbpts = 10000
X = np.random.random_sample((nbpts, 3))

PC = npimporters.vtkPointSetFromArrays()
#PC.SetCoordinates(X[:,0], X[:,1],X[:,2])
PC.SetVCoordinates(X)
PC.AddArray(X[:,0]*X[:,0] + X[:,1]*X[:,1] + X[:,2]*X[:,2], "distancesq")
PC.AddArray(X[:,0], "X")

print("Point Cloud has ", PC.GetOutput().GetNumberOfPoints())
# create a new 'PVTrivialProducer'
pVTrivialProducer3 = PVTrivialProducer(guiName="Point Cloud")
obj = pVTrivialProducer3.GetClientSideObject()
obj.SetOutput(PC.GetOutput())
pVTrivialProducer3.UpdatePipeline()

rep3=Show(pVTrivialProducer3)
rep3.Representation = 'Points'
