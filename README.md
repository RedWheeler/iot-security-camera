# iot-security-camera

## Setup

This project uses conda to manage its dependencies. 
In order to easily setup your development environment, it is recommended you first install conda [here](https://docs.conda.io/en/latest/miniconda.html).

Setup your conda environment by running the following commands in the project's root directory:  
```shell script
conda env create -f environment.yml
conda activate iot-security-camera_env
```
 
## Starting the server

This project uses flask to handle HTTP requests.

Once your environment is activated, you can start the web server with the following commands:
```shell script
set FLASK_APP=server.py
flask run
```

### Debug mode

Debug mode can be enabled with flask to allow automatic reloads and error reporting. To enable debug mode, 
set the following environment variable before running:
```shell script
set FLASK_ENV=development
```

### Making the server visible

By default, `flask run` will make the server only accessible on your localhost. To make the server externally visible on 
your network, start the server with the following command:

```shell script
flask run --host=0.0.0.0
```

**Note - make sure debug mode is off if you do not trust others on your network**




