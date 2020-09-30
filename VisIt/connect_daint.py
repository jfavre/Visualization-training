# Written by Jean M Favre, CSCS
# Test passed with v3.1.2 Wed 30 Sep 2020 05:12:52 PM CEST

# Run from your local desktop with version 3.1.2
# syntax:
#         visit -cli -s connect_daint.py
#
# on daint, get the EBROOTVISIT with "module load daint-mc Visit; echo $EBROOTVISIT"
# This is the install_dir variable below

install_dir = "/apps/daint/UES/jenkins/7.0.UP02/mc/easybuild/software/Visit/3.1.2-CrayGNU-20.08"

args = ("-sshtunneling", "-np", "8", "-nn", "1", # 1 node and 8 tasks per node
        "-l", "srun",
        "-dir", install_dir,
        "-t", "00:05:00", # allocate for 5 minutes
        "-la", # launcher option follow
        "--cpu_bind=sockets -C mc -p debug")

# copy /apps/daint/UES/6.0.UP02/VisIt/host_daint.xml  $HOME/.visit/hosts/host_daint.xml on your desktop
# host name must match the one in $HOME/.visit/hosts/host_daint.xml

host = "daint101.cscs.ch"

OpenComputeEngine(host, args)

OpenDatabase(host+":" + install_dir + "/data/multi_ucd3d.silo")
DefineScalarExpression("procid", "procid(mesh1)")
AddPlot("Pseudocolor", "procid", 1, 0)

View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.264402, 0.544304, 0.796131)
View3DAtts.focus = (0, 2.5, 10)
View3DAtts.viewUp = (0.256419, 0.835472, -0.486042)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 11.4564
View3DAtts.nearPlane = -22.9129
View3DAtts.farPlane = 22.9129
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (0, 2.5, 10)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
SetView3D(View3DAtts)

N=1024
ResizeWindow(1, N, N)

save_win_atts = SaveWindowAttributes()
save_win_atts.fileName = "/tmp" + "/daint_multi_ucd3d."
save_win_atts.resConstraint = save_win_atts.NoConstraint
save_win_atts.width = N
save_win_atts.height = N
save_win_atts.screenCapture = 0
SetSaveWindowAttributes(save_win_atts)

DrawPlots()

SaveWindow()

OpenGUI()

