#!/bin/bash

AUTH="--load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies"
URL="https://hydro1.gesdisc.eosdis.nasa.gov/data/WLDAS/WLDAS_NOAHMP001_DA1.D1.0/2020/01/WLDAS_NOAHMP001_DA1_20200102.D10.nc"

wget $AUTH --directory-prefix=WLDAS --content-disposition $URL

