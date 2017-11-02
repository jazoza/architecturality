from twython import Twython
from auth import TwitterAuthProfiles
import pickle

#Twython AUTHENTICATE (Oauth2)
#Obtain an OAuth 2 Access Token
twitter = Twython(TwitterAuthProfiles.consumer_key, TwitterAuthProfiles.consumer_secret, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
#Use the Access Token
twitter = Twython(TwitterAuthProfiles.consumer_key, access_token=ACCESS_TOKEN)

BIM_list=['@AutodeskRevit', '@autodesk', '@Vectorworks', '@BIM360', '@DynamoBIM', '@autodesku', '@Navisworks', '@davewlight', '@ElrondBurrell', '@NivenArchitects', '@MistresDorkness', '@cadaddict', '@randydeutsch', '@bim_OTG', '@BIM4Struc', '@BIMgcs', '@AutodeskAEC', '@BIMbuilder', '@BentleySystems', '@wmdarchitecture', '@UNIFILabs', '@davidfano', '@TugaBIM', '@TheBIMHub', '@JayZallan', '@topcadexperts', '@AutoCAD', '@designalyze', '@amyonymous', '@Lynn_Allen', '@EEPaul', '@mcc_une', '@AECFactory', '@ColinMcCrone', '@MattBeNimble', '@VMichl', '@osbim', '@BimChannel', '@BIMIntelligence', '@TheB1M', '@Hilti_BIM', '@SimonBIM', '@BIM4M2', '@BIMStrategy', '@bimpages', '@BIMSummit', '@BIMregNI', '@BIM4FItOut', '@becdecicco', '@BIMTridents', '@CampusBIM', '@BIM_Vienna', '@BIMregWM', '@BIMregScot', '@TheBIMCenter', '@BIMbicycle', '@cad4mac', '@BIMWorld_DE', '@markasaurus', '@BIMIreland', '@jamesmfee', '@GraitecRevitUK', '@brecert', '@eBIMc_', '@arch__tech', '@revitscratchpad', '@BIM_EUROPA', '@PuneetaroraBIM', '@BIMextension', '@PBC_Today', '@AEWarchitects', '@BIM_Bespoke', '@BIM4Housing']

DynamoBIM_list=['@DynamoBIM', '@BIM4Struc', '@ladybug_tools', '@ian_siegel', '@a_dieckmann', '@KevinJFielding', '@racoelho', '@DynamoBIM_Arch', '@jasonboehning', '@Thommynat0r', '@Dynamo_BIM', '@dynamobim_pl']

Revit_list=['@AutodeskRevit', '@DynamoBIM', '@autodesk', '@RevitNews', '@autodesku', '@AutodeskHelp', '@ShaanHurley', '@RevitDork', '@AutoCAD', '@davidfano', '@BIMbuilder', '@davewlight', '@AutodeskAEC', '@carlbass', '@geometrygym', '@Lynn_Allen', '@RevitHelp', '@amyonymous', '@archinate', '@katemorrical', '@ElrondBurrell', '@UNIFILabs', '@dabutts7', '@ShitMyRevitSays', '@Navisworks', '@MistresDorkness', '@REVIT', '@RevitZone', '@revitclinic', '@LARUG', '@TheRevitKid', '@3dRevitFamilies', '@masteringrevit', '@GraitecRevitUK', '@TheRevitGeek', '@IdeateInc', '@RTVTools', '@RevitCat', '@RevitUsers', '@RevitEs', '@prathianu', '@RevitLink', '@SeaRUG', '@RevitManager710', '@jadamthomas', '@SteveDeadman', '@Rcardial', '@tools4revit', '@BIMcollab', '@barrymaguireni', '@F9Productions', '@Troika_Elf', '@joeyoungblood', '@BillDebevc', '@cvedesigns', '@dennisrmartinez', '@qbimgest', '@r_robert_bell', '@AutodeskHelp', '@revitjames', '@NolanStrom', '@Techviz3D', '@KevinJFielding', '@RevitSevilla', '@RevitLution', '@Revitfamilies', '@KnowledgeSmart', '@RevitGenie', '@RevitTips', '@RevitCollection', '@ClassicalRevit', '@RevitLA', '@MundoRevit', '@theBIMbandit', '@RevitAsian', '@RevitBlocos', '@RevitTraining', '@RevitJedi', '@Bim4revitIvanov', '@RevitSchool']

DigArch_list=['@NieuweInstituut', '@CITAcph', '@HNI_Agentschap', '@HJDigiarch', '@marina_ov', '@hellomendelsohn', '@mediafacades','@crassociati', '@digitaltoolbox', '@ConstructionGL', '@kafrin', '@Jesseseegers', '@JeromeBuvat', '@marktgreen', '@ZNO_NZ', '@thespacesmag', '@StrelkaPress']

Parametric_list=['@parametric', '@Thinkparametric', '@algoritmic', '@bonooobong', '@Parametric01', '@ParametricMnky', '@CreoParametric', '@process_designs', '@teocomi', '@ParametricCamp', '@RhinoGrass', '@ParametricBIM', '@paramcookie', '@roryone', '@ParaComponents', '@MicroStation', '@SolidFaceCAD', '@sam_ng_', '@Modelur', '@Tygron', '@ConceptPara']

other_list=['@ColumbiaGSAPP', '@sciarc', '@sciarcdev', '@sciarc_alumni', '@AHDeleuran', '@Jamie_Farrell']

# adding a list of profiles who were tweeting the keywords from the second stream
keywords_list = []

#list of all lists
screen_names_list=list(set(BIM_list+DynamoBIM_list+Revit_list+DigArch_list+Parametric_list+other_list+keywords_list))
#Convert the list of Twitter screen names into a coma separated string, removing @signs into a string
screen_names_withoutat = []
for i in screen_names_list:
  screen_names_withoutat.append(i[1:])

# Query twitter with the comma separated list
userID_list = []
for user in screen_names_withoutat:
    userID=twitter.lookup_user(screen_name=user)
    userID_list.append(str(userID[0]["id_str"]))

# write the list of usedIDs to a file
with open('userID.txt', 'a') as f:
    pickle.dump(userID_list, f)
