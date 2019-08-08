import pandas as pd
import datetime as dt
import json, numpy, csv

def is_empty_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for i, _ in enumerate(reader):
            if i:  # found the second row
                return False
    return True

def init():
    with open('currentCars.csv', 'w+') as f:
        f.write('')
    with open('readerIndex.txt', 'w') as f:
        f.write(str(0))

    return None

def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

def np_convert(number):
    if isinstance(number, numpy.integer):
        return int(number)
    elif isinstance(number, numpy.floating):
        return float(number)
    else:
        return super(MyEncoder, self).default(number)



def currentCars():
    #open Current Cars and ReaderIndex
    if is_empty_csv('currentCars.csv'):
        currentCars = pd.DataFrame()
    else:
        currentCars = pd.read_csv('currentCars.csv')

    if len(currentCars) > 0:
        currentCars['mappedTime'] =  pd.to_datetime(currentCars['mappedTime'])

    with open('readerIndex.txt', 'r') as f:
        readerIndex = int(f.read())

    #read in all data
    csv_input = pd.read_csv('realtimeBSMs.csv')

    nRows = len(csv_input)

    #select unread section
    if readerIndex > nRows:
        print('readerIndex exceeds CSV')
        newRows = csv_input
    else:
        newRows = csv_input[readerIndex:]

    #add column for current time (when the instance was read)
    newRows['mappedTime'] = dt.datetime.now()

    #advance reader index
    readerIndex = len(csv_input)

    with open('readerIndex.txt', 'w') as f:
        if type(readerIndex) != int:
            print(type(readerIndex))
            print('not an int')
        f.write(str(readerIndex))

    #add new cars to currentCars
    currentCars = currentCars.append(newRows, ignore_index= True, sort=False)

    #clean up current cars
    #keep last known instance of ID only
    currentCars.drop_duplicates(subset=['BSM_tmp_ID'], keep='last', inplace=True)

    #drop old IDs, find the time x seconds ago
    x = 5
    maxAllowedTime = dt.datetime.now() - dt.timedelta(seconds=x)

    #remove IDs that are from before maxAllowedTime
    currentCars = currentCars[currentCars['mappedTime'] > maxAllowedTime]

    currentCars = currentCars.fillna(-1)

    currentCars.to_csv('currentCars.csv', index=False)

    currentCars = currentCars.drop(['mappedTime'], axis=1)

    currentCars[' X'] = currentCars[' X']/10000000
    currentCars[' Y'] = currentCars[' Y']/10000000

    cols = list(currentCars.columns)
    geojson = df_to_geojson(currentCars, cols, lat=' X', lon=' Y')

    return(str(json.dumps(geojson, indent=2, default=np_convert)))
