import pandas as pd

# regions to be excluded
excl = ['WLD', 'IBT', 'LMY', 'MIC', 'IBD', 'EAR', 'LMC', 'UMC', 'EAS', 'LTE', 
        'EAP', 'TEA', 'TSA', 'SAS', 'IDA', 'OED', 'HIC', 'IDX', 'SSF', 'TSS',
        'SSA', 'LDC', 'PST', 'PRE', 'FCS', 'ECS', 'AFE', 'HPC', 'LIC', 'LCN',
        'MEA', 'AFW', 'TLA', 'IDB', 'LAC', 'TEC', 'ARB', 'EUU', 'MNA', 'ECA',
        'TMN', 'NAC', 'EMU', 'CEB', 'SST', 'OSS']
   
df = pd.read_csv('data/API_SP.POP.TOTL_DS2_en_csv_v2_85.csv', header = 2)
filtered = df[~df['Country Code'].isin(excl)]
filtered.to_csv('data/filtered.csv', index = False)