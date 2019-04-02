# RestWSAndSwagger2
## Restful WebServices to host weather information  
This application is used to host Weather Information using RestFul WebServices.

### Setup application in EC2 AWS 

* Create a folder at your convenient location and clone the repository.  
* Sign in to your AWS Account.  
* Follow the User guide documentation to launch Amazon EC2 Linux Instance.  
  [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance]  
* Once your instance is in running state, check if the status checks are passed. Then, connect to your instance using putty.  
[https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html]  
* Set up WinSCP to transfer files to your Linux instance. Steps are provided in the above link.  
* Once connected to WinSCP, transfer the project folder RestWSAndSwagger2 to /home/ec2-user/  

### Run your Application in Cloud
Now, set the current directory to /home/ec2-user/RestWSAndSwagger2/ in EC2 Console opened via putty.  
`cd /home/ec2-user/RestWSAndSwagger2/`  

Run `sudo python app.py`  
Now, Flask starts serving your app at port 80 by default.  
`app.run(host="0.0.0.0", port = 80)`  

### Access HomePage
Once your web server is up and running, use your public ip to access the homepage.  
This can be fetched from Description tab of Instances screen in EC2 console.

### Available Rest API Endpoints in detail  
#### [/historical/] - GET  
It will fetch all the dates for which weather information is available. This doesnot need any input parameter.  
It will return JSON Array of each and every date in YYYYMMDD format with 200 OK status.  
#### [/historical/`date`] - GET  
We need to pass date parameter in YYYYMMDD format. It will fetch that particular weather information if available in JSON array with 200 OK status. Else if data is not available, it will return 404 error code.  
#### [/historical/] - POST  
This is used to add or update the weather information for any particular date.  
We need to pass the data to be updated in request body in JSON format.  
i.e, by selecting Content-Type as application/json  
on success, it returns - JSON array with date added/updated with 201 Created statuscode.  
#### [/historical/`date`] - DELETE  
We need to pass date parameter in YYYYMMDD format. It will delete that particular weather information if available and returns 204 status. Else if data is not available, it will return 404 error code.  
#### [/forecast/`date`] - GET  
We need to pass date parameter in YYYYMMDD format. It will forecast weather for that particular week based on previous year's data with 200 status.  

### Sample Requests and Responses  

* GET - [http://myweatherapp.com/historical/]  
  * RESPONSE -  
    [  
    {"DATE": "20130101"},  
     {"DATE": "20130102"},  
     {"DATE": "20130103"},  
     ...  
     {"DATE": "20190327"}  
     ]  
     200 OK  

* GET - [http://myweatherapp.com/historical/20190327/]  
  * RESPONSE -   
    {  
        "DATE": "20190327",  
        "TMAX": "90.7",  
        "TMIN": "68.9"  
    }  
    200 OK  

* GET - [http://myweatherapp.com/historical/20190328/]  
  * RESPONSE -  
  404 Data Not Found  
  
* POST - [http://myweatherapp.com/historical/]  
  * REQUEST DATA (Content-Type:application/json) -  
    {  
        "DATE": "20190328",  
        "TMAX": "87.0",  
        "TMIN": "74.5"  
    }  
  
  * RESPONSE -  
    {"DATE": "20190328"}  
    201 Created  

* DELETE - [http://myweatherapp.com/historical/20190328/]  
  * RESPONSE - Deleted data of :20190328  
    204  
  
* DELETE - [http://myweatherapp.com/historical/20190331/]  
  * RESPONSE - Data for given Date Not Found    
    404  
  
* GET - [http://myweatherapp.com/forecast/20190302/]  
  * RESPONSE -  
    [  
        {  
            "DATE": "20190302",  
            "TMAX": "60.4",  
            "TMIN": "46.3"  
        },  
        {  
            "DATE": "20190303",  
            "TMAX": "58.7",  
            "TMIN": "41.5"  
        },  
        {  
            "DATE": "20190304",  
            "TMAX": "56.1",  
            "TMIN": "38.0"  
        },  
        {  
            "DATE": "20190305",  
            "TMAX": "58.0",  
            "TMIN": "44.6"  
        },  
        {  
            "DATE": "20190306",  
            "TMAX": "82.6",  
            "TMIN": "39.8"  
        },  
        {  
            "DATE": "20190307",  
            "TMAX": "52.9",  
            "TMIN": "46.5"  
        },  
        {  
            "DATE": "20190308",  
            "TMAX": "61.2",  
            "TMIN": "53.9"  
        }  
    ]  
    200 OK  
