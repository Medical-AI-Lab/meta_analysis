import argparse
import os
import pandas as pd
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter

# mada definitions


def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csvdir', type=str,
                        default='.', help='Path for directory.')    
    parser.add_argument('--csvname', type=str,
                        default='test.csv', help='Name for metrics csv.')
    parser.add_argument('--figdir', type=str, default='figs_meta4diag',
                        help='Directory to save figs.')
    parser.add_argument('--modality', type=str, default='Xp',
                        help='Choose modality.')
    args = parser.parse_args()
    return args


class meta4diag():
    def __init__(self, args):
        importr('meta4diag')
        importr('INLA')
        csvpath = args.csvdir + '/' + args.csvname
        r.assign("csvpath", csvpath)
        r.assign("modality", args.modality)
        r('df_r_pre2 <- read.csv(csvpath)')
        r('df_r_pre <- df_r_pre2[df_r_pre2$Meta.analysis=="Applicable",]')
        r('df_r <- df_r_pre[df_r_pre$Modality==modality,]')
        self.figdir = args.figdir + '/' + args.csvname.replace('.csv','')
        os.makedirs(self.figdir, exist_ok=True)

    def forest_plot(self):
        '''Forest plot for sensitivity'''
        r('res <- meta4diag(data = df_r, model.type = 1, var.prior = "invgamma", cor.prior = "normal", var.par = c(0.25, 0.025), cor.par = c(0, 5), init = c(0.01, 0.01, 0), link = "logit", quantiles = c(0.025, 0.5, 0.975), verbose = FALSE, covariates = NULL, nsample = FALSE)')
        r.pdf(self.figdir+'/'+'sens_forest.pdf')
        r('forest(res, accuracy.type="sens", est.type="mean", p.cex="scaled", p.pch=15, p.col="black", nameShow="right", dataShow="center", estShow="left", text.cex=1, shade.col="gray", arrow.col="black", arrow.lty=1, arrow.lwd=1, cut=TRUE, intervals=c(0.025,0.975), main="Forest plot", main.cex=1.5, axis.cex=1)')
        r.pdf(self.figdir+'/'+'spec_forest.pdf')
        r('forest(res, accuracy.type="spec", est.type="mean", p.cex="scaled", p.pch=15, p.col="black", nameShow="right", dataShow="center", estShow="left", text.cex=1, shade.col="gray", arrow.col="black", arrow.lty=1, arrow.lwd=1, cut=TRUE, intervals=c(0.025,0.975), main="Forest plot", main.cex=1.5, axis.cex=1)')

    def sroc(self):
        '''Summary ROC'''
        r('res <- meta4diag(data = df_r, model.type = 1, var.prior = "invgamma", cor.prior = "normal", var.par = c(0.25, 0.025), cor.par = c(0, 5), init = c(0.01, 0.01, 0), link = "logit", quantiles = c(0.025, 0.5, 0.975), verbose = FALSE, covariates = NULL, nsample = FALSE)')
        r.pdf(self.figdir+'/'+'sroc1.pdf')
        r('SROC(res, sroc.type=1, est.type="mean", sp.cex=1.5, sp.pch=8, sp.col="red", dataShow="o", data.col="#FF0000", data.cex="scaled", data.pch=1, lineShow=T, line.lty=1, line.lwd=2, line.col="black", crShow=T, cr.lty=2, cr.lwd=1.5, cr.col="blue", prShow=T, pr.lty=3, pr.lwd=1,  pr.col="darkgray", dataFit=T, add=FALSE, main="", legend=F, legend.cex=0.7)')
        r.pdf(self.figdir+'/'+'sroc2.pdf')
        r('SROC(res, sroc.type=2, est.type="mean", sp.cex=1.5, sp.pch=8, sp.col="red", dataShow="o", data.col="#FF0000", data.cex="scaled", data.pch=1, lineShow=T, line.lty=1, line.lwd=2, line.col="black", crShow=T, cr.lty=2, cr.lwd=1.5, cr.col="blue", prShow=T, pr.lty=3, pr.lwd=1,  pr.col="darkgray", dataFit=T, add=FALSE, main="", legend=F, legend.cex=0.7)')
        r.pdf(self.figdir+'/'+'sroc3.pdf')
        r('SROC(res, sroc.type=3, est.type="mean", sp.cex=1.5, sp.pch=8, sp.col="red", dataShow="o", data.col="#FF0000", data.cex="scaled", data.pch=1, lineShow=T, line.lty=1, line.lwd=2, line.col="black", crShow=T, cr.lty=2, cr.lwd=1.5, cr.col="blue", prShow=T, pr.lty=3, pr.lwd=1,  pr.col="darkgray", dataFit=T, add=FALSE, main="", legend=F, legend.cex=0.7)')
        r.pdf(self.figdir+'/'+'sroc4.pdf')
        r('SROC(res, sroc.type=4, est.type="mean", sp.cex=1.5, sp.pch=8, sp.col="red", dataShow="o", data.col="#FF0000", data.cex="scaled", data.pch=1, lineShow=T, line.lty=1, line.lwd=2, line.col="black", crShow=T, cr.lty=2, cr.lwd=1.5, cr.col="blue", prShow=T, pr.lty=3, pr.lwd=1,  pr.col="darkgray", dataFit=T, add=FALSE, main="", legend=F, legend.cex=0.7)')
        r.pdf(self.figdir+'/'+'sroc5.pdf')
        r('SROC(res, sroc.type=5, est.type="mean", sp.cex=1.5, sp.pch=8, sp.col="red", dataShow="o", data.col="#FF0000", data.cex="scaled", data.pch=1, lineShow=T, line.lty=1, line.lwd=2, line.col="black", crShow=T, cr.lty=2, cr.lwd=1.5, cr.col="blue", prShow=T, pr.lty=3, pr.lwd=1,  pr.col="darkgray", dataFit=T, add=FALSE, main="", legend=F, legend.cex=0.7)')


def main(args):
    # R meta
    classmeta4diag = meta4diag(args)
    classmeta4diag.forest_plot()
    classmeta4diag.sroc()


if __name__ == '__main__':
    args = _argparse()
    main(args)
