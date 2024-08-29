import sys, os
import argparse
import math

from math import log10,log,sqrt

#sys.path.append('/work_dir/task_1/')

import ROOT
from ROOT import TFile, TCanvas, TH1F
from ROOT import gStyle
from ROOT import kGreen, kRed, kBlue

dictPileup = {
     'p_05':'0.5',
     'p_1':'1',
     'p_2':'2',
     'p_10':'10',
     'p_30':'30',
     'p_50':'50',
     'p_75':'75',
     'p_100':'100',
     'p_120':'120',
     'p_140':'140',
     'p_160':'160',
     'p_180':'180',
     'p_200':'200',
}

dictiInputFileO = {
     'o_05':'HF_0.5.root',
     'o_1':'HF_1.0.root',
     'o_2':'HF_2.0.root',
     'o_10':'HF_10.0.root',
     'o_30':'HF_30.0.root',
     'o_50':'HF_50.0.root',
     'o_75':'HF_75.0.root',
     'o_100':'HF_100.0.root',
     'o_120':'HF_120.0.root',
     'o_140':'HF_140.0.root',
     'o_160':'HF_160.0.root',
     'o_180':'HF_180.0.root',
     'o_200':'HF_200.0.root',
}


def calc_zerofrac(zero_frac, hit):
    if hit:
        zero_frac[1]+=1
    else:
        zero_frac[0]+=1
        zero_frac[1]+=1

gStyle.SetOptStat(ROOT.kFALSE)

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="The root file for data")
parser.add_argument("-p", "--pileup", help="The label of the output file")
#parser.add_argument("-t", "--threshold", help="The ADC threshold") #спросить что это?

args = parser.parse_args()

filename = args.file.split()
labels = args.pileup.split()
thresholds = args.pileup.split()
#thresholds = args.threshold.split()

f = 0
for f in range(len(filename)):
    tfile = ROOT.TFile(dictiInputFileO[filename[f]])
    ttree = tfile.Get("HFtree")
    fout = ROOT.TFile("HFOC"+dictPileup[thresholds[f]]+"_"+dictPileup[labels[f]]+".root", "RECREATE")
    gra_HFOC = ROOT.TGraphErrors()
    PU_list = {}
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
                if ttree.ADC_31[iCh]<=int(dictPileup[thresholds[f]]):
                    PU_list[pu].append([1,1])
                else:
                    PU_list[pu].append([0,1])

            for iCh2 in range(nCh2):
                #print "ADC", ttree.ADC_31[iCh]
                if ttree.ADC_32[iCh2]<=int(dictPileup[thresholds[f]]):
                    PU_list[pu].append([1,1])
                else:
                    PU_list[pu].append([0,1])
        else:
            for iCh in range(nCh):
                calc_zerofrac(PU_list[pu][iCh], bool((ttree.ADC_31[iCh]>int(dictPileup[thresholds[f]]))))
            for iCh in range(nCh2):
                calc_zerofrac(PU_list[pu][iCh+nCh], bool((ttree.ADC_32[iCh]>int(dictPileup[thresholds[f]]))))
        #print PU_list[pu]
        #print PU_list[pu]
    print(PU_list)
    PUs = list(PU_list.keys())
    PUs.sort()
    iPU = 0

    for PU in PUs:
        AveFrac=0
        nCh = 0 #len(PU_list[PU])
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
