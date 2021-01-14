# zoom_intigration
This POC is an example of procidure of integrating zoom apis to any project. This POC includes the following:
  1) zoom user authentication
  2) zoom creating meeting
  3) zoom chat

This POC uses apis provided by zoom. Paid accounts provide more functionality to these api (eg add more user to the app). Before using zoom apis, we need to create 
an OAuth app on zoom market (https://marketplace.zoom.us/develop/create) and use the client id of that app for authentication.
  
# Prerequisites
You will need the following programmes properly installed on your computer.<br>
Python 3.7+

# Installation and Running

clone the repository
```
git clone https://github.com/ongraphpythondev/zoom_intigration.git
cd zoom_intigration
```
create a vertual environment
```
python3 -m venv venv
source venv/bin/activate
```
install required packages
```
pip install -r requirements.txt
```
running
```
./manage.py runserver
```
### Note
Before running the the django project:
  1) change base_url in config.py 
  2) change 'Redirect URL for OAuth' in the zoom market app to be same as zoom_auth_callback_url from config.py 
  3) add the Redirect URL to 'Whitelist URL' in the zoom market app
  4) change redirect_uri in zoom_app/templates/login.html
