# from dwapi import datawiz
from . import datawiz

from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

pd.options.display.float_format = '{:.2f}'.format

def main_script(date_from, date_to, log = 'test1@mail.com', pas = '1qaz'):
	dw = datawiz.DW(log, pas)

	#####################################################################################
	############################     ПЕРВАЯ ТАБЛ - ПО КАТЕГОРЯИМ    #####################
	#####################################################################################
	def clean_date(x):
	    d = datetime.strptime(x, '%Y-%m-%d')
	    new_d = d.strftime('%d-%m-%Y')
	    return new_d

	df = dw.get_categories_sale(date_from=date_from, date_to=date_to, by=['turnover','qty','receipts_qty'], view_type = 'raw')
	df['date'] = df['date'].apply(lambda x: clean_date(x))

	bla = pd.DataFrame(df.pivot_table(index = ['date'], values=['turnover','qty','receipts_qty'], aggfunc=sum))
	bla['Середній чек'] = bla['turnover'] / bla['receipts_qty']
	bla.index.names = ['Показник']
	bla.rename(columns = {'turnover':'Оборот', 'qty':'Кількість товарів', 'receipts_qty':'Кількість чеків'}, inplace = True)

	df = bla[['Оборот', 'Кількість товарів', 'Кількість чеків', 'Середній чек']].sort_index(ascending=0).T
	uniq_date = df.columns[:-1].values

	# РАСЧЕТЫ
	all_df = []

	for i in range(len(df.columns)-1):
	    try:
	        df_small = df.iloc[:, i:i+2]
	        df_small['Різниця'] = df.iloc[:,i] - df.iloc[:,i+2]
	        df_small['Різниця в %'] = (df_small.loc[:, 'Різниця'] / df.iloc[:,i+2]).mul(100).round(2)
	        
	    except:
	        df_small = df.iloc[:, i:]
	        df_small['Різниця'] = df.iloc[:,i] - df.iloc[:,-1]
	        df_small['Різниця в %'] = (df_small.loc[:, 'Різниця'] / df.iloc[:,-1]).mul(100).round(2)
	        
	    all_df.append(df_small.to_html(classes="table table-bordered table-hover"))


	#####################################################################################
	##########################     ОСТАЛЬНЫЕ ТАБЛ - ПО ПРОДУКТАМ    #####################
	#####################################################################################
	df = dw.get_products_sale(date_from=date_from, date_to=date_to, by=['turnover','qty'], view_type = 'raw')
	df['date'] = df['date'].apply(lambda x: clean_date(x))

	bla = df.groupby(['name', 'date']).sum().reset_index()
	bla.drop(columns = ['product'], inplace = True)

	# prepare df

	qty = pd.pivot_table(bla, index = 'name', values = 'qty', columns = 'date', aggfunc = np.sum, fill_value=0)
	turnover = pd.pivot_table(bla, index = 'name', values = 'turnover', columns = 'date', aggfunc = np.sum, fill_value=0)

	qty = qty.T.sort_values('date', ascending = False).T
	turnover = turnover.T.sort_values('date', ascending = False).T


	# РАСЧЕТЫ
	negative_df = []
	positive_df = []


	for i in range(len(qty.columns)-1):
	    try:        
	        small_qty = qty.iloc[:, i:i+2]
	        small_qty['Зміна кількості продаж'] = qty.iloc[:,i] - qty.iloc[:,i+2]
	        
	        small_turnover = turnover.iloc[:, i:i+2]
	        small_turnover['Зміна обороту'] = turnover.iloc[:,i] - turnover.iloc[:,i+2]
	        
	        merged = pd.merge(small_qty, small_turnover, on = 'name')
	        merged = merged[['Зміна кількості продаж','Зміна обороту']].reset_index().sort_values('Зміна обороту', ascending = True)
	     
	        
	    except:
	        small_qty = qty.iloc[:, i:]
	        small_qty['Зміна кількості продаж'] = qty.iloc[:,i] - qty.iloc[:,-1]
	        
	        small_turnover = turnover.iloc[:, i:]
	        small_turnover['Зміна обороту'] = turnover.iloc[:,i] - turnover.iloc[:,-1]
	        
	        merged = pd.merge(small_qty, small_turnover, on = 'name')
	        merged = merged[['Зміна кількості продаж','Зміна обороту']].reset_index().sort_values('Зміна обороту', ascending = True)
	    
	    merged = merged.rename(columns = {'name':'Назва товару'})

	    positive = merged[merged['Зміна обороту'] > 0].sort_values('Зміна обороту', ascending = False).reset_index(drop = True)
	    negative = merged[merged['Зміна обороту'] < 0].sort_values('Зміна обороту', ascending = True).reset_index(drop = True)

	    positive_df.append(positive.to_html(classes="table table-bordered table-hover posit"))
	    negative_df.append(negative.to_html(classes="table table-bordered table-hover negat"))


	return all_df, positive_df, negative_df, uniq_date





# dfs, pos, neg = main_script(date_from="2015-11-11", date_to="2015-11-18")

# for i in range(len(dfs)):
#     print(dfs[i], '\n')