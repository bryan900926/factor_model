import pandas as pd 
import statsmodels.api as sm 
import matplotlib.pyplot as plt  
import matplotlib.dates as mdates

# Define rolling regression function
def rolling_ols(data, window, sector, info):
    results = []
    sector_data = data[data['Sector'] == sector]
    for i in range(window, len(sector_data)):
        # Rolling window
        subset = sector_data.iloc[i-window:i]
        
        y = subset['Equally_Weighted']
        X = subset[['RF', 'SMB', 'HML', 'RMW', 'CMA','MRP']]
        X = sm.add_constant(X)
        
        model = sm.OLS(y, X).fit()

        statis = model.tvalues if info == 'T-ratio' else model.params
        results.append({
            'Sector': sector,
            'Date': subset['date'].iloc[-1],  # Last date in the window
            info+'_MRP': statis['MRP'],
            info+'_SMB': statis['SMB'],
            info+'_HML': statis['HML'],
            info+'_RMW': statis['RMW'],
            info+'_CMA': statis['CMA']
        })

    rolling_results =  pd.DataFrame(results)
    t_ratio_columns = [info+'_MRP', info+'_SMB', info+'_HML', info+'_RMW', info+'_CMA']
    labels = ['Market', 'Size', 'Value', 'Profitability', 'Investment']
    
    plt.figure(figsize=(14, 7))
    
    for column, label in zip(t_ratio_columns, labels):
        plt.plot(rolling_results['Date'], rolling_results[column], label=f'{info} ({label})')
    
    if info == 'T-ratio':  
      plt.axhline(2, color='green', linestyle='--', label='Significance Threshold (+2)')
      plt.axhline(-2, color='red', linestyle='--', label='Significance Threshold (-2)')
    
    plt.title(f"{info} for All Factors in {sector} Sector")
    plt.xlabel('Date')
    plt.ylabel(info)
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(sector + ' tratio.png')
    # plt.show()

data = pd.read_csv(r'C:\Users\bryan\OneDrive\桌面\python\ff.csv')
data['date'] = pd.to_datetime(data['date'])
sectors = data['Sector'].unique()
# rolling_results = rolling_ols(data, 36, 'Information Technology','T-ratio')
# for s in sectors:
#     rolling_ols(data, 36, s, 'T-ratio')




