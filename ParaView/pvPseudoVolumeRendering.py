# state file generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()


# Create a new 'Render View'
renderView2 = GetRenderView()
renderView2.AnnotationColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.OrientationAxesLabelColor = [0.0, 0.0, 0.0]
renderView2.OrientationAxesOutlineColor = [0.0, 0.0, 0.0]
renderView2.CenterOfRotation = [8.255000114440918, 0.0, 29.763084411621094]
renderView2.StereoType = 0
renderView2.CameraPosition = [-5.316174866173274, -42.49007940285952, 34.511198447949766]
renderView2.CameraFocalPoint = [8.559078097343445, 0.0, 29.808670043945312]
renderView2.CameraViewUp = [-0.07839654643106674, 0.13491847102077653, 0.9877504683294752]
renderView2.CameraFocalDisk = 1.0
renderView2.CameraParallelScale = 11.898504110287218
renderView2.Background = [107/255]*3


# create a new 'PLOT3D Reader'
pLOT3DReader1 = PLOT3DReader(registrationName='PLOT3DReader1', FileName='../Data/combxyz.bin',
    QFileName=['../Data/combq.bin'],
    FunctionFileName='')
pLOT3DReader1.Functions = ['Scalar - Pressure']

# create a new 'Contour'
contour1 = Contour(registrationName='Contour1', Input=pLOT3DReader1)
contour1.ContourBy = ['POINTS', 'Density']
contour1.Isosurfaces = [0.3]
contour1.PointMergeMethod = 'Uniform Binning'

# ----------------------------------------------------------------
# setup the visualization in view 'renderView2'
# ----------------------------------------------------------------

# show data from pLOT3DReader1
pLOT3DReader1Display = Show(pLOT3DReader1, renderView2, 'StructuredGridRepresentation')

# trace defaults for the display properties.
pLOT3DReader1Display.Representation = 'Outline'
pLOT3DReader1Display.ColorArrayName = ['POINTS', '']
pLOT3DReader1Display.OSPRayScaleArray = 'Density'
pLOT3DReader1Display.OSPRayScaleFunction = 'PiecewiseFunction'
pLOT3DReader1Display.SelectOrientationVectors = 'Momentum'
pLOT3DReader1Display.ScaleFactor = 1.6510000228881836
pLOT3DReader1Display.SelectScaleArray = 'Density'
pLOT3DReader1Display.GlyphType = 'Arrow'
pLOT3DReader1Display.GlyphTableIndexArray = 'Density'
pLOT3DReader1Display.GaussianRadius = 0.08255000114440918
pLOT3DReader1Display.SetScaleArray = ['POINTS', 'Density']
pLOT3DReader1Display.ScaleTransferFunction = 'PiecewiseFunction'
pLOT3DReader1Display.OpacityArray = ['POINTS', 'Density']
pLOT3DReader1Display.OpacityTransferFunction = 'PiecewiseFunction'
pLOT3DReader1Display.DataAxesGrid = 'GridAxesRepresentation'
pLOT3DReader1Display.PolarAxes = 'PolarAxesRepresentation'
pLOT3DReader1Display.ScalarOpacityUnitDistance = 0.6792129301318574

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
pLOT3DReader1Display.ScaleTransferFunction.Points = [0.19781309366226196, 0.0, 0.5, 0.0, 0.710419237613678, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
pLOT3DReader1Display.OpacityTransferFunction.Points = [0.19781309366226196, 0.0, 0.5, 0.0, 0.710419237613678, 1.0, 0.5, 0.0]

# show data from contour1
contour1Display = Show(contour1, renderView2, 'GeometryRepresentation')

# get color transfer function/color map for 'Density'
densityLUT = GetColorTransferFunction('Density')
densityLUT.RGBPoints = [0.19781309366226196, 0.231373, 0.298039, 0.752941, 0.45411616563796997, 0.865003, 0.865003, 0.865003, 0.710419237613678, 0.705882, 0.0156863, 0.14902]
densityLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
contour1Display.Representation = 'Surface'
contour1Display.ColorArrayName = ['POINTS', 'Density']
contour1Display.LookupTable = densityLUT
contour1Display.SelectTCoordArray = 'None'
contour1Display.SelectNormalArray = 'Normals'
contour1Display.SelectTangentArray = 'None'
contour1Display.OSPRayScaleArray = 'Density'
contour1Display.OSPRayScaleFunction = 'PiecewiseFunction'
contour1Display.SelectOrientationVectors = 'Momentum'
contour1Display.ScaleFactor = 1.5885862469673158
contour1Display.SelectScaleArray = 'Density'
contour1Display.GlyphType = 'Arrow'
contour1Display.GlyphTableIndexArray = 'Density'
contour1Display.GaussianRadius = 0.07942931234836578
contour1Display.SetScaleArray = ['POINTS', 'Density']
contour1Display.ScaleTransferFunction = 'PiecewiseFunction'
contour1Display.OpacityArray = ['POINTS', 'Density']
contour1Display.OpacityTransferFunction = 'PiecewiseFunction'
contour1Display.DataAxesGrid = 'GridAxesRepresentation'
contour1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
contour1Display.ScaleTransferFunction.Points = [0.30000001192092896, 0.0, 0.5, 0.0, 0.30006104707717896, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
contour1Display.OpacityTransferFunction.Points = [0.30000001192092896, 0.0, 0.5, 0.0, 0.30006104707717896, 1.0, 0.5, 0.0]

# setup the color legend parameters for each legend in this view

# get color legend/bar for densityLUT in view renderView2
densityLUTColorBar = GetScalarBar(densityLUT, renderView2)
densityLUTColorBar.Title = 'Density'
densityLUTColorBar.ComponentTitle = ''

# set color bar visibility
densityLUTColorBar.Visibility = 1

# show color legend
contour1Display.SetScalarBarVisibility(renderView2, True)

# ----------------------------------------------------------------
# setup the visualization in view 'renderView2'
# ----------------------------------------------------------------

# show data from pLOT3DReader1
pLOT3DReader1Display_1 = Show(pLOT3DReader1, renderView2, 'StructuredGridRepresentation')

# trace defaults for the display properties.
pLOT3DReader1Display_1.Representation = 'Outline'
pLOT3DReader1Display_1.ColorArrayName = ['POINTS', '']
pLOT3DReader1Display_1.OSPRayScaleArray = 'Density'
pLOT3DReader1Display_1.OSPRayScaleFunction = 'PiecewiseFunction'
pLOT3DReader1Display_1.SelectOrientationVectors = 'Momentum'
pLOT3DReader1Display_1.ScaleFactor = 1.6510000228881836
pLOT3DReader1Display_1.SelectScaleArray = 'Density'
pLOT3DReader1Display_1.GlyphType = 'Arrow'
pLOT3DReader1Display_1.GlyphTableIndexArray = 'Density'
pLOT3DReader1Display_1.GaussianRadius = 0.08255000114440918
pLOT3DReader1Display_1.SetScaleArray = ['POINTS', 'Density']
pLOT3DReader1Display_1.ScaleTransferFunction = 'PiecewiseFunction'
pLOT3DReader1Display_1.OpacityArray = ['POINTS', 'Density']
pLOT3DReader1Display_1.OpacityTransferFunction = 'PiecewiseFunction'
pLOT3DReader1Display_1.DataAxesGrid = 'GridAxesRepresentation'
pLOT3DReader1Display_1.PolarAxes = 'PolarAxesRepresentation'
pLOT3DReader1Display_1.ScalarOpacityUnitDistance = 0.6792129301318574

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
pLOT3DReader1Display_1.ScaleTransferFunction.Points = [0.19781309366226196, 0.0, 0.5, 0.0, 0.710419237613678, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
pLOT3DReader1Display_1.OpacityTransferFunction.Points = [0.19781309366226196, 0.0, 0.5, 0.0, 0.710419237613678, 1.0, 0.5, 0.0]

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'Density'
densityPWF = GetOpacityTransferFunction('Density')
densityPWF.Points = [0.19781309366226196, 0.0, 0.5, 0.0, 0.3018876910209656, 0.0, 0.5, 0.0, 0.3547016382217407, 0.59375, 0.5, 0.0, 0.4137290120124817, 0.0, 0.5, 0.0, 0.710419237613678, 0.0, 0.5, 0.0]
densityPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# restore active source
SetActiveSource(pLOT3DReader1)

