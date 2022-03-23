# Written by Jean M Favre, CSCS
# Test passed with ParaView v5.10.1 Wed Mar 23 12:47:22 PM CET 2022
#
# For Linux users only.
# syntax:
# paraview --script=pvParaView-v5.10ConnectToCrays.py
#
# You must edit the username, userid, and account
##############################################################################
from paraview.simple import *
import subprocess

username      = "jfavre"            # your username at CSCS
hosts         = ["daint104.cscs.ch", "dom.cscs.ch", "alps03.cscs.ch"]  # the login node
userid        = 1100               # your Linux userid on Piz Daint
remoteScript  = "/apps/daint/UES/ParaView/rc-submit-pvserver.sh"
atime         = "00:09:59"          # allocation time
nTasksPerNode = 1
nNodes        = 1
jobName       = "pvserver"
partition     = "debug"             # choices are "debug", "normal"
memory        = "standard"          # choices are "standard", or "high"
versions      = [
                "Daint-5.10", "Daint-5.10-OSMesa"
                ]
versions     += ["Eiger-5.10-OSMesa"]
account       = "csstaff"
reservation   = ["", "interact_gpu", "interact_mc", "interact"]

host = hosts[0]

cmd = format("ssh -l %s -R %s:localhost:%s %s %s %s %s %d %d %d %s %s %s %s %s %s; sleep 600" % 
      (username, userid, userid, host, remoteScript, jobName+"@"+host, atime, nNodes, nTasksPerNode, 
       userid, host, versions[1], partition, memory, account, reservation[0]))

c = subprocess.Popen(cmd.split())
ReverseConnect(str(userid)) # will block until the compute node calls back.

# Create a new 'Render View'
renderView1 = GetRenderView()
renderView1.CameraPosition = [-42.94939946237012, 38.1029243396441, 34.37989545754576]
renderView1.CameraViewUp = [0.26066568322867206, 0.7919803263419563, -0.5521055734859216]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 17.320508075688775

wavelet1 = Wavelet(registrationName='Wavelet')
wavelet1.WholeExtent = [0, 7, 0, 7, 0, 7]

tet = Tetrahedralize()
shrink = Shrink()
triangles = ExtractSurface()

wavelet1Display = Show(triangles, renderView1, 'UniformGridRepresentation')
wavelet1Display.Representation = 'Surface'

Render()
#ColorBy(wavelet1Display, ('POINTS', 'vtkProcessId'))
ColorBy(wavelet1Display, ('POINTS', 'RTData'))
#wavelet1Display.RescaleTransferFunctionToDataRange(False, True)
#vtkProcessIdLUT = GetColorTransferFunction('vtkProcessId')
#vtkProcessIdLUTColorBar = GetScalarBar(vtkProcessIdLUT, renderView1)
#vtkProcessIdLUTColorBar.Visibility = 1

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

