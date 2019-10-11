import pyowm
import json
import time
import pyodbc
import shutil
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=<servername>;'
                      'Database=Diabase;'
                      'Trusted_Connection=yes;')

x = conn.cursor()
city = '<city>'
timestr = time.strftime("%Y%m%d-%H%M%S")
owm = pyowm.OWM('<apikey>') 
sf = owm.three_hours_forecast(city+', NL')
f = sf.get_forecast()
keys = []
values = []
weather = {}

for weather in f:
      keys.append(weather.get_reference_time('iso'))
      values.append(weather.get_temperature(unit='celsius')['temp'])
weather = dict(zip(keys, values))

with open('weather'+timestr+'.json', 'w') as json_file:
  json.dump(weather, json_file, indent = 2, sort_keys=True)
  # close
shutil.move(json_file, 'D:\Python\Diabetes_Sara\import') 
x.execute("{CALL PrcInsertStagingWeather}")
conn.commit()
conn.close()
 
