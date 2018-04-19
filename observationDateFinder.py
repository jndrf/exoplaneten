def calendarToJulian(cdate):
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

def findTransitDate(refValue, period, calendaric=False, **kwargs):
    '''
Gives times of planet transits as list (julian date)
@param revValue: reference transit date (julian)
@param period: orbital period (days)

optional parameters
@param calendaric: return list of calendar dates if true
@param start: start of observation period (julian date) use cstart for calendar date
@param end: end of observation period, cend for calendar date
@param n_transits: number of transits to show

    '''
    if 'start' in kwargs:
        n_min = (kwargs['start'] - revValue)//period
    elif 'cstart' in kwargs:
        n_min = (calendarToJulian(kwargs['cstart']) - revValue)//period
    else:
        n_min = 0

    if 'n_transits' in kwargs:
        n_transits = kwargs['n_transits']
    elif 'end' in kwargs:
        n_max = (kwargs['end'] - revValue)//period
    elif 'cend' in kwargs:
        n_max = (calendarToJulian(kwargs['cend']) - revValue)//period
    else:
        print('either n_transits, end or cend have to be given')
        assert(False)

    transitdates = [revValue+ i*period for i in range(n_min, n_transits+1)]

if __name__ == '__main__':
    print(calendarToJulian('2018-04-19T15:08:01'))
    print(transitdates(2453957.635486, 2.470613402, cstart='2018-05-07', cend='2018-05-21')
