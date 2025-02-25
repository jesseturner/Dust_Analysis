#!/bin/bash

#--- Capture argument from dust_vs_wldas.py script
DATE_VAR=$1 #--- in YYYYMMDD format
YYYY=${DATE_VAR:0:4}
MM=${DATE_VAR:4:2}
DD=${DATE_VAR:6:2}

AUTH="--load-cookies $HOME/.urs_cookies --save-cookies $HOME/.urs_cookies --keep-session-cookies"
URL="https://hydro1.gesdisc.eosdis.nasa.gov/data/WLDAS/WLDAS_NOAHMP001_DA1.D1.0/$YYYY/$MM/WLDAS_NOAHMP001_DA1_${YYYY}${MM}${DD}.D10.nc"


wget $AUTH --directory-prefix=WLDAS --content-disposition $URL

