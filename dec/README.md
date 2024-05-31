# README #

Data Exchange Component (DEC) for Auxiliary Data Gathering Service (ADGS).

## Local deployment

### Prequisites

You will need to have the following installed locally to deploy locally the ADGS system:

- [Docker](https://docs.docker.com/install/)

### Quick start

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

** Build the DEC gem:
```
rake -f build_dec.rake dec:build[adgs,localhost,adgs_test_pg]
rake -f build_dec.rake dec:install[adgs,localhost,adgs_test_pg]
```

** Build the DEC image:

* Execute the following commands
```
rake -f build_dec.rake  dec:image_build[adgs,localhost,adgs]
```
* Publish the image in the google drive: [images folder](https://drive.google.com/drive/folders/1gKWJW90cuKxg3cKXoa8RJc-SK17J5Fzd?usp=drive_link)
```
docker save app_adgs_dec:latest > app_adgs_dec_<version>.tar
7z a app_adgs_dec_<version>.7z app_adgs_dec_<version>.tar
```
