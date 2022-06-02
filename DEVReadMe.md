## Install python if you dont have it yet

#### Navigate to the project dir

#### Start with creating a virtual environment with this command
* `python -m venv uplanddev`
  
## Activate the virtual enviroment
* Windows CMD `uplanddev\Scripts\activate.bat`
* Windows POWERSHELL `uplanddev\Scripts\Activate.ps1`
* If sucessfull your command promt should display as the following `(uplanddev) {Path to the current folder}`

#### Then install all the requires libraries with this command 
* `pip install -r requirements.txt`
  

### The application should now be ready to start
### Start the application with this command, you can change the port number if you want
* `uvicorn main:app --port 8090 --reload`
* If everything starts sucessfully you sould see the follow 
* ```
    INFO:     Will watch for changes in these directories: ['Path to the file']
    INFO:     Uvicorn running on http://127.0.0.1:8090 (Press CTRL+C to quit)
    INFO:     Started reloader process [14872] using statreload
    WARNING:  The --reload flag should not be used in production on Windows.
    INFO:     Started server process [28084]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```

### You can now navigate to {http://127.0.0.1:8090/docs} to see the Swagger Doc.


## Making the local endpoint externally accessable

### Download ngrok if you do not have it yet {https://ngrok.com/}
* unzip the file and place it somewhere, you can remember
* You can either add the dir to your enviroment PATH, or just use the app from the folder
- To Use the app from the folder 
  * navigate to the unziped folder and type the following command `ngrok http 8090` remember to change the port if you did in the previouse commands
  * If sucessfull you should get the following output:
   ```
    Version	3.0.4
    Region	Europe (eu)
    Latency	22ms
    Web Interface	http://127.0.0.1:4040
    Forwarding	https://dddb-2003-f8-973e-21sd0-7d17-8e5f-a559-9456.eu.ngrok.io -> 
    ```
    *  The previously Swagger doc can now also be access throw {https://dddb-2003-f8-973e-21sd0-7d17-8e5f-a559-9456.eu.ngrok.io/docs}


    * https://dddb-2003-f8-973e-21sd0-7d17-8e5f-a559-9456.eu.ngrok.io/upland/webhook
  
