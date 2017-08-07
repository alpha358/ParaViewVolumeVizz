# ============================ Importing stuff ============================
from paraview.simple import *
import os
import sys
import fileinput
import string
# import paraview
import glob

import pprint
import re

# =========================== Useful Functions ============================
def sort_nicely( l ):
	""" Sort the given list in the way that humans expect.
	"""
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )
    return l;

# ============================ Get File names =============================
img_files = glob.glob("*.png");

# pprint.pprint(img_files)

# ============================ Series Readers =============================
# help(para.simple.JPEGSeriesReader())
reader = paraview.simple.PNGSeriesReader(
                                FileNames = sort_nicely(img_files),
                                ReadAsImageStack = True,
                                DataSpacing = (1,1,40)
                            );

# ===================== Initialize a new interactor ======================
# Initialize a new interactor
view = CreateRenderView()
import vtk
iren = vtk.vtkRenderWindowInteractor()
# vtk.vtkInteractorStyleJoystickCamera
# vtkInteractorStyleTrackball
iren.SetInteractorStyle(vtk.vtkInteractorStyleJoystickCamera())
iren.SetRenderWindow(view.GetRenderWindow())
iren.Initialize()

# ================================= Show ==================================
display = Show(reader)
SetDisplayProperties(Representation ="Volume")
display.RescaleTransferFunctionToDataRange(True)
ResetCamera()
ColorBy(display , "PNGImage")

# ------------------------------- Color Map -------------------------------
colorMap = GetColorTransferFunction('PNGImage')
#colorMap.RGBPoints = [0.025500000000000005, 1.0, 1.0, 1.0, 43.37116500000003, 0.0, 0.0, 1.0, 86.71683000000006, 0.0, 1.0, 1.0, 127.51275000000008, 0.0, 1.0, 0.0, 170.85841500000012, 1.0, 1.0, 0.0, 214.20408000000015, 1.0, 0.0, 0.0, 255.00000000000017, 0.878431372549, 0.0, 1.0]

# ------------------------------- ColorBar --------------------------------
# source = GetActiveSource()
# view = GetActiveView()
#
# display_p = GetDisplayProperties(source , view)
# display_p.SetScalarBarVisibility(view , True)
# print dir(display_p)
# y.SetScalarBarVisibility(True)


# ------------------------------ Opacity Map ------------------------------
# Similarly, for opacity map. The value here is
# a flattened list of (data-value, opacity, mid-point, sharpness)
opacityMap = GetOpacityTransferFunction('PNGImage')


opacityMap.Points = [1.0, 0.0,     0.5,    0.0,
                     135,     0.0204,  0.5, 0.0,
                     255, 1.0,    0.5, 0.0]

Render()
iren.Start() # start the interactor

# -------------------------------- Camera ---------------------------------
paraview.simple.GetActiveCamera().SetPosition(
    (-3246.8811397036384, 3140.7476618452392, -2217.6731165778656)
)

# --------------------------------- Axes ----------------------------------
renderView = GetActiveView()
renderView.OrientationAxesVisibility=0

 # AxesGrid property provides access to the AxesGrid object.
axesGrid = renderView.AxesGrid
 # To toggle visibility of the axes grid,
axesGrid.Visibility = 1



# =============================== Save IMG ================================

paraview.simple.SaveScreenshot(
    "../" + os.path.relpath( os.getcwd(), os.path.dirname(os.getcwd()) ) + ".png",
     viewOrLayout=None,
     ImageResolution = (800, 800)
)
