# extract keyframes values from an interactive session
# extract also Python Animation cues
# The script created should be concatenated to an existing script saved from
# the SaveState() menu
#
# written by Jean M. Favre, CSCS
# tested Tue 04 May 2021 08:00:34 PM CEST with Paraview v5.9

filename = '/tmp/keyframes.py'
with open(filename, 'w') as f:
  print("saving animation keyframes script in file: ", filename)
  print("\nscene = GetAnimationScene()", file=f)
  scene = GetAnimationScene()
  if scene.PlayMode == 'Sequence':
    L = scene.NumberOfFrames
  elif scene.PlayMode == 'Snap To TimeSteps':
      L = len(scene.TimeKeeper.TimestepValues)
  else: #'Real Time'
      L=10
      print("scene.Duration = ", scene.Duration, file=f)
  print("scene.NumberOfFrames = ", L, file=f)
  print("scene.PlayMode = ", scene.PlayMode, file=f)
#
# start by scanning if there is a CameraAnimationCue (there is atmost one)
#
  for iq, cue in enumerate(scene.Cues):
    if cue.GetXMLName() == "CameraAnimationCue":
      print("\nCues = GetCameraTrack(view=GetRenderView())\n", file=f)
      Cues = GetCameraTrack(view=GetRenderView())
      print("Cues.Mode = ", Cues.Mode, file=f)
      print("Cues.Interpolation = ", Cues.Interpolation, file=f)
      if Cues.Mode == 'Interpolate Camera':
        for i, kf in enumerate(Cues.KeyFrames):
          print(format("k%02d = CameraKeyFrame()" % i), file=f)
          print(format("k%02d.KeyTime = " % i), kf.KeyTime, file=f)
          print(format("k%02d.Position = " % i), kf.Position, file=f)
          print(format("k%02d.FocalPoint = " % i), kf.FocalPoint, file=f)
          print(format("k%02d.ViewUp = " % i), kf.ViewUp, file=f)
          print(format("k%02d.ViewAngle = " % i), kf.ViewAngle, file=f)
          print(format("k%02d.ParallelScale = " % i), kf.ParallelScale, file=f)
          print("", file=f)

      else:
        if Cues.Mode == 'Path-based':
          for i, kf in enumerate(Cues.KeyFrames):
            print(format("k%02d = CameraKeyFrame()" % i), file=f)
            print(format("k%02d.KeyTime = " % i), kf.KeyTime, file=f)
            print(format("k%02d.ViewUp = " % i), kf.ViewUp, file=f)
            print(format("k%02d.ClosedFocalPath = " % i), kf.ClosedFocalPath, file=f)
            print(format("k%02d.FocalPathPoints = [" % i), file=f)
            num_lines = len(kf.FocalPathPoints)//3
            for start in range(0, num_lines):
              items = kf.FocalPathPoints[start*3:(start+1)*3]
              for item in items:
                print(item,end=', ', file=f)
              print("", file=f)
            print("]", file=f)
            print(format("k%02d.ClosedPositionPath = " % i), kf.ClosedPositionPath, file=f)
            print(format("k%02d.PositionPathPoints = [" % i), file=f)
            num_lines = len(kf.PositionPathPoints)//3
            for start in range(0, num_lines):
              items = kf.PositionPathPoints[start*3:(start+1)*3]
              for item in items:
                print(item,end=', ', file=f)
              print("", file=f)
            print("]", file=f)

      print("Cues.KeyFrames = [", file=f)
      for i, kf in enumerate(Cues.KeyFrames):
        print(format("k%02d," % i), file=f)
      print("]", file=f)
#
# second, start scanning for all possible PythonAnimationCues
#
  for iq, cue in enumerate(scene.Cues):
    if cue.GetXMLName() == "PythonAnimationCue":
      print("\n# Adding now a PythonAnimationCue()\n", file=f)
      print(format("pyQ%02d = PythonAnimationCue()" % iq), file=f)
      print(format("pyQ%02d.Script=\"\"\"" % iq) + cue.Script + "\"\"\"", file=f)
      print(format("pyQ%02d.StartTime=" % iq) + str(cue.StartTime), file=f)
      print(format("pyQ%02d.EndTime=" % iq) + str(cue.EndTime), file=f)
      print(format("scene.Cues.append(pyQ%02d)" % iq), file=f)

#
# third, start scanning for all other KeyFrameAnimationCues
#
  gs = GetSources() # will be used to find the associated proxy with a given cue
  for iq, cue in enumerate(scene.Cues):
    myprox = ''
    if cue.GetXMLName() == "KeyFrameAnimationCue":
      for k, v, in gs.items():
        if v == cue.AnimatedProxy:
          myprox = k[0]
      if myprox:
        print("\n# Adding now a KeyFrameAnimationCue()\n", file=f)
        print(format("kfaQ%02d = KeyFrameAnimationCue()" % iq), file=f)
        # smtrace.py has a hint in get_varname() that the first letter should be lower-case
        print(format("kfaQ%02d.AnimatedProxy=" % iq) + myprox[0].lower() + myprox[1:], file=f)
        print(format("kfaQ%02d.AnimatedPropertyName=\"" % iq) + cue.AnimatedPropertyName+"\"", file=f)
        print(format("kfaQ%02d.StartTime=" % iq) + str(cue.StartTime), file=f)
        print(format("kfaQ%02d.EndTime=" % iq) + str(cue.EndTime), file=f)
 
        for i, kf in enumerate(cue.KeyFrames):
          print(format("ckf%02d = CompositeKeyFrame()" % i), file=f)
          print(format("ckf%02d.Base = " % i), kf.Base, file=f)
          print(format("ckf%02d.EndPower = " % i), kf.EndPower, file=f)
          print(format("ckf%02d.Frequency = " % i), kf.Frequency, file=f)
          print(format("ckf%02d.KeyTime = " % i), kf.KeyTime, file=f)
          print(format("ckf%02d.KeyValues = " % i), kf.KeyValues, file=f)
          print(format("ckf%02d.Offset = " % i), kf.Offset, file=f)
          print(format("ckf%02d.Phase = " % i), kf.Phase, file=f)
          print(format("ckf%02d.StartPower = " % i), kf.StartPower, file=f)
          print(format("ckf%02d.Interpolation = " % i), kf.Interpolation, file=f)
        print(format("kfaQ%02d.KeyFrames" % iq) + " = [", file=f)
        for i, kf in enumerate(cue.KeyFrames):
          print(format("ckf%02d," % i), file=f)
        print("]", file=f)
        print(format("scene.Cues.append(kfaQ%02d)" % iq), file=f)
      else:
        """
        my slice ActiveSource has ListProperties() which itself has ListProperties() matching 'Offset'
        """
        print("\nWARNING: skipping cue ", cue.AnimatedProxy)
        print(format("track%02d = GetAnimationTrack(\"...\", 0, \"...\")" % iq), file=f)
f.close()
