
# Python Implementation of the XenquAPI

## Installation
    pip install xenqu-api

## Usage
    from xenqu import XenquAPI

    api = XenquAPI(
        clientId=os.getenv('CLIENT_ID'), 
        clientSecret=os.getenv('CLIENT_SECRET'), 
        pemPrivateKey=open('./privatekey.pem', 'rb').read(), 
        subscriber=os.getenv('SUBSCRIBER')
        )

    userInfo = api.account.getUserInfo()

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