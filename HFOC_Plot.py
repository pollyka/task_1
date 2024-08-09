import sys, os
import argparse
import math

from math import log10

sys.path.append('/work_dir/task_1/')
import ROOT
from ROOT import gStyle

gStyle.SetOptStat(ROOT.kFALSE)

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="The root file of the TProfile")
parser.add_argument("-l", "--label", help="The label of the output file")

args = parser.parse_args()

can = ROOT.TCanvas("can", "can", 800, 800)
can.SetTickx()
can.SetTicky()
can.SetLeftMargin(0.15)
can.SetBottomMargin(0.15)
can.cd()
filename = args.file
tfile = ROOT.TFile(filename)

text = ROOT.TLatex(0.18, 0.82, "CMS #bf{#scale[0.75]{#it{Simulation Preliminary}}}")
text.SetNDC()
text.SetTextSize(0.05)
text.SetTextFont(62)
text.Draw("SAME")

pro_pu = tfile.Get("gra_HFOC")
#pro_pu_sub = tfile.Get("pro_pu_sub")

pro_pu.SetTitle("HF occupancy")
lowpuf1 = ROOT.TF1("f1", "pol1", 0, 2.5)
pro_pu.Fit(lowpuf1, "R")
par0 = lowpuf1.GetParameter(0)
par1 = lowpuf1.GetParameter(1)
extraf1 = ROOT.TF1("f1", "pol1",0, 200)
extraf1.SetParameter(0, par0)
extraf1.SetParameter(1, par1)
extraf1.SetLineColor(ROOT.kRed)
extraf1.SetLineWidth(2)
pro_pu.GetXaxis().SetTitle("Average Pileup")
pro_pu.GetYaxis().SetTitle("-log(1-f_{occ})")
pro_pu.SetMarkerStyle(ROOT.kFullCircle)
pro_pu.SetMarkerSize(0.7)
pro_pu.SetMarkerColor(ROOT.kBlack)
pro_pu.SetLineWidth(2)
pro_pu.Draw("APEZ0")
extraf1.Draw("SAME")
text = ROOT.TLatex(0.18, 0.82, "CMS #bf{#scale[0.75]{#it{Simulation Preliminary}}}")
text.SetNDC()
text.SetTextSize(0.05)
text.SetTextFont(62)
text.Draw("SAME")



can.SaveAs('HFOC_Phase2_'+args.label+'.pdf')
can.SaveAs('HFOC_Phase2_'+args.label+'.png')


can.Update()

pro_pu.GetXaxis().SetRangeUser(0, 10)
pro_pu.GetYaxis().SetRangeUser(0, 0.05)
pro_pu.Draw("APEZ0")
extraf1.Draw("SAME")

text = ROOT.TLatex(0.18, 0.82, "CMS #bf{#scale[0.75]{#it{Simulation Preliminary}}}")
text.SetNDC()
text.SetTextSize(0.05)
text.SetTextFont(62)
text.Draw("SAME")

can.SaveAs('HFOC_Phase2_'+args.label+'_zoom.pdf')
can.SaveAs('HFOC_Phase2_'+args.label+'_zoom.png')

can.Update()

gra_pu = ROOT.TGraphErrors()
gra_pu.SetTitle("HF occupancy")
xarray = pro_pu.GetX()
yarray = pro_pu.GetY()
errarray = pro_pu.GetEY()
nbins = pro_pu.GetN()
ip=0
for ibin in range(nbins):
    binCent = xarray[ibin]
    binCont = yarray[ibin]
    binError = errarray[ibin]#yarray[ibin]
    curr_y = extraf1.Eval(binCent)
    gra_pu.SetPoint(ip, binCent, (binCont-curr_y)/curr_y)
    gra_pu.SetPointError(ip, 0, binError/curr_y)
    print(binError/curr_y)
    ip+=1

gra_pu.SetMarkerStyle(ROOT.kFullCircle)
gra_pu.SetMarkerSize(0.7)
gra_pu.SetMarkerColor(ROOT.kBlack)
gra_pu.SetLineColor(ROOT.kBlue)
gra_pu.SetLineWidth(2)
gra_pu.GetXaxis().SetTitle("Average Pileup")
gra_pu.GetYaxis().SetTitle("(<hfoc>-<hfoc>_{exp})/ <hfoc>")
gra_pu.GetYaxis().SetRangeUser(-0.06, 0.06)
line = ROOT.TLine(0, 0, 190, 0)
line.SetLineColor(ROOT.kRed)
line.SetLineWidth(2)

gra_pu.Draw("APE0Z")
#gra_pu.GetXaxis().SetRangeUser(0,2)
line.Draw("SAME")
text = ROOT.TLatex(0.18, 0.82, "CMS #bf{#scale[0.75]{#it{Simulation Preliminary}}}")
text.SetNDC()
text.SetTextSize(0.05)
text.SetTextFont(62)
text.Draw("SAME")


can.SaveAs("HFOC_deviation_from_linear_Phase2_"+args.label+".pdf")
can.SaveAs("HFOC_deviation_from_linear_Phase2_"+args.label+".png")

can.Update()
gra_pu.Draw("APE0Z")
gra_pu.GetXaxis().SetRangeUser(0,10)
line = ROOT.TLine(0, 0, 10, 0)

line.Draw("SAME")
text = ROOT.TLatex(0.18, 0.82, "CMS #bf{#scale[0.75]{#it{Simulation Preliminary}}}")
text.SetNDC()
text.SetTextSize(0.05)
text.SetTextFont(62)
text.Draw("SAME")

can.SaveAs("HFOC_deviation_from_linear_Phase2_"+args.label+"_Zoom.pdf")
can.SaveAs("HFOC_deviation_from_linear_Phase2_"+args.label+"_Zoom.png")
