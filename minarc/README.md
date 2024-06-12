# README #

minimum archive (minARC) for Auxiliary Data Gathering Service (ADGS).

### Docker image / container minARC ###

* Build gem in the repository
```
rake -f build_minarc.rake minarc:build[adgs,localhost,adgs_test_pg]
```

* Build app_adgs_auxip

```
docker build -f Dockerfile.adgs.minarc.localhost.yaml -t app_adgs_minarc:latest .
```

* Publish the image at in the google drive: [images folder](https://drive.google.com/drive/folders/1gKWJW90cuKxg3cKXoa8RJc-SK17J5Fzd?usp=drive_link):
```
docker save app_adgs_minarc:latest > app_adgs_minarc_<version>.tar
7z a app_adgs_minarc_<version>.7z app_adgs_minarc_<version>.tar
```

* Test end-point availability

```
curl -k -v -u test:test --max-time 12000 --connect-timeout 60 --keepalive-time 12000 -L -f -s -X GET https://adgs_minarc:4567/dec/arc/requestArchive/*
```


### minarc repository management

* Establish the development environment:
** Create the following folders in the development environment:
```
mkdir ~/workspace
```
** Establish the needed repositories:
```
cd ~/workspace/
git clone https://borja_lopez_fernandez@bitbucket.org/borja_lopez_fernandez/dec.git
cd ~/workspace/dec/
git fetch
git pull origin
```

** Build the minARC gem:
```
rake -f build_minarc.rake minarc:build[adgs,localhost,adgs_test_pg]
rake -f build_minarc.rake minarc:install[adgs,localhost,adgs_test_pg]
