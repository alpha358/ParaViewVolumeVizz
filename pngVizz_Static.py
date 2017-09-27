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


SPACING_SCALE = 15;

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

z_coords = []
for i in img_files:
	z_coords.append(float(i[0:-4]))



# pprint.pprint(img_files)

# ============================ Series Readers =============================
# help(para.simple.JPEGSeriesReader())
reader = paraview.simple.PNGSeriesReader(
                                FileNames = sort_nicely(img_files),
                                ReadAsImageStack = True,
                                DataSpacing = (1,1,SPACING_SCALE)
                            );

# ===================== Initialize a new interactor ======================
# Initialize a new interactor
view = CreateRenderView()
# import vtk
# iren = vtk.vtkRenderWindowInteractor()
# # vtk.vtkInteractorStyleJoystickCamera
# # vtkInteractorStyleTrackball
# iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackball())
# iren.SetRenderWindow(view.GetRenderWindow())
# iren.Initialize()

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


#opacityMap.Points = [1.0, 0.0,     0.5,    0.0,
#                     135,     0.0204,  0.5, 0.0,
#                     255, 1.0,    0.5, 0.0]
					 
opacityMap.Points = [1.0, 0.0, 0.5, 0.0, 140.1351318359375, 0.0625, 0.5, 0.0, 255.0, 1.0, 0.5, 0.0]



# -------------------------------- Camera ---------------------------------
paraview.simple.GetActiveCamera().SetPosition(
    (-2068.648088053665, 5311.560006222404, -311.8683687711676)
)



# --------------------------------- Axes ----------------------------------
renderView = GetActiveView()

# --- Background
renderView.Background = [0.0, 0.0, 0.0];
renderView.ViewSize = [1173, 811];

renderView.OrientationAxesVisibility=1

 # AxesGrid property provides access to the AxesGrid object.
axesGrid = renderView.AxesGrid
 # To toggle visibility of the axes grid,
axesGrid.Visibility = 1


# Data Inflate Bounds
axesGrid.DataBoundsInflateFactor = 0

# Show Grid
axesGrid.ShowGrid = 1

# Axes Labels & Ticks

#axesGrid.ZAxisLabels = z_coords;
#ZAxisUseCustomLabels = 0;

axesGrid.ZTitle = 'Z, mm'
axesGrid.DataScale = [1 , 1 , 1/(max(z_coords) - min(z_coords)) * len(z_coords)*SPACING_SCALE]

# =============================== Save IMG ================================
Render()
paraview.simple.SaveScreenshot(
    "../" + os.path.relpath( os.getcwd(), os.path.dirname(os.getcwd()) ) + ".png",
     viewOrLayout=None,
     ImageResolution = (1173, 811)
)

# ==================== Start the interactor ===============================
Render()
#Interact()
#iren.Start() # start the interactor

