npm start &

echo "
Tests take ~ 20s
The initial 'Connection failed... attempting reconnect' output is expected.
A testing coverage report is compiled after testing.
"

sudo python3 -m coverage run unit_test.py


echo "
Compiling testing coverage report...
Please wait...
"

sudo python3 -m coverage report -m | egrep -v "/usr|test"

sudo pkill electron
sudo pkill npm