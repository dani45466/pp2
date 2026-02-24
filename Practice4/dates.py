import datetime as dt

print(dt.datetime.now()-dt.timedelta(days=5))



print(dt.datetime.now()-dt.timedelta(days=1)) #yesterday
print(dt.datetime.now()+dt.timedelta(days=1)) #tomorrow
print(dt.datetime.now()) #today



print(dt.datetime.now().replace(microsecond = 0))



date1=dt.datetime.strptime(input(), "%Y-%m-%d %H:%M:S%")
date2=dt.datetime.strptime(input(), "%Y-%m-%d %H:%M:S%")
print(abs(date2-date1).total_seconds())