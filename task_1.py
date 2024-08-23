import sys, os
import ROOT
import numpy
import argparse 
import array 
from math import fabs 


parser = argparse.ArgumentParser(description="Produce HF Lumi")


parser.add_argument("-f", "--file", nargs = "+", default="", help="The path the file") #выбор файла для чтения из консоли
parser.add_argument("-o", "--output", nargs = "+", default="", help="The name of the output file") #написать pileup
parser.add_argument("-d", "--depth", default="1", help="The depth of the fiber: 1, long; 2, short") #использую пока на default
parser.add_argument("-p", "--pileup", nargs = "+", default="", help="The pileup value") #написать pileup

args = parser.parse_args()

depth = int(args.depth)

filenames = args.file
outputs = args.output
puleups = args.pileup

print("OUTPUTS - HF", outputs)
print("File names - ", filenames)
#tfile = ROOT.TFile.Open(filename)

i = 0 
for i in range (len(filenames)):
        ttree = ROOT.TChain("hcalTupleTree/tree")
        ttree.AddFile(filenames[i])
        #ttree = tfile.Get("hcalTupleTree/tree")
        nevts = ttree.GetEntries()
        print (nevts)
        PU = array.array('f', [0])
        ET_sum = array.array('d', [0]) #'d' - double
        ET_sum_sub = array.array('d', [0])
        nCh_31 = array.array('I', [0])
        nCh_32 = array.array('I', [0]) 
        ADC_31 = array.array('I', 1000*[0]) # "I" - signed long (int)
        ADC_32 = array.array('I', 1000*[0])

        PU[0] = float(puleups[i])
        print("Puleups:", PU[0])

        fout = ROOT.TFile("HF_"+str(PU[0])+".root", "RECREATE")
        newtree = ROOT.TTree("HFtree", "HFtree")
        newtree.Branch("PU", PU, "PU/D")
        newtree.Branch("ET_sum", ET_sum, "ET_sum/D")
        newtree.Branch("ET_sum_sub", ET_sum_sub, "ET_sum_sub/D")
        newtree.Branch("nCh_31", nCh_31, "nCh_31/i")
        newtree.Branch("nCh_32", nCh_32, "nCh_32/i")
        newtree.Branch("ADC_31", ADC_31, "ADC_31[nCh_31]/i")
        newtree.Branch("ADC_32", ADC_32, "ADC_32[nCh_32]/i")

        for ievt in range(nevts):
            print(ievt)
            ttree.GetEntry(ievt)
            etsum=0
            etsum_sub = 0
            Neta = ttree.QIE10DigiIEta.size()
            print("вывод Neta", Neta)
            N31 = 0
            N32 = 0
            for ieta in range(Neta):
                if fabs(ttree.QIE10DigiIEta.at(ieta))==31 or fabs(ttree.QIE10DigiIEta.at(ieta))==32:
                    nchannel = ttree.QIE10DigiFC.at(ieta).size()
                    curreta = fabs(ttree.QIE10DigiIEta.at(ieta))
                    for ich in range(nchannel):
                        etsum+=ttree.QIE10DigiFC.at(ieta).at(ich)
                        if ttree.QIE10DigiADC.at(ieta).at(ich)>7: # выбрать оптимизатор для ката, понять как влияет кат на выходные данные
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
        fout.WriteTObject(newtree, "HFtree")
        fout.Close()
        i+=1
        print(i)
