from paraview.simple import *
import vtk;


# Create a view
view = CreateRenderView()

# Initialize a new interactor

iren = vtk.vtkRenderWindowInteractor()
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackball())
iren.SetRenderWindow(view.GetRenderWindow())
iren.Initialize()

# Build pipeline
Sphere()
Show()
Render()

# Start interaction
iren.Start()
