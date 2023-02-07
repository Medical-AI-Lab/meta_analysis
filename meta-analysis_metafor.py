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
    parser.add_argument('--figdir', type=str, default='figs_metafor',
                        help='Directory to save figs.')
    parser.add_argument('--modality', type=str, default='Xp',
                        help='Choose modality.')
    args = parser.parse_args()
    return args


class metafor():
    def __init__(self, args):
        importr('metafor')
        csvpath = args.csvdir + '/' + args.csvname
        r.assign("csvpath", csvpath)
        r.assign("modality", args.modality)
        r('df_r_pre2 <- read.csv(csvpath)')
        r('df_r_pre <- df_r_pre2[df_r_pre2$Meta.analysis=="Applicable",]')
        r('df_r <- df_r_pre[df_r_pre$Modality==modality,]')
        self.figdir = args.figdir + '/' + args.csvname.replace('.csv','')
        os.makedirs(self.figdir, exist_ok=True)

    def meta_fig_forest(self, type='OR'):
        '''Forest plot for odds'''
        r.assign("type", type)
        r('meta_escalc <- escalc(measure=type, ai=df_r$TP, bi=df_r$FP, ci=df_r$FN, di=df_r$TN)')
        rma_analysis = r('rma(yi, vi, data=meta_escalc)')
        r.pdf(self.figdir+'/'+type+'_forest.pdf')
        r.forest(rma_analysis, header='Trials')

    def meta_fig_funnel(self, type='OR'):
        '''Funnel plot for odds'''
        r.assign("type", type)
        r('meta_escalc <- escalc(measure=type, ai=df_r$TP, bi=df_r$FP, ci=df_r$FN, di=df_r$TN)')
        rma_analysis = r('rma(yi, vi, data=meta_escalc)')
        r.pdf(self.figdir+'/funnel.pdf')
        r.funnel(rma_analysis)

    def meta_res_funnel(self, type='OR'):
        '''Funnel plot for odds'''
        r.assign("type", type)
        r('meta_escalc <- escalc(measure=type, ai=df_r$TP, bi=df_r$FP, ci=df_r$FN, di=df_r$TN)')
        r('res <- rma(yi, vi, data=meta_escalc)')
        regres = r('regtest(res)')
        r.sink(self.figdir+'/'+'funnel.csv')
        r.print(regres)
        r.sink()

def main(args):
    # R meta
    classmeta = metafor(args)
    classmeta.meta_fig_funnel()
    classmeta.meta_res_funnel()
    classmeta.meta_fig_forest()


if __name__ == '__main__':
    args = _argparse()
    main(args)
