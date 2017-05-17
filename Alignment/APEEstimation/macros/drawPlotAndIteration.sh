#!/bin/bash



dirbase="$CMSSW_BASE/src/Alignment/APEEstimation"

mkdir $dirbase/hists/workingArea_startup/iter0/plots/
mkdir $dirbase/hists/workingArea_startup/iter14/plots/
mkdir $dirbase/hists/workingArea_startup/iter15/plots/

root -l -b $dirbase/macros/commandsDrawPlot.C
#root -l -b $dirbase/macros/commandsDrawPlot_thesis.C

#~ root -l -b $dirbase/macros/commandsDrawIteration.C




