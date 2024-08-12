import sys, os
import argparse
import math

from math import log10,log,sqrt

sys.path.append('/Users/jingyuluo/Downloads/root_dir/lib')

import ROOT
from ROOT import TFile, TCanvas, TH1F
from ROOT import gStyle
from ROOT import kGreen, kRed, kBlue


def calc_zerofrac(zero_frac, hit):
    if hit:
        zero_frac[1]+=1
    else:
        zero_frac[0]+=1
        zero_frac[1]+=1

gStyle.SetOptStat(ROOT.kFALSE)



parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="The root file for data")
parser.add_argument("-l", "--label", help="The label of the output file")
parser.add_argument("-t", "--threshold", help="The ADC threshold")

args = parser.parse_args()

filename = args.file
tfile = ROOT.TFile(filename)

ttree = tfile.Get("HFtree")

fout = ROOT.TFile("HFOC_threshold"+str(args.threshold)+"_new_Phase2_"+args.label+".root", "RECREATE")

gra_HFOC = ROOT.TGraphErrors()

PU_list = {}

#for i in range(85, 0, -5):
#    PU_list[i]=[]



nevts = ttree.GetEntries()

for ievt in range(nevts):
    ttree.GetEntry(ievt)
    pu = float(ttree.PU)
    if ievt%1000==0:
        print(ievt,pu)
    if not pu in PU_list.keys():
        PU_list[pu]=[]
    nCh = ttree.nCh_31
    nCh2 = ttree.nCh_32
    if len(PU_list[pu])==0:
        for iCh in range(nCh):
            #print "ADC", ttree.ADC_31[iCh]
            if ttree.ADC_31[iCh]<=int(args.threshold):
                PU_list[pu].append([1,1])
            else:
                PU_list[pu].append([0,1])

        for iCh2 in range(nCh2):
            #print "ADC", ttree.ADC_31[iCh]
            if ttree.ADC_32[iCh2]<=int(args.threshold):
                PU_list[pu].append([1,1])
            else:
                PU_list[pu].append([0,1])


    else:
        for iCh in range(nCh):
            calc_zerofrac(PU_list[pu][iCh], bool((ttree.ADC_31[iCh]>int(args.threshold))))
        for iCh in range(nCh2):
            calc_zerofrac(PU_list[pu][iCh+nCh], bool((ttree.ADC_32[iCh]>int(args.threshold))))
    #print PU_list[pu]
    #print PU_list[pu]
print(PU_list)
PUs = list(PU_list.keys())
PUs.sort()
iPU = 0

for PU in PUs:
    AveFrac=0
    nCh = 0#len(PU_list[PU])
    Err = 0
    for channel in PU_list[PU]:
        AveFrac+=channel[0]
        nCh+=channel[1]
    #print nCh
    if nCh!=0:
        Err = sqrt(1/float(AveFrac)-1/float(nCh))
        AveFrac = float(AveFrac)/float(nCh)
        
    if AveFrac!=0:
        print(PU, nCh, -log10(AveFrac), Err)
        gra_HFOC.SetPoint(iPU, float(PU), -log10(AveFrac))
        gra_HFOC.SetPointError(iPU, 0, 1/(log(10))*Err)
        iPU+=1

fout.WriteTObject(gra_HFOC, "gra_HFOC")
fout.Close()
