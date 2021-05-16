# Written by Jean M. Favre, Swiss National Supercomputing Center
# Tested with paraView v5.9. Wed Apr 21 08:05:54 CEST 2021


import numpy as np
import vtk
from vtk.numpy_interface import algorithms as algs
from vtk.util import numpy_support as vtknp

class vtkStructuredGridFromArrays:
    def __init__(self):
        self.__mesh = vtk.vtkStructuredGrid()
        self.__dims = [-1,-1,-1]

    def SetVCoordinates(self, cArray):
        assert len(cArray.shape) == 1
        self.__mesh.Points = vtknp.numpy_to_vtk(cArray)
        self.__dims[0] = cArray.shape[0]
        
        self.__mesh.SetDimensions(self.__dims)

    def SetCoordinates(self, cArray0, cArray1, cArray2):
        assert len(cArray0.shape) == 3
        assert len(cArray1.shape) == 3
        assert len(cArray2.shape) == 3
        assert cArray2.shape == cArray1.shape
        assert cArray2.shape == cArray0.shape
        points = vtk.vtkPoints()
        self.__mesh.SetPoints(points)
        points.SetData(vtknp.numpy_to_vtk(
           algs.make_vector(cArray0.ravel(), cArray1.ravel(), cArray2.ravel()))
           )
        self.__dims = np.flip(cArray0.shape)
        self.__mesh.SetDimensions(self.__dims)

    def GetDimensions(self):
        self.__dims = self.__mesh.GetDimensions()
        return self.__dims

    def AddArray(self, dArray, name):
        assert dArray.shape[0] == np.prod(self.__dims)
        vtkarr = vtknp.numpy_to_vtk(dArray)
        vtkarr.SetName(name)
        self.__mesh.GetPointData().AddArray(vtkarr)
        if len(dArray.shape) == 1:
          self.__mesh.GetPointData().SetActiveScalars(name)

    def AddCellArray(self, dArray, name):
        assert dArray.shape[0] == np.prod(self.__dims-np.array([1]))
        vtkarr = vtknp.numpy_to_vtk(dArray)
        vtkarr.SetName(name)
        self.__mesh.GetCellData().AddArray(vtkarr)
        if len(dArray.shape) == 1:
          self.__mesh.GetCellData().SetActiveScalars(name)

    def GetOutput(self):
        return self.__mesh

class vtkRectGridFromArrays:
    def __init__(self):
        self.__mesh = vtk.vtkRectilinearGrid()
        self.__dims = [-1,-1,-1]

    def SetCoordinates(self, cArray0, cArray1, cArray2):
        assert len(cArray0.shape) == 1
        self.__mesh.SetXCoordinates(vtknp.numpy_to_vtk(cArray0))
        self.__dims[0] = cArray0.shape[0]
        
        assert len(cArray1.shape) == 1
        self.__mesh.SetYCoordinates(vtknp.numpy_to_vtk(cArray1))
        self.__dims[1] = cArray1.shape[0]

        assert len(cArray2.shape) == 1
        self.__mesh.SetZCoordinates(vtknp.numpy_to_vtk(cArray2))
        self.__dims[2] = cArray2.shape[0]
        
        self.__mesh.SetDimensions(self.__dims)

    def GetDimensions(self):
        return self.__mesh.GetDimensions()

    def AddArray(self, dArray, name):
        assert dArray.shape[0] == np.prod(self.__dims)
        vtkarr = vtknp.numpy_to_vtk(dArray)
        vtkarr.SetName(name)
        self.__mesh.GetPointData().AddArray(vtkarr)
        self.__mesh.GetPointData().SetActiveScalars(name)

    def AddCellArray(self, dArray, name):
        assert dArray.shape[0] == np.prod(self.__dims-np.array([1]))
        vtkarr = vtknp.numpy_to_vtk(dArray)
        vtkarr.SetName(name)
        self.__mesh.GetCellData().AddArray(vtkarr)
        self.__mesh.GetCellData().SetActiveScalars(name)
        
    def GetOutput(self):
        return self.__mesh
###############################################################################
# a very rudimentary Point Cloud
class vtkPointSetFromArrays:
    def __init__(self):
        self.__mesh = vtk.vtkPolyData()
        self.__nnodes = 0
    
    def Make_PolyVertex(self):
      assert self.__nnodes > 0
      mlist = vtk.vtkIdList()
      mlist.SetNumberOfIds(self.__nnodes)
      for ii in range(self.__nnodes):
        mlist.SetId(ii, ii)
      self.__mesh.Allocate(1)
      self.__mesh.InsertNextCell(vtk.VTK_POLY_VERTEX, mlist)

    def SetVCoordinates(self, cArray):
        assert len(cArray.shape) == 2 and cArray.shape[1] == 3
        points = vtk.vtkPoints()
        self.__mesh.SetPoints(points)
        points.SetData(vtknp.numpy_to_vtk(cArray))
        self.__nnodes = cArray.shape[0]
        self.Make_PolyVertex()

    def SetCoordinates(self, cArray0, cArray1, cArray2):
        assert len(cArray0.shape) == 1
        assert len(cArray1.shape) == 1
        assert len(cArray2.shape) == 1
        assert cArray2.shape == cArray1.shape
        assert cArray2.shape == cArray0.shape
        points = vtk.vtkPoints()
        self.__mesh.SetPoints(points)
        points.SetData(vtknp.numpy_to_vtk(
          algs.make_vector(cArray0, cArray1, cArray2))
          )
        self.__nnodes = cArray0.shape[0]
        self.Make_PolyVertex()

    def AddArray(self, dArray, name):
        assert dArray.shape[0] == self.__nnodes
        vtkarr = vtknp.numpy_to_vtk(dArray)
        vtkarr.SetName(name)
        self.__mesh.GetPointData().AddArray(vtkarr)
        if len(dArray.shape) == 1:
          self.__mesh.GetPointData().SetActiveScalars(name)

    def GetOutput(self):
        return self.__mesh
###############################################################################
