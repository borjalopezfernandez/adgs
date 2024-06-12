# README #

Data Exchange Component (DEC) for Auxiliary Data Gathering Service (ADGS).


### Docker image / container minARC ###

* Build gem in the repository
```
rake -f build_dec.rake dec:build[adgs,localhost,adgs_test_pg]
```

* Build app_adgs_auxip

```
docker build -f Dockerfile.adgs.dec.localhost.yaml -t app_adgs_dec:latest .
```

* Publish the image at in the google drive: [images folder](https://drive.google.com/drive/folders/1gKWJW90cuKxg3cKXoa8RJc-SK17J5Fzd?usp=drive_link):
```
docker save app_adgs_dec:latest > app_dec_minarc_<version>.tar
7z a app_adgs_dec_<version>.7z app_dec_minarc_<version>.tar
```

### minarc repository management


* Establish the development environment:

Create the following folders in the development environment:
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
