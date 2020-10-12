# Demonstration script for paraview version 5.8
# written by Jean M. Favre, Swiss National Supercomputing Centre
# tested Sat 10 Oct 2020 11:46:36 AM CEST

from paraview.simple import *

w = Wavelet()
w.UpdatePipeline()

w2 = PointDatatoCellData(Input=w)
w2.PassPointData = 1
#w2.ProcessAllArrays = 1
w2.UpdatePipeline()

cdi = w2.GetCellDataInformation()
assert cdi.keys()[0] == 'RTData'

SetActiveSource(w2)

selection=SelectPoints()
selection.QueryString="RTData <= 100"
selection.FieldType = 'POINT'
selection.UpdatePipelineInformation()

# create a new 'Extract Selection'
mySelection = ExtractSelection(Input=w2, Selection=selection, guiName="Node Extract")
mySelection.UpdatePipeline()
Show(mySelection)

SetActiveSource(w2)
selection2=SelectCells()
selection2.QueryString="RTData <= 100"
selection2.FieldType = 'CELL'
selection2.UpdatePipelineInformation()

# create a new 'Extract Selection'
mySelection2 = ExtractSelection(Input=w2, Selection=selection2, guiName="Cell Extract")
mySelection2.UpdatePipeline()
Show(mySelection2)

ResetCamera()
