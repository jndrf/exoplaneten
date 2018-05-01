def fractionOfDay(stime):
    '''
    converts a hh:mm:ss time string to the fraction of a day
    '''
    tlist = stime.split(':')

    time = int(tlist[0])/24 + int(tlist[1])/1440 + float(tlist[2])/86400

    return time % 1

def gregorianToJulian(cdate):
    '''
    Converts a calender date in format YYY-MM-DDThh:mm:ss to Julian Day Number
    Accepts only years after 1582 and assumes the calendar to be gregorian
    Time can be omitted
    '''
    cdlist = cdate.split('T')[0].split('-')
    year = int(cdlist[0])
    month = int(cdlist[1])
    day = int(cdlist[2])

    try:
        time = fractionOfDay(cdate.split('T')[1])
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
    converts a julian day number back to a gregorian calendar date

@return string yyyy-mm-ddThh:mm:ss number of year digits not constrained
    '''
    jtime = jdate %1
    jdate = jdate            # strip part of day


    f = jdate + 1401 + (((4*jdate + 274277)//146097)*3)//4 -38
    e = 4*f + 3
    g = (e % 1461) // 4
    h = 5*g + 2
    day = int((h % 153) // 5 + 1)
    month = int((h//153 + 2)%12 + 1)
    year = int(e//1461 - 4716 + (14 - month) // 12)

    # l = jdate + 68569
    # n = (4*l)//146097
    # l = l - (146097*n + 3)//4
    # i = (4000 * (l + 1))//1461001
    # l = l - (1461*i)//4 + 31
    # j = (80*l)//2447

    # day = int(l-(2447*j)/80)
    # l = j//11

    # month = int(j + 2 - 12*l)
    # year = int(100*(n -49) + i + l)
    hour = int((12 + 24*jtime )//1)
    jtime -= (hour - 12)/24
    if hour>=24:
        day += 1
        hour -= 24
    minute = int((1440*jtime)//1)
    jtime -= minute/1440

    # deal with different length of months and leap years

    leapyear = ((year%4==0) and (year%100 != 0))
    if not leapyear:
        leapyear = (year%400 == 0)
    if month in [4, 6, 9, 11] and day > 30:
        month += 1
        day -= 30
    elif month ==2:
        if leapyear:
            if day >29:
                print('moep')
                day -= 29
                month += 1
        elif day > 28:
            print('se')
            day -= 28
            month += 1
        

    second = round(86400*jtime)

    cday = '{}-{:02d}-{:02d}'.format(year, month, day)

    ctime = '{:02d}:{:02d}:{:02d}'.format(hour, minute, int(second))

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


def isObservable(jdate, dusk, dawn, duration=1, rim=1):
    '''
    Checks whether the transit at jdate is observable, i.e. whole of 
    transit plus rim hours (default one) at each end is between dusk and dawn.

@param dusk, dawn: times given in 'hh:mm:ss' format
    @param duration: duration of transit in hours
    '''
    jdusk = fractionOfDay(dusk) + .5     # 'cause midnight is at .5
    jdawn = fractionOfDay(dawn) + .5

    jdusk = jdusk % 1
    jdawn = jdawn % 1

    ostart = (jdate - duration/48 - rim /24) %1
    oend = (jdate + duration/48 + rim /24) %1

    # print('jdusk {}\njdawn {}\nostart {}\noend  {}'.format(jdusk, jdawn, ostart, oend))
    return ostart > jdusk and ostart < jdawn and oend > jdusk and oend < jdawn

if __name__ == '__main__':
    exoplanets = [              # List of exoplanets. period in days, duration in hours
        {'name':'TrES-2', 'reference':2453957.635486, 'period':2.470613402, 'duration':1.83},
        {'name':'Qatar-1', 'reference':2455518.4102, 'period':1.42003, 'duration':1.6 },
        {'name':'WASP-135', 'reference':2455230.9902, 'period':1.4013794, 'duration':1.7},
        {'name':'WASP-14', 'reference':2454463.57583, 'period':2.243752, 'duration':3.1},
        {'name':'Tres-5', 'reference':2455443.25153, 'period':1.4822446, 'duration':1.8}
    ]

    print('''
Night-time transits between 2018-05-07 and 2018-05-21. (Planet list hardcoded)
Times for Dusk and Dawn are from the last observation day for the Calo Alto Observatory.
All times are UT.
    ''')
    for planet in exoplanets:
        print(planet['name'])
        for transit in findTransitDate(planet['reference'], planet['period'], cstart='2018-05-07', cend='2018-05-21'):
            if isObservable(transit, '21:01:00', '03:11:00', 1):
                print(julianToGregorian(transit))

        print('\n----------')

#    print(gregorianToJulian('2018-05-01T01:29:00'))
#    print(julianToGregorian(2457448.24543))
