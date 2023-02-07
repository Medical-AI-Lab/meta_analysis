import argparse
import os
import pandas as pd
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

# mada definitions


def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csvdir', type=str,
                        default='.', help='Path for directory.')    
    parser.add_argument('--csvname', type=str,
                        default='test.csv', help='Name for metrics csv.')
    parser.add_argument('--figdir', type=str, default='figs_mada',
                        help='Directory to save figs.')
    parser.add_argument('--modality', type=str, default='Xp',
                        help='Choose modality.')
    args = parser.parse_args()
    return args


class mada():
    def __init__(self, args):
        importr('mada')
        pandas2ri.activate()
        df = pd.read_csv(args.csvdir + '/' + args.csvname)
        df_modality = df[df['Modality'] == args.modality]
        df_inclusion = df_modality[df_modality['Meta analysis'] == "Applicable"][[
            'TP', 'FN', 'FP', 'TN']].astype('int')
        self.r_df = pandas2ri.py2rpy(df_inclusion)
        self.figdir = args.figdir + '/' + args.csvname.replace('.csv','')
        os.makedirs(self.figdir, exist_ok=True)

    def mada_fig_forest(self, type):
        '''Forest plot for type (sens, spec)'''
        mada_data = r.madad(self.r_df)
        r.pdf(self.figdir+'/'+type+'.pdf')
        r.forest(mada_data, type=type)

    def mada_msl_sroc(self):
        '''Summary ROC part1'''
        r.pdf(self.figdir+'/'+'mslsroc.pdf')
        r.ROCellipse(self.r_df)
        r.mslSROC(self.r_df, add=True)

    def mada_rs_sroc(self):
        '''Summary ROC part2'''
        r.pdf(self.figdir+'/'+'rssroc.pdf')
        r.ROCellipse(self.r_df)
        r.rsSROC(self.r_df, add=True)

    def mada_reitsma_sroc(self):
        '''Summary ROC part3'''
        r.pdf(self.figdir+'/'+'reitsmaroc.pdf')
        res = r.reitsma(self.r_df)
        summary = r.summary(res)
        with open(self.figdir+'/'+'reitsmasummary.txt', 'w') as f:
            print(summary, file=f)
        f.close()
        r.ROCellipse(self.r_df)
        r.plot(res, add=True)

    def mada_phm_sroc(self):
        '''Summary ROC part4'''
        r.pdf(self.figdir+'/'+'phmroc.pdf')
        res = r.phm(self.r_df)
        summary = r.summary(res)
        with open(self.figdir+'/'+'phmsummary.txt', 'w') as f:
            print(summary, file=f)
        r.ROCellipse(self.r_df)
        r.plot(res, add=True)


def main(args):
    # R mada
    classmada = mada(args)
    classmada.mada_msl_sroc()
    classmada.mada_rs_sroc()
    classmada.mada_reitsma_sroc()
    classmada.mada_phm_sroc()
    l_type = ['sens', 'spec']
    for type in l_type:
        classmada.mada_fig_forest(type)


if __name__ == '__main__':
    args = _argparse()
    main(args)
