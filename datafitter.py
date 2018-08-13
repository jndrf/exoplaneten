import numpy as np
import matplotlib.pyplot as plt

from pandas import read_csv
from scipy.optimize import curve_fit

def transitModel(t, iTransit, iStar, t3rdContact, t4thContact, duskParam):
    '''
fugly hack to make the picewise definition work, should be pretty slow

still wont fit it.
    '''
    t = np.asarray(t)
    conditions = [
        t < t3rdContact,
        np.logical_and(t > t3rdContact, t < t4thContact),
        t > t4thContact
    ]

    functions = [
        lambda t: iTransit  + np.exp(t*duskParam),
        lambda t: (iTransit + (iStar - iTransit)/(t4thContact - t3rdContact) * (t - t3rdContact)) + np.exp(t*duskParam),
        lambda t: iStar + np.exp(t*duskParam)
    ]

    return np.piecewise(t, conditions, functions)

intab = read_csv('Measurements.csv')

timelist = intab.JD_UTC.subtract(58253)
params = curve_fit(transitModel, timelist, intab.rel_flux_T1, sigma=intab.rel_flux_err_T1, p0=[25, 27, 0.92, 0.95, .5], bounds=([24, 25, 0.91, 0.92, -np.inf], [27, 28, 0.94, 0.96, np.inf]))

print(params[0])
print(params[0][3])
covmat = params[1]
deptherror = np.sqrt(covmat[2][2]*params[0][3]**-2 + params[0][2]**2 / (params[0][3]**4)*covmat[3][3])
print('transit depth\t {depth:.3} +- {de:.3}\n3rd Contact\t {t3:.4} +- {e3:.3}\n4th Contact\t {t4:.4} +- {e4:.3}'.format(depth=1-params[0][0]/params[0][1], t3=params[0][2], t4=params[0][3], de=deptherror, e3=np.sqrt(covmat[2][2]), e4=np.sqrt(covmat[3][3])))
time_fine = np.linspace(timelist.iloc[0], timelist.iloc[-1], 10000)
plt.errorbar(timelist, intab.rel_flux_T1, intab.rel_flux_err_T1, fmt='.')
plt.plot(time_fine, transitModel(time_fine, *params[0]))
plt.xlabel('Geocentric Julian Date (UTC) - 58253')
plt.ylabel('flux [a.u.]')


plt.show()
