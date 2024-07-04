# Install ADGSFE
pip3 install --user -e "/adgsfe[tests]"

# Script to start the web server in development mode
npm --force --prefix /adgsfe/adgsfe/static install &> /log/npm.log
npm --prefix /adgsfe/adgsfe/static run build &>> /log/npm.log
nohup npm --prefix /adgsfe/adgsfe/static run test &>> /log/npm.log &

# Start flask server on port 5001 for SSL connection
# Create certificates if they are not available
if [ ! -f /resources_path/certificate.pem ] || [ ! -f /resources_path/key.pem ];
then
    openssl req -x509 -newkey rsa:4096 -nodes -out /resources_path/certificate.pem -keyout /resources_path/key.pem -subj "/emailAddress=daniel.brosnan@elecnor.es/C=SP/ST=Madrid/L=Tres Cantos/O=Elecnor Deimos/OU=Ground Segment/CN=BOA"
fi

# Start flask server on port 5000 for testing purposes
export ADGSFE_DEBUG=FALSE; export ADGSFE_TEST=TRUE; nohup flask run --host=0.0.0.0 -p 5000 &> /log/flask_5000.log &

export ADGSFE_DEBUG=TRUE; export ADGSFE_TEST=TRUE; nohup flask run --cert=/resources_path/certificate.pem --key=/resources_path/key.pem  --host=0.0.0.0 -p 5001 &> /log/flask_5001.log &

sleep infinity
