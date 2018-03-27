#!/usr/bin/env python3
" \
Author: A. Dunning \
Date: March 2018 \
Descripton: Code for performing statistical analysis on financial instrument data for instruments traded on Plus500. Data gathered using data-analysis/pull-from-iex/grab_data.py. \
"
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle('data_output_USstock.pickle')

"set index to datetime format to make resampling possible"
df.index = pd.to_datetime(df.index)
#df = df.resample('M').backfill()

"method to calculate the percentage change of a symbol since day 0"
def gen_fromstart_pc(col):
    pc_d = (col - col[0])/col[0] * 100.
    pc_d = pd.DataFrame(pc_d)
    return pc_d

"method to calculate the percentage change of a symbol day-to-day or month-to-month or ..."
def gen_pointpoint_pc(col):
    pc_d = (col - col.shift(1))/col.shift(1) * 100
    pc_d = pd.DataFrame(pc_d)
    return pc_d

"make a dict to identify which of the above methods to use according to a string"
key = pd.DataFrame({'A':['pointpoint','fromstart'],
        'operation':[gen_pointpoint_pc,gen_fromstart_pc]})

"run gen_<which>_pc on all symbols in the dataframe, returning a new 'percentage change' dateframe df_p. res_rule determines the resampling ('D', 'W', 'M', ...)"
def gen_pc_df(df_i, res_rule, which):
    df_p = pd.DataFrame()
    df_i = df_i.resample(res_rule).backfill()
    for symbol in df_i.columns.values:
        if df_p.empty:
            df_p = key['operation'][key['A']==which].iloc[0](df_i[symbol])
        else:
            df_p[symbol] = key['operation'][key['A']==which].iloc[0](df_i[symbol])
    return df_p

"generate the correlation coefficients for all possible stock pairs, for data sampled at various intervals; put them in a dataframe"
resample_rules = ['1D','2D','W','M']
def pairwise_corr(df_i):
    all_pc_corr = pd.DataFrame()
    for rule in resample_rules:
        df_pc = gen_pc_df(df_i, rule, 'pointpoint')

        "run correlation on percentage change data"
        df_pc_corr = df_pc.corr()

        "unstack correlation dataframe to create a double-index (symbol1, symbol2) dataframe with \
        correlation between each pair as the only column"
        s_pc_corr = df_pc_corr.unstack()

        "drop NaNs and self-correlations from the correlation dataframe"
        s_pc_corr.dropna(inplace=True)
        s_pc_corr = s_pc_corr[s_pc_corr != 1.0]

        "sort this to find the pairs with highest correlation"
        #s_pc_corr_o = s_pc_corr.sort_values(kind='quicksort')

        if all_pc_corr.empty:
            all_pc_corr = pd.DataFrame(s_pc_corr)
            all_pc_corr.columns = [rule]
        else:
            all_pc_corr[rule] = s_pc_corr

    return all_pc_corr

"run the above"
pc_corr = pairwise_corr(df)

