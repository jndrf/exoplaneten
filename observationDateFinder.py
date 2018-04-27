def gregorianToJulian(cdate):
    '''
Converts a calender date in format YYY-MM-DDThh:mm:ss to Julian Date
Accepts only years in the gregorian calendar, i.e. years after 1582.

Might show deviations in the last shown digit due to numerical artifacts
    '''
    cdlist = cdate.split('T')[0].split('-')
    year = int(cdlist[0])
    month = int(cdlist[1])
    day = int(cdlist[2])

    try:
        tlist = cdate.split('T')[1].split(':')
        time = int(tlist[0])/24 + int(tlist[1])/1440 + float(tlist[2])/86400 
    except IndexError:
        time = 0

    # Check for gregorian Calendar
    assert(year>1582)
    
    if month <= 2:             
        year -= 1
        month += 12

    a = year//100
    b = 2 -a + a//4

    return round(int(365.25*(year+4716)) + int(30.6001*(month+1)) + day + time + b - 1524.5, 5)

def julianToGregorian(jdate):
    '''
converts a julian day number back do a gregorian calendar date
    '''
    f = jdate + 1401 + (((4*jdate + 274277)//146097)*3)//4 -38
    e = 4*f + 3
    g = (e % 1461) // 4
    h = 5*g + 2
    day = int((h % 153) // 5 + 1)
    month = int((h//153 + 2)%12 + 1)
    year = int(e//1461 - 4716 + (14 - month) // 12)
    cday = '{}-{:02d}-{:02d}'.format(year, month, day)

    jtime = jdate%1
    hour = int((12 + 24*jtime)//1)
    jtime -= (hour - 12)/24
    if hour>=24:
        day += 1
        hour -= 24
    minute = int((1440*jtime)//1)
    jtime -= minute/1440

    second = round(86400*jtime)

    ctime = '{:02d}:{:02d}:{}'.format(hour, minute, second)

    return 'T'.join([cday, ctime])

def findTransitDate(refValue, period, calendaric=False, **kwargs):
    '''
Gives times of planet transits as list (julian date)
@param revValue: reference transit date (julian)
@param period: orbital period (days)

optional parameters
@param start: start of observation period (julian date) use cstart for gregorian date
@param end: end of observation period, cend for gregorian date
@param n_transits: number of transits to show

@bug first entry of returned list may be before start date
    '''
    if 'start' in kwargs:
        n_min = (kwargs['start'] - refValue)//period
    elif 'cstart' in kwargs:
        n_min = (gregorianToJulian(kwargs['cstart']) - refValue)//period
    else:
        n_min = 0

    n_min = int(n_min)
    
    if 'n_transits' in kwargs:
        n_max = kwargs['n_transits'] + n_min
    elif 'end' in kwargs:
        n_max = (kwargs['end'] - refValue)//period
    elif 'cend' in kwargs:
        n_max = (gregorianToJulian(kwargs['cend']) - refValue)//period
    else:
        print('either n_transits, end or cend have to be given')
        assert(False)

    n_max = int(n_max)
    
    transitdates = [refValue + i*period for i in range(n_min, n_max+1)]
    
    return transitdates

if __name__ == '__main__':
    # testdate = '1994-12-17T18:19:20.3'
    # print(gregorianToJulian(testdate))
    # print(julianToGregorian(gregorianToJulian(testdate)))

    exoplanets = [
        {'name':'TrES-2', 'reference':2453957.635486, 'period':2.470613402, 'duration':1.83},
        {'name':'Qatar-1', 'reference':2.470613402, 'period':1.42003, 'duration':1.6 },
        {'name':'WASP-135', 'reference':2455230.9902, 'period':1.4013794, 'duration':1.7},
        {'name':'WASP-14', 'reference':2454463.57583, 'period':2.243752, 'duration':3.1},
        {'name':'Tres-5', 'reference':2455443.25153, 'period':1.4822446, 'duration':1.8}
    ]

    for planet in exoplanets:
        print(planet['name'])
        for transit in findTransitDate(planet['reference'], planet['period'], cstart='2018-05-07', cend='2018-05-21'):
            print(julianToGregorian(transit))

        print('\n\n----------')
