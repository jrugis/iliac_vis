#!/usr/bin/python

import numpy as np
import random as rd
from pyevtk.hl import pointsToVTK

# elements  3840?
nodes = 33159

type = "stenosis"  # stenosis, normal
pdir = "output/iliac3840/XX/0.5/quadratic/RCR/"
name = "TimeStep3D_ZZ.partYY.exnode"
parts = 32

print "read opencmiss data files"

xyz = np.empty((nodes,3), dtype=np.float)
for k in range(101):
  fname = name.replace("ZZ",str(20*k))  
  fxyz = np.empty((nodes,4), dtype=np.float)
  vm = np.empty((nodes,1), dtype=np.float)
  for i in range(parts):
    f1 = open(pdir.replace("XX",type)+fname.replace("YY",str(i)),'r')
    for line in f1: 
      l = line.split()
      if(l[0] == "Node:"):
        nnum = int(l[1]) - 1 # index from zero
        if k==0:
          r = 0.0*(rd.random()-0.5)
          xyz[nnum, 0] = float(f1.next())+r
          r = 0.8*(rd.random()-0.5)
          xyz[nnum, 1] = float(f1.next())+r
          r = 0.0*(rd.random()-0.5)
          xyz[nnum, 2] = float(f1.next())+r
        else:
          for j in range(3): 
            f1.next()
        for j in range(2): 
          f1.next()
        for j in range(4):
          fxyz[nnum, j] = float(f1.next())
        vm[nnum,0] = np.sqrt(fxyz[nnum,0]**2+fxyz[nnum,1]**2+fxyz[nnum,2]**2)
    f1.close()

  print 20*k
  #print "write vtk data file"
  d = {}
  d["vel"] = (fxyz[:,0],fxyz[:,1],fxyz[:,2])
  d["x"] = fxyz[:,0]
  d["y"] = fxyz[:,1]
  d["z"] = fxyz[:,2]
  #d["a"] = fxyz[:,3]
  d["v"] = vm[:,0]
  pointsToVTK("sequenceY/"+type+str(20*k), xyz[:,0], xyz[:,1], xyz[:,2], d)


