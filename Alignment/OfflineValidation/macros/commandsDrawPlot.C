{
gROOT->SetStyle("Plain");
gROOT->ForceStyle();

gROOT->ProcessLine(".L FitPVResiduals.C");


FitPVResiduals("PVValidation_test_mp1834.root=mp1834, PVValidation_test_mp1834_Connor.root=mp1834_Connor");

gROOT->ProcessLine(".q");



}






