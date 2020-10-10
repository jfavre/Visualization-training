# Demonstration script for paraview version 5.8
# written by Jean M. Favre, Swiss National Supercomputing Centre
# tested Sat 10 Oct 2020 11:46:36 AM CEST

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
viewID = GetRenderView()

RequestData = """
import numpy as np
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
ts = executive.UPDATE_TIME_STEP().Get(outInfo)
dims = (exts[1]-exts[0]+1, exts[3]-exts[2]+1, exts[5]-exts[4]+1)

output.SetExtent(exts)
xaxis = np.linspace(-.5, 1., dims[0])
yaxis = np.linspace(-1.,1., dims[1])
zaxis = np.linspace(-1., .5, dims[2])
[xc,yc,zc] = np.meshgrid(zaxis,yaxis,xaxis, indexing="ij")
data = .1*ts +sin(ts) + np.sqrt(xc**2 + yc**2 + zc**2, dtype='f')
output.PointData.append(data.ravel(), "scalarA")
"""

RequestInfo = """
import numpy as np
executive = self.GetExecutive ()
outInfo = executive.GetOutputInformation(0)

dims = [24,24,24]
outInfo.Set(executive.WHOLE_EXTENT(), 0, dims[0]-1 , 0, dims[1]-1 , 0, dims[2]-1)
outInfo.Set(vtk.vtkDataObject.SPACING(), 1, 1, 1)
outInfo.Set(vtk.vtkDataObject.ORIGIN(), 0,0,0)
outInfo.Set(vtk.vtkAlgorithm.CAN_PRODUCE_SUB_EXTENT(), 1)
timesteps = np.arange(32)*.1
outInfo.Remove(executive.TIME_STEPS())
for timestep in timesteps:
  outInfo.Append(executive.TIME_STEPS(), timestep)
outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), timesteps[0])
outInfo.Append(executive.TIME_RANGE(), timesteps[-1])
"""

# create a new 'Programmable Source'
programmableSource1 = ProgrammableSource()
programmableSource1.OutputDataSetType = 'vtkImageData'
programmableSource1.Script = RequestData
programmableSource1.ScriptRequestInformation = RequestInfo
programmableSource1.UpdatePipelineInformation()

Show()
ResetCamera()

SaveData('ts.vti', Writetimestepsasfileseries=1, Filenamesuffix='_%02d')
