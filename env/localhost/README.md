# README #

This README documents how to run the ADGS service in some *localhost* as development environment.

### Environment definition ###

* containers user adgs: uid=2020(adgs) gid=2020(adgs) groups=2020(adgs)
* host mount point in /data
* find /data/ -type d

```
/data/
/data/adgs
/data/adgs/dec
/data/adgs/dec/s2_aux
/data/adgs/dec/s3_aux_raw
/data/adgs/dec/log
/data/adgs/in_basket_if_localhost_notsecure
/data/adgs/tmp
/data/adgs/tmp/in_basket_if_nasa_eosdis_iers
/data/adgs/tmp/in_basket_if_noaa_ims
/data/adgs/arc
/data/adgs/arc/minarc_root
/data/adgs/arc/intray
/data/adgs/arc/minarc_error
/data/adgs/arc/log
/data/adgs/arc/tmp
/data/adgs/db
```


### Containers ###
## dec ##
* https://nexus3.elecnor-deimos.com/repository/NAOS-IVV/adgs/images/app_adgs_dec.7z

## minarc ##
* https://nexus3.elecnor-deimos.com/repository/NAOS-IVV/adgs/images/app_adgs_minarc.7z


