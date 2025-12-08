This was built using Python 3.9
If you are having issues with SSL certifications try using Python 3.9 or updating ssl certificates,
If you are still experiencing issues try using in a python 3.9 virtual environment.

# Getting started 

How to set up the python virtual environment
```shell
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```
### Setting up the .env
The .env file requires the following:
EPC_ENCODED_API_TOKEN
OS_API_KEY

#### How to get your EPC_ENCODED_API_TOKEN

- You need to set an account with EPC open data communities [sign up/in](https://epc.opendatacommunities.org/login)
- Make an API call using postman for example 
    - end point: https://epc.opendatacommunities.org/api/v1/domestic/search
    - Authorisation type: Basic auth
    - Username: your email you signed up with
    - Password: Your API key from EPC open data account
- You should be able to find your EPC_ENCODED_API_TOKEN in your 'authorization'

#### How to get your OS_API_KEY
- you need to set up an account with OS datahub [sign up/in](https://osdatahub.os.uk/)
- Use the data exploration licence Data Exploration Licence | OS Licensing [found at](https://www.ordnancesurvey.co.uk/licensing/data-exploration-licence)
- create a new project on datahub with OS Places API and OS NGD Features API 
- copy the project key into .env  

# To run app

```shell
flask run
```

