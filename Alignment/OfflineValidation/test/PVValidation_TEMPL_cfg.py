import FWCore.ParameterSet.Config as cms
import sys
 
isDA = ISDATEMPLATE
isMC = ISMCTEMPLATE
allFromGT = ALLFROMGTTEMPLATE
applyBows = APPLYBOWSTEMPLATE
applyExtraConditions = EXTRACONDTEMPLATE

process = cms.Process("Demo") 

###################################################################
# Event source and run selection
###################################################################
# readFiles = cms.untracked.vstring()
# readFiles.extend(FILESOURCETEMPLATE)
# process.source = cms.Source("PoolSource",
#                             fileNames = readFiles ,
#                             duplicateCheckMode = cms.untracked.string('checkAllFilesOpened')
#                             )

process.load("Alignment.OfflineValidation.DATASETTEMPLATE");
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

runboundary = RUNBOUNDARYTEMPLATE
process.source.firstRun = cms.untracked.uint32(int(runboundary))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(MAXEVENTSTEMPLATE) )

###################################################################
# JSON Filtering
###################################################################
if isMC:
     print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: This is Simulation!"
     runboundary = 1
else:
     print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: This is DATA!"

     ## working recipe for CMSSW_4_X_Y
     ##import PhysicsTools.PythonAnalysis.LumiList as LumiList
     #myLumis = LumiList.LumiList(filename = 'LUMILISTTEMPLATE').getCMSSWString().split(',')
     #process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()
     #process.source.lumisToProcess.extend(myLumis)

     ## working recipe for CMSSW_5_X_Y
     import FWCore.PythonUtilities.LumiList as LumiList
     process.source.lumisToProcess = LumiList.LumiList(filename ='LUMILISTTEMPLATE').getVLuminosityBlockRange()

###################################################################
# Messages
###################################################################
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

####################################################################
# Produce the Transient Track Record in the event
####################################################################
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

####################################################################
# Get the Magnetic Field
####################################################################
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

###################################################################
# Standard loads
###################################################################
#from Geometry.CommonDetUnit.globalTrackingGeometry_cfi import *
# this line works in 44X, deprecated in 53X
#process.load("Configuration.StandardSequences.GeometryIdeal_cff")
#process.load("Configuration.Geometry.GeometryIdeal_cff")
#process.load("Geometry.CommonDetUnit.globalTrackingGeometry_cfi")
#process.load("Geometry.TrackerGeometryBuilder.trackerGeometry_cfi")
process.load("Configuration.Geometry.GeometryRecoDB_cff")

####################################################################
# Get the BeamSpot
####################################################################
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cff")

####################################################################
# Get the GlogalTag
####################################################################
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = "GLOBALTAGTEMPLATE"  # take your favourite

if allFromGT:
     print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: All is taken from GT"
else:
     ####################################################################
     # Get Alignment constants
     ####################################################################
     from CondCore.DBCommon.CondDBSetup_cfi import *
     process.trackerAlignment = cms.ESSource("PoolDBESSource",CondDBSetup,
                                             connect = cms.string('ALIGNOBJTEMPLATE'),
                                             timetype = cms.string("runnumber"),
                                             toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentRcd'),
                                                                        tag = cms.string('GEOMTAGTEMPLATE')
                                                                        )
                                                               )
                                             )
     process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource", "trackerAlignment")

     ####################################################################
     # Get APE
     ####################################################################
     process.setAPE = cms.ESSource("PoolDBESSource",CondDBSetup,
                                   connect = cms.string('APEOBJTEMPLATE'),
                                   timetype = cms.string("runnumber"),
                                   toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorExtendedRcd'),
                                                              tag = cms.string('ERRORTAGTEMPLATE')
                                                              )
                                                     )
                                   )
     process.es_prefer_setAPE = cms.ESPrefer("PoolDBESSource", "setAPE")

     ####################################################################
     # Kinks and Bows (optional)
     ####################################################################
     if applyBows:
          print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: Applying TrackerSurfaceDeformations!"
          process.trackerBows = cms.ESSource("PoolDBESSource",CondDBSetup,
                                             connect = cms.string('BOWSOBJECTTEMPLATE'),
                                             toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerSurfaceDeformationRcd'),
                                                                        tag = cms.string('BOWSTAGTEMPLATE')
                                                                        )
                                                               )
                                             )
          process.es_prefer_Bows = cms.ESPrefer("PoolDBESSource", "trackerBows")
     else:
          print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: MultiPVValidation: Not applying TrackerSurfaceDeformations!"

          ####################################################################
          # Extra corrections not included in the GT
          ####################################################################
          if applyExtraConditions:
               print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: Applying extra calibration constants!"

               ### this is just an example 
               import CalibTracker.Configuration.Common.PoolDBESSource_cfi
               process.SiPixelTemplates = cms.ESSource("PoolDBESSource",CondDBSetup,
                                                       connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
                                                       timetype = cms.string("runnumber"),
                                                       toGet = cms.VPSet(cms.PSet(record = cms.string('SiPixelTemplateDBObjectRcd'),
                                                                                  tag = cms.string('SiPixelTemplateDBObject_38T_v6_offline')
                                                                                  )
                                                                         )
                                                       )
               process.es_prefer_SiPixelTemplates = cms.ESPrefer("PoolDBESSource", "SiPixelTemplates") 

               ## END OF EXTRA CONDITIONS
               
          else:
               print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: Not applying extra calibration constants!"
               
     
####################################################################
# Load and Configure event selection
####################################################################
process.primaryVertexFilter = cms.EDFilter("VertexSelector",
                                           src = cms.InputTag("VERTEXTYPETEMPLATE"),
                                           cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"),
                                           filter = cms.bool(True)
                                           )

process.noscraping = cms.EDFilter("FilterOutScraping",
                                  applyfilter = cms.untracked.bool(True),
                                  src =  cms.untracked.InputTag("TRACKTYPETEMPLATE"),
                                  debugOn = cms.untracked.bool(False),
                                  numtrack = cms.untracked.uint32(10),
                                  thresh = cms.untracked.double(0.25)
                                  )

process.noslowpt = cms.EDFilter("FilterOutLowPt",
                                applyfilter = cms.untracked.bool(True),
                                src =  cms.untracked.InputTag("TRACKTYPETEMPLATE"),
                                debugOn = cms.untracked.bool(False),
                                numtrack = cms.untracked.uint32(0),
                                thresh = cms.untracked.int32(1),
                                ptmin  = cms.untracked.double(PTCUTTEMPLATE),
                                runControl = cms.untracked.bool(RUNCONTROLTEMPLATE),
                                runControlNumber = cms.untracked.uint32(int(runboundary))
                                )

#process.goodvertexSkim = cms.Sequence(process.primaryVertexFilter + process.noscraping + process.noslowpt)
if isMC:
     process.goodvertexSkim = cms.Sequence(process.noscraping)
else:
     #process.goodvertexSkim = cms.Sequence(process.primaryVertexFilter + process.noscraping)
     process.goodvertexSkim = cms.Sequence(process.primaryVertexFilter + process.noscraping + process.noslowpt)

####################################################################
# Load and Configure Measurement Tracker Event
####################################################################
process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi") 
process.MeasurementTrackerEvent.pixelClusterProducer = 'ALCARECOTkAlMinBias'
process.MeasurementTrackerEvent.stripClusterProducer = 'ALCARECOTkAlMinBias'
process.MeasurementTrackerEvent.inactivePixelDetectorLabels = cms.VInputTag()
process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag()

####################################################################
# Load and Configure TrackRefitter
####################################################################
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
import RecoTracker.TrackProducer.TrackRefitters_cff
process.TrackRefitter = RecoTracker.TrackProducer.TrackRefitter_cfi.TrackRefitter.clone()
process.TrackRefitter.src = "TRACKTYPETEMPLATE"
process.TrackRefitter.TrajectoryInEvent = True
process.TrackRefitter.TTRHBuilder = "WithAngleAndTemplate"

####################################################################
# Output file
####################################################################
process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string("OUTFILETEMPLATE")
                                  )                                    

####################################################################
# Deterministic annealing clustering
####################################################################
if isDA:
     print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: Running DA Algorithm!"
     process.PVValidation = cms.EDAnalyzer("PrimaryVertexValidation",
                                           TrackCollectionTag = cms.InputTag("TrackRefitter"),
                                           VertexCollectionTag = cms.InputTag("VERTEXTYPETEMPLATE"),  
                                           Debug = cms.bool(False),
                                           storeNtuple = cms.bool(False),
                                           useTracksFromRecoVtx = cms.bool(False),
                                           isLightNtuple = cms.bool(True),
                                           askFirstLayerHit = cms.bool(False),
                                           probePt = cms.untracked.double(PTCUTTEMPLATE),
                                           runControl = cms.untracked.bool(RUNCONTROLTEMPLATE),
                                           runControlNumber = cms.untracked.uint32(int(runboundary)),
                                           
                                           TkFilterParameters = cms.PSet(algorithm=cms.string('filter'),                           
                                                                         maxNormalizedChi2 = cms.double(5.0),                        # chi2ndof < 5                  
                                                                         minPixelLayersWithHits = cms.int32(2),                      # PX hits > 2                       
                                                                         minSiliconLayersWithHits = cms.int32(5),                    # TK hits > 5  
                                                                         maxD0Significance = cms.double(5.0),                        # fake cut (requiring 1 PXB hit)     
                                                                         minPt = cms.double(0.0),                                    # better for softish events                        
                                                                         trackQuality = cms.string("any")
                                                                         ),
                                           
                                           TkClusParameters=cms.PSet(algorithm=cms.string('DA'),
                                                                     TkDAClusParameters = cms.PSet(coolingFactor = cms.double(0.8),  # moderate annealing speed
                                                                                                   Tmin = cms.double(4.),            # end of annealing
                                                                                                   vertexSize = cms.double(0.05),    # ~ resolution / sqrt(Tmin)
                                                                                                   d0CutOff = cms.double(3.),        # downweight high IP tracks
                                                                                                   dzCutOff = cms.double(4.)         # outlier rejection after freeze-out (T<Tmin)
                                                                                                   )
                                                                     )
                                           )

####################################################################
# GAP clustering
####################################################################
else:
     print ">>>>>>>>>> testPVValidation_cfg.py: msg%-i: Running GAP Algorithm!"
     process.PVValidation = cms.EDAnalyzer("PrimaryVertexValidation",
                                           TrackCollectionTag = cms.InputTag("TrackRefitter"),
                                           VertexCollectionTag = cms.InputTag("VERTEXTYPETEMPLATE"), 
                                           Debug = cms.bool(False),
                                           isLightNtuple = cms.bool(True),
                                           storeNtuple = cms.bool(False),
                                           useTracksFromRecoVtx = cms.bool(False),
                                           askFirstLayerHit = cms.bool(False),
                                           probePt = cms.untracked.double(PTCUTTEMPLATE),
                                           runControl = cms.untracked.bool(RUNCONTROLTEMPLATE),
                                           runControlNumber = cms.untracked.uint32(int(runboundary)),
                                           
                                           TkFilterParameters = cms.PSet(algorithm=cms.string('filter'),                             
                                                                         maxNormalizedChi2 = cms.double(5.0),                        # chi2ndof < 20                  
                                                                         minPixelLayersWithHits=cms.int32(2),                        # PX hits > 2                   
                                                                         minSiliconLayersWithHits = cms.int32(5),                    # TK hits > 5                   
                                                                         maxD0Significance = cms.double(5.0),                        # fake cut (requiring 1 PXB hit)
                                                                         minPt = cms.double(0.0),                                    # better for softish events     
                                                                         trackQuality = cms.string("any")
                                                                         ),
                                        
                                           TkClusParameters = cms.PSet(algorithm   = cms.string('gap'),
                                                                       TkGapClusParameters = cms.PSet(zSeparation = cms.double(0.2)  # 0.2 cm max separation betw. clusters
                                                                                                      ) 
                                                                       )
                                           )

####################################################################
# Path
####################################################################
process.p = cms.Path(process.goodvertexSkim*
                     process.offlineBeamSpot*
                     process.MeasurementTrackerEvent*
                     process.TrackRefitter*
                     process.PVValidation)
