{



gROOT->ProcessLine(".L tdrstyle.C");
setTDRStyle();
gStyle->SetErrorX(0.5);

gStyle->SetPadLeftMargin(0.15);
gStyle->SetPadRightMargin(0.10);
gStyle->SetTitleOffset(1.0,"Y");






//----------------------------------------------------------------------------------------------------------------------------





gROOT->ProcessLine(".L DrawIteration.C");




gROOT->ProcessLine("DrawIteration drawIteration1(14, true)");

//drawIteration1.outputDirectory("$CMSSW_BASE/src/ApeEstimator/ApeEstimator/hists/comparison/");  // default

drawIteration1.addInputFile("/afs/cern.ch/work/c/cschomak/APEPhase1/CMSSW_9_0_0/src/Alignment/APEEstimation/hists/workingArea_startup/iter14/allData_iterationApe.root","Startup Misalignment");
drawIteration1.addInputFile("/afs/cern.ch/work/c/cschomak/APEPhase1/CMSSW_8_1_0/src/Alignment/APEEstimation/hists/workingArea_RealignStep1/iter14/allData_iterationApe.root","Realign step1");
drawIteration1.addInputFile("/afs/cern.ch/work/c/cschomak/APEPhase1/CMSSW_8_1_0/src/Alignment/APEEstimation/hists/workingArea_RealignStep2/iter14/allData_iterationApe.root","Realign step2");
drawIteration1.addInputFile("/afs/cern.ch/work/c/cschomak/APEPhase1/CMSSW_9_0_0/src/Alignment/APEEstimation/hists/workingArea_CRUZET_0p5M/iter14/allData_iterationApe.root","CRUZET 0.5 M");
//drawIteration1.addInputFile("","");

//drawIteration1.addCmsText("CMS Preliminary");
drawIteration1.drawResult();

gROOT->ProcessLine(".q");


}
