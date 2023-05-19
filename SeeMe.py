import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn.objects as so
from datetime import datetime

class PropperRead:
    def __init__(self) -> None:
        pass
          
    def read_excel(self, file_address):
      """Read the timeshedules and return a DataFrame"""
      raw_file=pd.read_excel(file_address, engine='openpyxl')
      return raw_file
    
    def grouping(self, input_file):
        
        # grouping raw file into two level, as the "Level" is not required for weekly classification  
        D_L_grouped= input_file.groupby(['Date','Level'], as_index=False)['Hour'].sum()
        D_grouped= input_file.groupby(['Date'], as_index=False)['Hour'].sum()
        # format corrections
        D_L_grouped['Date_Dow'] = list(map(lambda x: x.day_name(),D_L_grouped.Date)) 
        D_L_grouped.Date = list(map(lambda x: x.date(),D_L_grouped.Date))
        D_grouped.Date = list(map(lambda x: x.date(),D_grouped.Date))
        
        DailyReport = D_L_grouped.pivot_table(values="Hour" , index=["Date", 'Date_Dow'] , columns="Level",fill_value=0)
        DailyReport['total']=DailyReport[1.0]+ DailyReport[2.0] +DailyReport[3.0]
        DailyReport['minutes']= (DailyReport['total']%1)*60
        DailyReport['Comb_Date']= list(map(lambda x,y: str(x)[-5:]+ ", " + str(y)[:3] , DailyReport.index.get_level_values(0),DailyReport.index.get_level_values(1)))
        DailyReport['Week'] = list(map(lambda x: x.isocalendar().week, D_grouped.Date)) 
        
        WeeklyReport= DailyReport.groupby(['Week'], as_index=False)['total',1.0,2.0,3.0].sum()
        return D_L_grouped,D_grouped,DailyReport, WeeklyReport
  

class Prettification():
    
    def graph_line(self, tbl_in):
        
        fig,ax = plt.subplots()
        sns.lineplot(x=tbl_in.Comb_Date,y= tbl_in.total, label='total')
        sns.lineplot(x=tbl_in.Comb_Date,y= tbl_in[1.0], label='level 1', linestyle='dotted')
        sns.lineplot(x=tbl_in.Comb_Date,y= tbl_in[2.0], label='level 2', linestyle='dashed')
        sns.lineplot(x=tbl_in.Comb_Date,y= tbl_in[3.0], label='level 3', linestyle='dashdot')
        plt.xticks(rotation=45)
        plt.ylim(0,7)
        plt.legend()
        plt.show() 

    def graph_area(self, tbl_in):
        plt.stackplot(tbl_in.Comb_Date, tbl_in[1.0], tbl_in[2.0], tbl_in[3.0], labels=['Level 1','Level 2','Level 3'], alpha=0.6)
        sns.lineplot(x=tbl_in.Comb_Date,y= tbl_in.total, label='total', linestyle='dashed', color='r', alpha=.3, linewidth=4.0)
        plt.legend(loc='upper left')
        plt.xticks(rotation=45)
        plt.ylabel('Hours [h]')
        plt.title("Rojin's detailed study hours", fontsize=20)
        plt.show()
    
    def graph_bar(self, tbl_in):
        
        # Draw a nested barplot
        fig, ax = plt.subplots(nrows=1,ncols=1)
        sns.set_style('darkgrid')
        sns.catplot(data=tbl_in, kind="bar",
                        x="Week", y="total",  alpha=.6, height=6)
        ax.set( ylabel= "Total hours [h]")
        
        # g.set_axis_labels("", "Total hours [h]")
        ax2 = ax.twinx()
        # Add scales to both sides of the vertical axis
        # ax2 = g.twinx()
        ax2.set_ylabel("Total hours [h]")
        ax2.set_ylim(ax.get_ylim())
        ax.legend()
        plt.show()


    # sns.barplot(x=Date_Level_Sum.Date,y=Date_Level_Sum.Hour, hue= Date_Level_Sum.Level)
    # ax.bar(Detailed_Sum.index, Detailed_Sum[1.0])
    # ax.bar(Detailed_Sum.index, Detailed_Sum[1.0], bottom=Detailed_Sum[2.0])
    # ax.bar(Detailed_Sum.index, Detailed_Sum[1.0], bottom=Detailed_Sum[2.0]+Detailed_Sum[3.0])
    # print(Detailed_Sum.index[1].dayofweek())




url= r'C:\Users\rojin\Documents\Repo\Local Taks\Timesheets.xlsx'
classRead = PropperRead()
raw_table=classRead.read_excel(url)
Date_Level_Sum, Date_Sum, Detailed_Sum, Week_sum = classRead.grouping(raw_table)

graphed= Prettification()



print(Week_sum)
print(Detailed_Sum)

# graphed.graph_area(Detailed_Sum) 
graphed.graph_area(Detailed_Sum)