import sys, os
import ROOT
import numpy
import argparse 
import array 
from math import fabs 
import ostap.fitting.roofit

dictInputFileN = {
     'n_05':'HF0.5.root',
     'n_1': 'HF1.root',
     'n_2':'HF2.root',
     'n_10':'HF10.root',
     'n_30': 'HF30.root',
     'n_50':'HF50.root',
     'n_75':'HF75.root',
     'n_100': 'HF100.root',
     'n_120':'HF120.root',
     'n_140': 'HF140.root',
     'n_160':'HF160.root',
     'n_180': 'HF180.root',
     'n_200':'HF200.root',
}

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



parser = argparse.ArgumentParser(description="Produce HF Lumi")

parser.add_argument("-f", "--file", default="", help="The path the file") #выбор файла для чтения из консоли
parser.add_argument("-d", "--depth", default="1", help="The depth of the fiber: 1, long; 2, short") #использую пока на default
parser.add_argument("-p", "--pileup", default="", help="The pileup value") #написать pileup
parser.add_argument("-t", "--threshold", default="", help="The threshold")

args = parser.parse_args()

depth = int(args.depth)

filenames = args.file.split()
pileups = args.pileup.split()
thresholds = args.threshold

print("OUTPUTS - HF", pileups)
print("File names - ", filenames)
#tfile = ROOT.TFile.Open(filename)


Mean_list = array.array('d', [])
PU_list = array.array('d', [])


i = 0 
for i in range (len(filenames)):
        ttree = ROOT.TChain("hcalTupleTree/tree")
        ttree.AddFile(dictInputFileN[filenames[i]])
        #print(dictInputFileN[filenames[i]])
        #ttree = tfile.Get("hcalTupleTree/tree")
        nevts = ttree.GetEntries()
        #print (nevts)
        PU = array.array('f', [0])
        ET_sum = array.array('d', [0]) #'d' - double
        ET_sum_sub = array.array('d', [0])
        nCh_31 = array.array('I', [0])
        nCh_32 = array.array('I', [0]) 
        ADC_31 = array.array('I', 1000*[0]) # "I" - signed long (int)
        ADC_32 = array.array('I', 1000*[0])

        
        PU[0] = float(dictPileup[pileups[i]]) #записывает 0
        fout = ROOT.TFile("HF_"+str(PU[0])+"_"+thresholds+"_.root", "RECREATE")
        newtree = ROOT.TTree("HFtree", "HFtree")
        newtree.Branch("PU", PU, "PU/D")
        newtree.Branch("ET_sum", ET_sum, "ET_sum/D")
        newtree.Branch("ET_sum_sub", ET_sum_sub, "ET_sum_sub/D")
        newtree.Branch("nCh_31", nCh_31, "nCh_31/i")
        newtree.Branch("nCh_32", nCh_32, "nCh_32/i")
        newtree.Branch("ADC_31", ADC_31, "ADC_31[nCh_31]/i")
        newtree.Branch("ADC_32", ADC_32, "ADC_32[nCh_32]/i")


        for ievt in range(nevts):
            #print(ievt)

            ttree.GetEntry(ievt)
            etsum=0
            etsum_sub = 0
            Neta = ttree.QIE10DigiIEta.size()
            N31 = 0
            N32 = 0
            
            for ieta in range(Neta):
                if fabs(ttree.QIE10DigiIEta.at(ieta))==31 or fabs(ttree.QIE10DigiIEta.at(ieta))==32:
                    nchannel = ttree.QIE10DigiFC.at(ieta).size()
                    curreta = fabs(ttree.QIE10DigiIEta.at(ieta))
                    for ich in range(nchannel):
                        etsum+=ttree.QIE10DigiFC.at(ieta).at(ich)
                        if ttree.QIE10DigiADC.at(ieta).at(ich)>int(thresholds):
                            etsum_sub+=ttree.QIE10DigiFC.at(ieta).at(ich)
                        if ttree.QIE10DigiDepth.at(ieta)!=depth: continue
                        if curreta==31:
                            ADC_31[N31] = ttree.QIE10DigiADC.at(ieta).at(ich)
                            N31+=1
                        if curreta==32:
                            ADC_32[N32] = ttree.QIE10DigiADC.at(ieta).at(ich)
                            N32+=1
                        
                        

            nCh_31[0] = N31
            nCh_32[0] = N32
            ET_sum[0]=etsum
            ET_sum_sub[0]=etsum_sub
            newtree.Fill()
            
        PU_list.append(float(dictPileup[pileups[i]]))
        a = newtree.ET_sum_sub
        Mean_list.append(a)
        print(a)
        fout.WriteTObject(newtree, "HFtree")
        fout.Close()
        print("Pileups:", PU[0], " - done!")
        i+=1
   
#print(Mean_list, PU_list)

fout_2 = ROOT.TFile("result"+thresholds+".root", "RECREATE")
сanv = ROOT.TCanvas("canv", "Graph", 800, 600)
gra_HFOC = ROOT.TGraph(int(len(PU_list)), PU_list, Mean_list)
gra_HFOC.SetTitle("Graph; PileUp; SumSub")
gra_HFOC.Draw("*")
fit1 = ROOT.TF1("f1", "[0]+[1]*x")
gra_HFOC.Fit(fit1)
fout_2.WriteTObject(gra_HFOC, "gra_HFOC")
fout_2.Close()
print("DONE!")

