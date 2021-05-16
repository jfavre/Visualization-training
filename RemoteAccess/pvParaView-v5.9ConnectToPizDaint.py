# Written by Jean M Favre, CSCS
# Test passed with ParaView v5.9 Fri Apr  9 10:14:58 CEST 2021
#
# For Linux users only.
# syntax:
# paraview --script=pvParaView-v5.9ConnectToPizDaint.py
#
##############################################################################
from paraview.simple import *
#from paraview.modules.vtkRemotingViews import vtkPVOpenGLInformation

import os

username      = "jfavre"              # your username on Piz Daint
hosts         = ["daint103.cscs.ch"]  # a fixed host address daint10?.cscs.ch
userid        = 1100                  # your Linux userid on Piz Daint
remoteScript  = "/users/jfavre/rc-submit-pvserver.sh"
#remoteScript  = "/apps/daint/UES/ParaView/rc-submit-pvserver.sh"
atime         = "00:09:59"          # allocation time
nTasksPerNode = 4
nNodes        = 1
jobName       = "pvserver"
partition     = "normal"             # choices are "debug", or "normal"
memory        = "standard"          # choices are "standard", or "high"
versions      = ["GNU-5.9", "GNU-5.9-OSMesa"]
account       = "csstaff"

host = hosts[0]
cmd = format("ssh -l %s -R %s:localhost:%s %s \"%s %s %s %d %d %d %s %s %s %s %s; sleep 200\"" % 
      (username, userid, userid, host, remoteScript, jobName+"@"+host, atime, nNodes, nTasksPerNode, 
       userid, host, versions[0], partition, memory, account))

pid = os.fork()
if pid == 0: # pid is only equal to 0 in the child process
    os.system(cmd)

ReverseConnect(str(userid)) # will block until the compute node calls back.

# Create a new 'Render View'
renderView1 = GetRenderView()
renderView1.CameraPosition = [-42.94939946237012, 38.1029243396441, 34.37989545754576]
renderView1.CameraViewUp = [0.26066568322867206, 0.7919803263419563, -0.5521055734859216]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 17.320508075688775

wavelet1 = Wavelet(registrationName='Wavelet')
wavelet1.WholeExtent = [0, 255, 0, 255, 0, 255]

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

print('################ Local desktop ############')
info = GetOpenGLInformation() # client-side graphics hardware

print("Vendor:   %s" % info.GetVendor())
print("Version:  %s" % info.GetVersion())
print("Renderer: %s" % info.GetRenderer())
print('################ Remote Render Server ############')
info = GetOpenGLInformation(location=servermanager.vtkSMSession.RENDER_SERVER) # server-side graphics hardware
print("Vendor:   %s" % info.GetVendor())
print("Version:  %s" % info.GetVersion())
print("Renderer: %s" % info.GetRenderer())
print('##################################################')

