import numpy as np

def aqh(temp,pressure):
    """Call signatures::
    
    specificHumidity = aqh(temp,pressure)

    estimate specific humidity from dew point temperature and surface
    pressure over water
    INPUT:  temp     :: dew point temperature in Kelvin
            pressure :: surface pressure (Pa)
    OUTPUT: specHum  :: specific humidity (kg/kg)
  
    Author: Martin Losch, Dec 2006 (matlab) rewritten for python Mar 2015
    source: http://www.faqs.org/faqs/meteorology/temp-dewpoint
    """

    # constants
    # $$$   tqw    = 237.3;
    # $$$   tqi    = 265.5;
    # $$$   qsi    =  17.2694;
    Pa2hPa = 1e-2;
    T0  = 273.15 # K, reference temperature
    es0 = 6.11   # hPa, reference saturation vapor pressure (es at 0 deg C)
    lv  = 2.5e6  # J/kg, latent heat of vaporization of water 
    Rv  = 461.5  # J K/kg, gas constant for water vapor 
    #
    # $$$   TD = temp - 273.16;
    # $$$   specHum = es0*0.622/(pressure*Pa2hPa)*exp(qsi*TD/(TD+tqw))
    #
    #vapPresAir = rh*10**( (0.7859 + 0.03477*temp)/(1 + 0.00412*temp) + 2 )
    vapPresAir = es0 * np.exp( lv/Rv * (1/T0 - 1/temp) )
    specHum    = 0.622*vapPresAir/(pressure*Pa2hPa + 0.378*vapPresAir);  
    
    return specHum

def lwdown(atemp,clouds):
    """Call signature::
    lwd = lwdown(atemp,clouds)
    estimate downward (incoming) radiation in long wave wave band from air 
    temperature according to Parkinson and Washington (1979), A Large-Scale 
    Numerical Model of Sea Ice, JGR, 84(C1), 311-337.

    INPUT:  atemp   :: air temperature in Kelvin
            clouds  :: fractional cloud cover, range: [0 1]
     OUTPUT: lwd     :: down ward long wave radiation (positive down)

     Author: Martin Losch, Dec 2006 (rewritten for python in Mar 2015)
    """

    # some constants
    stefanBoltzmann = 5.670e-8  # W/m^2/K^4
  
    # first long wave downward radiation (eq. 5 of P&W, who cite Idso and
    # Jackson, 1969)
    lwd = stefanBoltzmann*atemp**4 \
        * ( 1- 0.261*np.exp(-7.77e-4*(273-atemp)**2)) \
        * ( 1 + 0.275 * clouds )

    return lwd
  
def swdown(lon,lat,tdew,clouds,myTime):
    """Call signature::
    swd = swdown(lon,lat,atemp,clouds,myTime)
    estimate downward (incoming) radiation in short wave band from dew point
    temperature, cloud cover and astonomical parameters according to
    Parkinson and Washington (1979), A Large-Scale Numerical Model of Sea
    Ice, JGR, 84(C1), 311-337.

    INPUT:  tdew    :: dew point temperature in Kelvin
            clouds  :: fractional cloud cover, range: [0 1]
            lon,lat :: geographical coordinates (same dimensions as
                       tdew/clouds)
             myTime  :: current time in seconds (since Jan 01 00:00)
    OUTPUT: swd     :: down ward short wave radiation (positive down)

    Author: Martin Losch, Dec 2006 (rewritten for python in Mar 2015)
    """
    # check shape of arrays
    if np.prod(lat.shape) != np.prod(tdew.shape):
        errstr = (  "dimensions do not match: \n lat.shape = " 
                    + str(lat.shape) 
                  + ", but tdew.shape = " + str(tdew.shape) )
        raise RuntimeError(errstr)

    # some constants
    solarConstant   = 1353      #  W/m^2
    deg2rad         = np.pi/180
    secsInYear      = 31536000  # 365 days
    secsInDay       = 86400
    longestDay      = 172       # Jun21 for a 365day-year
  
    # handle time
    dayOfYear  = np.floor(np.mod(myTime,secsInYear)/secsInDay)
    solarTime  = np.mod(np.mod(myTime,secsInYear),secsInDay)
  
    # eq. 1-4 (Zillmann (1972) equation for 
    # cloudless skies, modified by a cloudiness factor according to 
    # Laevastu (1960))
  
    # cosine of solar zenith angle Z
    phi         = lat*deg2rad
    declination = 23.44*deg2rad*np.cos((longestDay-dayOfYear)*deg2rad)
    hourAngle   = (12*3600-solarTime)*np.pi/(12*3600)
    cosZ        = np.sin(phi)*np.sin(declination) \
        +         np.cos(phi)*np.cos(declination)*np.cos(hourAngle)
    cosZ = np.maximum(cosZ,0.)
    TD = tdew-273.16 # should be dew point temperature in Celsius
# $$$   A =   7.5 # for use in vapor pressure
# $$$   B = 237.3 # with respect to WATER
# $$$ # $$$   A =   9.5 # for use in vapor pressure
# $$$ # $$$   B = 265.5 # with respect to ICE
# $$$   vaporPressure = 6.1078e-5 * 10**((TD * A)/(TD + B))
  # vaporPressure (evap) according to atmos.f of mom2:
    vaporPressure = 6.1078e-5 * np.exp(19.*TD/(TD + 250))
		   
    swd = solarConstant*cosZ**2 * (1 - 0.6*clouds**3)/ \
        ( (cosZ+2.7)*vaporPressure + 1.085*cosZ + 0.10)
  
    return swd
