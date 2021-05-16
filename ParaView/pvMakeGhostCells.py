# state file generated using paraview version 5.9.1
# Left view holds an isocontour where Normals were not computed. Thus,
# no ghost-cells were needed.
# Right View holds an isocontour with Normals=ON
# ghosts cells were computed. They can be viewed, except that by default
# ParaView does not show them. We use a trick whereby a Programmable Filter
# makes a copy of the structure (The extracted ghost cells) without data,
# and it can be viewed on the screen. Go to the right view, hide the "Contour"
# object and make the "GhostCells" object visible
#
# Tested Wed 05 May 2021 09:26:55 PM CEST

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()



RightView = CreateView('RenderView')
RightView.AxesGrid = 'GridAxes3DActor'
RightView.CenterOfRotation = [35.15753173828125, 31.602006912231445, 33.624698638916016]
RightView.CameraPosition = [306.28275083455515, 175.10668474182037, 280.49530142845566]
RightView.CameraFocalPoint = [151.95041963700476, 93.4196637372208, 139.96940066698758]
RightView.CameraViewUp = [-0.24011760645342517, 0.9303538776161575, -0.27710142091959394]
RightView.CameraFocalDisk = 1.0
RightView.CameraParallelScale = 58.011716380114954


# Create a new 'Render View'
LeftView = CreateView('RenderView')
LeftView.AxesGrid = 'GridAxes3DActor'
LeftView.CenterOfRotation = [35.15753173828125, 31.602006912231445, 33.624698638916016]
LeftView.CameraPosition = [306.28275083455515, 175.10668474182037, 280.49530142845566]
LeftView.CameraFocalPoint = [151.95041963700476, 93.4196637372208, 139.96940066698758]
LeftView.CameraViewUp = [-0.24011760645342517, 0.9303538776161575, -0.27710142091959394]
LeftView.CameraFocalDisk = 1.0
LeftView.CameraParallelScale = 58.011716380114954

SetActiveView(LeftView)


wavelet2 = Wavelet(registrationName='Wavelet2')
wavelet2.WholeExtent = [0, 99, 0, 99, 0, 99]
wavelet2.UpdatePipeline()

# create a new 'Contour'
contour2 = Contour(registrationName='Contour2', Input=wavelet2)
contour2.ContourBy = ['POINTS', 'RTData']
contour2.Isosurfaces = [100.0]
contour2.ComputeNormals = 0
contour2.PointMergeMethod = 'Uniform Binning'
contour2.UpdatePipeline()


wavelet2Display = Show(wavelet2, LeftView, 'UniformGridRepresentation')
wavelet2Display.Representation = 'Outline'
wavelet2Display.ColorArrayName = ['POINTS', '']
wavelet2Display.ScaleTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]
wavelet2Display.OpacityTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]

# get color transfer function/color map for 'vtkProcessId'
vtkProcessIdLUT = GetColorTransferFunction('vtkProcessId')
vtkProcessIdLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 1.5, 0.865003, 0.865003, 0.865003, 3.0, 0.705882, 0.0156863, 0.14902]
vtkProcessIdLUT.ScalarRangeInitialized = 1.0

# show data from contour2
contour2Display = Show(contour2, LeftView, 'GeometryRepresentation')
contour2Display.Representation = 'Surface'
contour2Display.ColorArrayName = ['POINTS', 'vtkProcessId']
contour2Display.LookupTable = vtkProcessIdLUT
contour2Display.ScaleTransferFunction.Points = [120.97290802001953, 0.0, 0.5, 0.0, 120.98853302001953, 1.0, 0.5, 0.0]
contour2Display.OpacityTransferFunction.Points = [120.97290802001953, 0.0, 0.5, 0.0, 120.98853302001953, 1.0, 0.5, 0.0]


# ----------------------------------------------------------------
# setup the visualization in view 'RightView'
# ----------------------------------------------------------------

wavelet1 = Wavelet(registrationName='Wavelet1')
wavelet1.WholeExtent = [0, 99, 0, 99, 0, 99]

contour1 = Contour(registrationName='Contour', Input=wavelet1)
contour1.ContourBy = ['POINTS', 'RTData']
contour1.ComputeNormals = 1
contour1.Isosurfaces = [100.0]
contour1.PointMergeMethod = 'Uniform Binning'

SetActiveSource(contour1)
selection=SelectCells()
selection.QueryString="vtkGhostType == 1"
selection.FieldType = 'CELL'
selection.UpdatePipelineInformation()
extractSelection1 = ExtractSelection(Selection=selection, registrationName='ExtractSelection1', Input=contour1)
extractSelection1.UpdatePipeline()

GhostCells = ProgrammableFilter(registrationName='GhostCells', Input=extractSelection1)
GhostCells.OutputDataSetType = 'Same as Input'
GhostCells.Script = """\"\"\"
By default, the input structure, without data, is copied to the output
\"\"\""""


# show data from contour1
contour1Display = Show(contour1, RightView, 'GeometryRepresentation')
contour1Display.Representation = 'Surface'
contour1Display.ColorArrayName = ['POINTS', 'vtkProcessId']
contour1Display.LookupTable = vtkProcessIdLUT

ghost_cells = Show(GhostCells, RightView, 'GeometryRepresentation')
ghost_cells.Representation = 'Surface'

# show data from wavelet1
wavelet1Display = Show(wavelet1, RightView, 'UniformGridRepresentation')
wavelet1Display.Representation = 'Outline'
wavelet1Display.ColorArrayName = ['POINTS', '']
wavelet1Display.ScaleTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]
wavelet1Display.OpacityTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]

# setup the color legend parameters for each legend in this view

# get color legend/bar for vtkProcessIdLUT in view RightView
vtkProcessIdLUTColorBar = GetScalarBar(vtkProcessIdLUT, RightView)
vtkProcessIdLUTColorBar.Title = 'vtkProcessId'
vtkProcessIdLUTColorBar.ComponentTitle = ''

# set color bar visibility
vtkProcessIdLUTColorBar.Visibility = 1

# show color legend
contour1Display.SetScalarBarVisibility(RightView, True)

SetActiveView(None)

layout1 = CreateLayout(name='My layout')
layout1.SplitHorizontal(0, 0.500000)
layout1.AssignView(1, LeftView)
layout1.AssignView(2, RightView)
SetActiveView(RightView)
Hide(GhostCells)
AddCameraLink(LeftView, RightView, 'CameraLink0')

