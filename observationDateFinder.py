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
        time = int(tlist[0])/24 + int(tlist[1])/1440 + float(tlist[2])/86400 - 0.5
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
@bug: time output not correct
    '''
    f = jdate + 1401 + (((4*jdate + 274277)//146097)*3)//4 -38
    e = 4*f + 3
    g = (e % 1461) // 4
    h = 5*g + 2
    day = int((h % 153) // 5 + 1)
    month = int((h//153 + 2)%12 + 1)
    year = int(e//1461 - 4716 + (14 - month) // 12)
    cday = '{}-{}-{}'.format(year, month, day)

    jtime = jdate%1
    hour = int((12 + 24*jtime)//1)
    jtime -= (hour - 12)/24
    if hour>=24:
        day += 1
        hour -= 24

    minute = int((60*jtime)//1)
    jtime -= minute/60

    second = round(60*jtime, 2)

    ctime = '{}:{}:{}'.format(hour, minute, second)

    return 'T'.join([cday, ctime])

def findTransitDate(refValue, period, calendaric=False, **kwargs):
    '''
Gives times of planet transits as list (julian date)
@param revValue: reference transit date (julian)
@param period: orbital period (days)

optional parameters
@param calendaric: return list of calendar dates if true
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
    
    print(n_min)
    print(n_max)
    transitdates = [refValue + i*period for i in range(n_min, n_max+1)]
    
    return transitdates

if __name__ == '__main__':
    testdate = '2018-04-26'#T15:08:09'
    print(gregorianToJulian(testdate))
    print(julianToGregorian(gregorianToJulian(testdate)))
    print(findTransitDate(2453957.635486, 2.470613402, cstart='2018-05-07', cend='2018-05-21'))
