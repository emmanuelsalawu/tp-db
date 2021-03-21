# Therapeutic Peptide Design Database (TP-DB)
We make all the executables, python source codes, and prebuilt databases for the Therapeutic Peptide Design Database (TP-DB, https://dyn.life.nthu.edu.tw/design) available through GitHub (https://github.com/emmanuelsalawu/tp-db) under the Apache License, Version 2.0 (https://www.apache.org/licenses/LICENSE-2.0). 

Kindly note that, for a general use case, **there is no need to directly download any of the files located in the links above**. They are provided for transparency. All downloads are directly handled in step 3 below, which contains a command that handles the downloading (of a 10 GB Docker image the first time the command is run) and its execution. For subsequent execution of the command (regardless of the query), the already downloaded docker image is loaded and performs the search with the results returned in a couple of minutes (which is slower than our webserver, see step 3 below for the reasons).

## About Docker 
Docker makes it possible to share prebuilt computation environment for a software so that all users can have all the required dependencies and libraries running in their local computers. For this reason, we provide a docker image for TP-DB (emmanuelsalawu/tp-db). Although the TP-DB is made available through Docker Hub (https://hub.docker.com/r/emmanuelsalawu/tp-db), **we strongly recommend that users follow step 3 below for the downloading and the execution of the docker image**. On the other hand, if desired, a user can extract/export all the codes and the databases from the docker image. We make the relevant contents of the docker image available here https://drive.google.com/drive/u/1/folders/1lEZR0JQ5NnTWA5lDhAP2MEtptMgXVs8k on Google Drive for reference. 


## Using TP-DB Online 
The easiest way for a general user to use the Therapeutic Peptide Design Database (TP-DB) is through the version we host online at https://dyn.life.nthu.edu.tw/design. Nonetheless, all the results of the version we are hosting can be reproduced and even extended through the executables, python source codes, and prebuilt-databases.

## Using TP-DB Locally, on Your Computer
To use TP-DB on your local machine, we recommend using docker. The steps are as follows.

### [1] System Requirements 
You would need a Mac, a Windows, or a Linux computer with at least 4 GB RAM, and 20 GB free disk space in which the docker image containing the database files can be saved. 
This version of TP-DB has been tested on Mac OS (version 10.14.6), Windows (version 10), and Linux (Ubuntu 20.04) computers. 

### [2] Download and install Docker
Docker can be downloaded and installed by following the guidelines available on their website at https://docs.docker.com/get-started/. Specific download links are also provided below. <br/>
[a] Download Docker Desktop for Mac: https://desktop.docker.com/mac/stable/Docker.dmg 
[b] Download Docker Desktop for Windows: https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe 
[c] Install Docker Engine on Linux: https://docs.docker.com/engine/install/ 

### [3] Run TP-DB / Demo 
NOTE: The first time you run TP-DB using the command below, a docker image would be downloaded. This may require about 10GB (for a first-time user) data transfer through the internet. Depending on your internet connection, this may take about 30 minutes, which includes the download time and the execution time. However, subsequent running of the program with different queries makes use of the already downloaded TP-DB docker image and would run faster finishing between 2 to 5 minutes depending on your system’s configuration. 

Please note that the processing of each query is much faster when using the version hosted on our server (https://dyn.life.nthu.edu.tw/design) because the databases have been preloaded in the server’s memory and the server responds to the queries that arrive. On the other hand, the local version that the user may run through docker needs to reload the databases each time, making it much slower than the webserver we provide.  

Go to your computer’s terminal and execute the following. (The appropriate terminal on a Windows machine could be the command prompt window that is running with an administrator privilege, and would not require “sudo” at the beginning of the command.)

`sudo docker run -v "/Users/esalawu/tp-db:/var/tp-db" emmanuelsalawu/tp-db /bin/bash -c "./loadDbAndListenJuly22.exe &> /dev/null & sleep 10 && /usr/local/miniconda2/bin/python query.py --query 'A/E 0,4 D 2,3 E 2,3 H' --output /var/tp-db/result; echo 'Done. Now exiting'; exit "`

#### Explanations of What this Step [3] Does
The command above has the following components. You will need to change the parts in bold accordingly. 
sudo docker run \
-v "**/Users/esalawu/tp-db**:/var/tp-db" \
emmanuelsalawu/tp-db \
/bin/bash -c "./loadDbAndListenJuly22.exe &> /dev/null & sleep 10 && \
/usr/local/miniconda2/bin/python query.py \
--query '**A/E 0,4 D 2,3 E 2,3 H**' \
--output /var/tp-db/result; \
echo 'Done. Now exiting'; exit "


`sudo docker run` <br/>
This tells Docker engine that we want to run an instance.

`-v "/Users/esalawu/tp-db:/var/tp-db"` <br/>
This tells Docker engine that we want to mount a path/directory on our computer **/Users/esalawu/tp-db** to in the Docker instance and it should be visible as /var/tp-db within the Docker instance. Through this, we can easily write outputs from the docker instance into a location that is accessible outside of the docker instance and can be opened on the host computer.

`emmanuelsalawu/tp-db`<br/>
This is the name of the TP-DB docker image that is available in docker hub https://hub.docker.com/repository/docker/emmanuelsalawu/tp-db. It is downloaded the first time we run the command and remains available locally henceforth.

`/bin/bash -c "./loadDbAndListenJuly22.exe &> /dev/null & sleep 10 &&` <br/>
This loads the TP-DB database and listens for incoming query. It waits for a few seconds to ensure that everything is loaded before accepting the query.  

`/usr/local/miniconda2/bin/python query.py` <br/>
This submits the query.

`--query 'A/E 0,4 D 2,3 E 2,3 H'` <br/>
This '**A/E 0,4 D 2,3 E 2,3 H**' is the query.

`--output /var/tp-db/result;` <br/>
This is where the results would be written. 
Only the bold part needs to be changed. You would remember that with -v "**/Users/esalawu/tp-db**:/var/tp-db" above, we successfully mapped "**/Users/esalawu/tp-db**" in the host computer to "/var/tp-db" in the docker instance. Therefore, /var/tp-db/**result** actually points to **/Users/esalawu/tp-db/result**. *The result will be written to **/Users/esalawu/tp-db/result**_table.html*.

`echo 'Done. Now exiting'; `<br/>
This informs the user that the computations have finished. 

`exit"`<br/>
This closes the docker instance and frees the resources. 


### [4] Visualize the Results 
Navigate to the folder you specified in step 3. Open the html file in the folder. It will contain the results identical to the one that can be obtained by using the online TP-DB. Here https://dyn.life.nthu.edu.tw/design/result?JobID=60567ea2z is an example of the results page.

### [5] Removing the Docker Image and Freeing up the Disk 
When a user does not need TP-DB anymore, it is possible to delete TP-DB’s docker image and free up the used disk space by executing the following command.

`sudo docker image rm -f emmanuelsalawu/tp-db`

NOTE: Any subsequent use of TP-DB after this step will make docker to redownload TP-DP’s docker image as explained in step 3 above. 


## Diving Deeper
Python source codes for TP-DB are available through GitHub: https://github.com/emmanuelsalawu/tp-db where users can go through the codes and, if desired, copy and modify it to suit their needs. 


