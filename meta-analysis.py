import argparse
import os
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

# mada definitions
def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csvpath', type=str, default='test.csv', help='Path for metrics csv.')
    parser.add_argument('--figdir', type=str, default='figs', help='Directory to save figs.')
    args = parser.parse_args() 
    return args

class mada():
    def __init__(self, args):
        importr('mada')
        with localconverter(robjects.default_converter + pandas2ri.converter):
            self.r_df = robjects.conversion.py2rpy(pd.read_csv(args.csvpath))
        self.figdir = args.figdir
        os.makedirs(args.figdir,exist_ok=True)

    def mada_fig_forest(self,type):
        '''Forest plot for type (sens, spec)'''
        mada_data = r.madad(self.r_df)
        r.pdf(self.figdir+'/'+type+'.pdf')
        r.forest(mada_data, type= type)

    def mada_msl_sroc(self):
        '''Summary ROC part1'''
        r.pdf(self.figdir+'/'+'mslsroc.pdf')
        r.ROCellipse(self.r_df)
        r.mslSROC(self.r_df, add = True)

    def mada_rs_sroc(self):
        '''Summary ROC part2'''
        r.pdf(self.figdir+'/'+'rssroc.pdf')
        r.ROCellipse(self.r_df)
        r.rsSROC(self.r_df, add = True)

def main(args):
    # R mada
    classmada = mada(args)
    classmada.mada_msl_sroc()
    classmada.mada_rs_sroc()
    l_type = ['sens','spec']
    for type in l_type:
        classmada.mada_fig_forest(type)

if __name__ == '__main__':
    args = _argparse()
    main(args)