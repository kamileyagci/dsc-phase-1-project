import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def dropOnes(df, jobCategory):
    
    df_pop = df[df.category == jobCategory]
    
    countList = df_pop.groupby('primary_name')['movie'].count().sort_values(ascending=False)
    #print(list(countList.index[0:52]), list(countList)[0:52])

    for i in range(0, len(countList)):
        if countList[i] == 1:
            stop = i
            break

    #print(stop)

    keepNameList = list(countList[:stop].index)
    #print(keepNameList)

    df_pop = df_pop.loc[df_pop['primary_name'].isin(keepNameList)]
    df_pop.shape
    
    return df_pop

def categoryStudy(df, jobCategory, maxList, figHeight, budget):
    
    dFrame = dropOnes(df, jobCategory)
    
    print("Total number: {}".format(len(dFrame['primary_name'].unique())))
    
    series1 = dFrame.groupby('primary_name')['profit_gross'].median().sort_values(ascending=False)[0:maxList]
    series2 = dFrame.groupby('primary_name')['profit_rate'].median().sort_values(ascending=False)[0:maxList]

    best1 = list(series1.index)
    best2 = list(series2.index)
    best = list(set(best1).intersection(best2))
    print('Best {} List: '.format(jobCategory), best)

    fig, axes = plt.subplots(1, 2, figsize=(20, figHeight))
    plt.subplots_adjust(wspace=0.4)

    series1.plot.barh(ax=axes[0])
    axes[0].set_title('Median Profit per {} (Production Budget > $100,000,000)'.format(jobCategory))
    axes[0].set_xlabel('Median Profit')
    axes[0].set_ylabel('{} Name'.format(jobCategory))

    series2.plot.barh(ax=axes[1], color='green')
    axes[1].set_title('Median Profit Rate per {} (Production Budget > $100,000,000)'.format(jobCategory))
    axes[1].set_xlabel('Median Profit Rate')
    axes[1].set_ylabel('{} Name'.format(jobCategory))

    plt.savefig('figures/{}-profit_{}Budget.png'.format(jobCategory, budget))
