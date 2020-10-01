# Written by Jean M Favre, CSCS
# Test passed with ParaView v5.8.1 Thu 01 Oct 2020 08:38:49 AM CEST
#
# For Linux users only.
# syntax:
# paraview --script=pvConnect_daint.py
#
##############################################################################
from paraview.simple import *

import os

username      = "jfavre"            # your username on Piz Daint
host          = "daint102.cscs.ch"  # a fixed host address daint10?.cscs.ch
userid        = 12345               # your Linux userid on Piz Daint
remoteScript  = "/apps/daint/UES/ParaView/rc-submit-pvserver.sh"
atime         = "00:04:59"          # allocation time
nTasksPerNode = 8
nNodes        = 1
jobName       = "pvserver"
partition     = "debug"             # choices are "debug", or "normal"
memory        = "standard"          # choices are "standard", or "high"
version       = "GNU-5.8"           # choices are "GNU-5.8" or "GNU-5.8-OSMesa"

cmd = format("ssh -l %s -R %s:localhost:%s %s \"%s %s %s %d %d %d %s %s %s %s; sleep 6000\"" % 
      (username, userid, userid, host, remoteScript, jobName, atime, nNodes, nTasksPerNode, 
       userid, host, version, partition, memory))

pid = os.fork()
if pid == 0: # pid is only equal to 0 in the child process
    os.system(cmd)

ReverseConnect(str(userid)) # will block until the compute node calls back.

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [932, 737]
renderView1.CameraPosition = [-42.94939946237012, 38.1029243396441, 34.37989545754576]
renderView1.CameraViewUp = [0.26066568322867206, 0.7919803263419563, -0.5521055734859216]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 17.320508075688775

SetActiveView(None)

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)

SetActiveView(renderView1)

wavelet1 = Wavelet()

# show data from wavelet1
wavelet1Display = Show(wavelet1, renderView1, 'UniformGridRepresentation')

# get color transfer function/color map for 'vtkProcessId'
vtkProcessIdLUT = GetColorTransferFunction('vtkProcessId')
vtkProcessIdLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 7.5, 0.865003, 0.865003, 0.865003, 15.0, 0.705882, 0.0156863, 0.14902]
vtkProcessIdLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
wavelet1Display.Representation = 'Surface'
wavelet1Display.ColorArrayName = ['POINTS', 'vtkProcessId']
wavelet1Display.LookupTable = vtkProcessIdLUT

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
wavelet1Display.ScaleTransferFunction.Points = [37.35310363769531, 0.0, 0.5, 0.0, 276.8288269042969, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
wavelet1Display.OpacityTransferFunction.Points = [37.35310363769531, 0.0, 0.5, 0.0, 276.8288269042969, 1.0, 0.5, 0.0]

# get color legend/bar for vtkProcessIdLUT in view renderView1
vtkProcessIdLUTColorBar = GetScalarBar(vtkProcessIdLUT, renderView1)
vtkProcessIdLUTColorBar.Title = 'vtkProcessId'

# set color bar visibility
vtkProcessIdLUTColorBar.Visibility = 1

# show color legend
wavelet1Display.SetScalarBarVisibility(renderView1, True)
Render()
wavelet1Display.RescaleTransferFunctionToDataRange(False, True)


