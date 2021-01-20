
# Python Implementation of the XenquAPI

This is the code for the python implementation of the Xenqu API by Essium, LLC.
The endpoints accessible are further documented [here](https://apidocs.xenqu.com). Before getting started also check [this](https://github.com/EssiumLLC/xenqu-rest-api) out.

## Installation
```shell
pip install xenqu-api
```

## Usage
```python
import os
from xenqu import XenquAPI

api = XenquAPI(
    clientId = os.getenv('CLIENT_ID'), 
    clientSecret = os.getenv('CLIENT_SECRET'), 
    pemPrivateKey = open('./privatekey.pem', 'rb').read(), 
    subscriber = os.getenv('SUBSCRIBER')
    )

userInfo = api.account.getUserInfo()
```

## Progress

| Sections             	| Scaffolded 	 | Implemented 	  | Tested 	   |
|----------------------	|--------------	 |-------------	  |----------  |
| Account              	| ✅          	| ✅           	| ✅      	|
| Contact              	| ✅          	| ✅           	| ✅      	|
| [Tracking] - Tabs    	| ✅          	| ✅           	| ✅      	|
| [Tracking] - Records 	| ✅          	| ✅           	| ✅      	|
| [Tracking] - Queues  	| ✅          	| ✅           	| ✅      	|
| [Tracking] - Items   	| ✅          	| ✅           	| ✅      	|
| Forms                	| ✅          	| ✅           	| ✅      	|
| Reports              	| ✅          	| ✅           	| ✅      	|
| Files                	| ✅          	| ✅           	| ✅      	|


## Problems

## Building
```shell
python setup.py sdist bdist_wheel

twine upload dist/*
```