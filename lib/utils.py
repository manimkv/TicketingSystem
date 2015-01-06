from datetime import datetime
from calendar import monthrange

def get_relative_dates(month, year):
    if month:
        start_date = datetime.strptime('%s%s01' % (year, '0%s' % month if month<10 else month) , '%Y%m%d')
        end_date = datetime.strptime('%s%s%s' % (year,  '0%s' % month if month<10 else month, monthrange(year, month)[1]) , '%Y%m%d')
    else:
        start_date = datetime.strptime('%s0101' % year , '%Y%m%d')
        end_date = datetime.strptime('%s1231' % year, '%Y%m%d')	
    return start_date, end_date