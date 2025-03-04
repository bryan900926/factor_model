import pandas as pd 

price_tw = pd.read_csv(r"C:\Users\bryan\OneDrive\桌面\factor model\price_2000_2023\20241225015925.csv",encoding='utf-16',delimiter='\t')
price_tw = price_tw.rename(columns={'證券代碼':'ticker','年月':'date','TSE新產業名':'sector','報酬率％_月':'monthly_return','市值(百萬元)':'MarketCap'})
five_factor = pd.read_excel(r"C:\TejPro\TejPro\DataExport\five_factor.xlsx").drop(columns=['代號','名稱'])
five_factor = five_factor.rename(columns={'年月':'date','市場風險溢酬':'MRP',
                                          '淨值市價比溢酬':'HML','規模溢酬 (5因子)':'SMB',
                                          '投資因子':'CMA','盈利能力因子':'RMW'})
five_factor['date'] = pd.to_datetime(five_factor['date'],format='%Y/%m')
price_tw['date'] = pd.to_datetime(price_tw['date'],format='%Y%m')
us_sector_mapping = {
    '水泥工業': 'Materials',
    '食品工業': 'Consumer',
    '塑膠工業': 'Materials',
    '建材營造': 'Industrials',
    '汽車工業': 'Consumer',
    '紡織纖維': 'Consumer',
    '運動休閒': 'Consumer',
    '電子零組件': 'Information Technology',
    '電機機械': 'Industrials',
    '電器電纜': 'Industrials',
    '生技醫療': 'Health Care',
    '化學工業': 'Materials',
    '玻璃陶瓷': 'Materials',
    '造紙工業': 'Materials',
    '鋼鐵工業': 'Materials',
    '橡膠工業': 'Materials',
    '電腦及週邊': 'Information Technology',
    '半導體': 'Information Technology',
    '其他電子業': 'Information Technology',
    '通信網路業': 'Information Technology',
    '光電業': 'Information Technology',
    '電子通路業': 'Information Technology',
    '資訊服務業': 'Information Technology',
    '貿易百貨': 'Consumer',
    '航運業': 'Industrials',
    '油電燃氣業': 'Utilities',
    '觀光餐旅': 'Consumer',
    '金融業': 'Financials',
    '居家生活': 'Consumer',
    '數位雲端': 'Information Technology',
    '文化創意業': 'Consumer',
    '綠能環保': 'Agriculture and Environment',
    '存託憑證': 'Financials',
    '農業科技': 'Agriculture and Environment',
    '其他': 'Miscellaneous',
}

price_tw['Industry Name'] = price_tw['sector'].str.split().str[1]
price_tw['Sector'] = price_tw['Industry Name'].map(us_sector_mapping)
count = {}
for s, df in price_tw.groupby('Sector'):
    count[s] = len(df['ticker'].unique())

grouped = price_tw.groupby(['Sector', 'date'])

# Equally-weighted returns
equally_weighted = grouped['monthly_return'].mean()
# Value-weighted returns function
def calc_value_weighted(group):
    total_market_cap = group['MarketCap'].sum()
    return (group['monthly_return'] * group['MarketCap'] / total_market_cap).sum()

value_weighted = grouped.apply(calc_value_weighted)

# Combine into a single DataFrame
result = pd.DataFrame({
    'Equally_Weighted': equally_weighted,
    'Value_Weighted': value_weighted
}).reset_index()

# Display the resulting DataFrame
merge =pd.merge(result,five_factor,on=['date'])
# merge.to_csv('five_factor.csv')

