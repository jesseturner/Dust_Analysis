#--- OPENDAP source: https://hydro1.gesdisc.eosdis.nasa.gov/opendap/WLDAS/WLDAS_NOAHMP001_DA1.D1.0/
#------ OPeNDAP is supposed to let me access the file while keeping it 
#------ on the NASA servers, but I haven't gotten this to work yet

import xarray as xr

url = "https://hydro1.gesdisc.eosdis.nasa.gov/opendap/WLDAS/WLDAS_NOAHMP001_DA1.D1.0/2001/01/"
file = "WLDAS_NOAHMP001_DA1_20010102.D10.nc"

ds = xr.open_dataset(url+file)
#subset = ds.sel(lat=slice(10, 20), lon=slice(30, 40))
print(ds.variables)
print(ds.attrs)