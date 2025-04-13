import pandas as pd
from datetime import datetime
import re
import numpy as np
days_of_week = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Понедельник'
}

day_column = 'Unnamed: 0' 

    
def get_schedule_for_today(excel_file, day_column, group_column):
    df = pd.read_excel(excel_file)
    df.columns = df.columns.str.strip()    
    today = datetime.now().weekday() 
    today_schedule = df[df[day_column] == days_of_week[today]]
    if not today_schedule.empty:
        start_index = today_schedule.index[0]  
        end_index = min(start_index + 20, len(df))  
        
        
        schedule_array = [] 

        
        pattern = re.compile(r'^[А-ЯЁ][а-яё]+s[А-ЯЁ].[А-ЯЁ].sАуд.sd{3}')

        for index, row in df.iloc[start_index:end_index].iterrows():
            time_slot = row['Unnamed: 1']  
            subjects = row[group_column]  
            
            
            if pd.isna(subjects):
                continue
            
            
            subjects_list = [subject.strip() for subject in str(subjects).split(',')]
           
            for subject in subjects_list:
                if pd.isna(time_slot):                                      
                    if schedule_array:
                        schedule_array[-1]['subject'] += f" {subject}"
                        

                else:
                    
                    schedule_array.append({ 'subject': subject})
   
        return schedule_array  
    else:
        return [] 



data= get_schedule_for_today("sheldure2.xlsx","Unnamed: 0","Unnamed: 3")
print(data)
