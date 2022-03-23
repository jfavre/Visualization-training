# state file tested with paraview version 5.10.1
#
# Tested Wed Mar 23 01:17:26 PM CET 2022


from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [394, 344]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [3.3199994008318754, 3.319997731645344, 3.3199989599470427]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [5.310857905828319, 6.494278787262183, 10.666535831430707]
renderView1.CameraFocalPoint = [-0.052487104146733146, -2.0571900475013227, -9.124931905418922]
renderView1.CameraViewUp = [0.04944978829774686, 0.9119035746907442, -0.40741451729602185]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 5.75018386149976

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [393, 344]
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.CenterOfRotation = [3.3199994008318754, 3.319997731645344, 3.3199989599470427]
renderView2.StereoType = 'Crystal Eyes'
renderView2.CameraPosition = [5.310857905828319, 6.494278787262183, 10.666535831430707]
renderView2.CameraFocalPoint = [-0.052487104146733146, -2.0571900475013227, -9.124931905418922]
renderView2.CameraViewUp = [0.04944978829774686, 0.9119035746907442, -0.40741451729602185]
renderView2.CameraFocalDisk = 1.0
renderView2.CameraParallelScale = 5.75018386149976
renderView2.UseAmbientOcclusion = 1

SetActiveView(None)

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.SplitHorizontal(0, 0.500000)
layout1.AssignView(1, renderView1)
layout1.AssignView(2, renderView2)


# create a new 'PLY Reader'
reader = PLYReader(FileNames=['../Data/sponge.ply'])

# show data from reader
readerDisplay = Show(reader, renderView1)

# trace defaults for the display properties.
readerDisplay.Representation = 'Surface'

# show data from reader
readerDisplay_1 = Show(reader, renderView2)

# trace defaults for the display properties.
readerDisplay_1.Representation = 'Surface'

# link cameras in two views
AddCameraLink(renderView2, renderView1, 'CameraLink1')

SetActiveSource(reader)

