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


if __name__ == '__main__':
    print(calendarToJulian('2018-04-19T15:08:01'))
