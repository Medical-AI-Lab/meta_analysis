# Overview
To generate Summary ROCs and forest plots for both sensivity and specificity.

# Usage
`python meta-analysis.py --csvpath test.csv --figdir figs`

`--csvpath` is the path for metrics csv  
`--figdir` is the directory to save figures

# csv
Must contain header = ['TP', 'FP', 'TN', 'FN'].  
One line for one study.
## Example  
TP, FN, FP, TN  
59, 5, 55, 136  
142, 50	571, 2788  
137, 24, 107, 358  

# R library
We implemented this with mada library in R.  
https://cran.r-project.org/web/packages/mada/index.html
