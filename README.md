# mitx-utilities
A set of utilities for MIT EDX courses.

## Requirements
Docker

## compare_trajectories
A test to see how similar a student's answer is to previously submitted, correct answers.

First, to run this, you must generate an RSA server certificate and key. Run the following commands to do so: `openssl req  -nodes -new -x509  -keyout server.key -out server.crt`.

Then, modify `config.ini` to contain the location of the correct, previously submitted answers. By default, the previous submissions are stored in the folder `data/`. There are sample files in this folder to demonstrate. They should be deleted.

Then, run the following command from the root directory of the project. This will preprocess the data:
```
docker build -f Dockerfile.pre -t pre . &&
docker run -d --name pre pre &&
docker cp pre:/data/STORAGE data/STORAGE
```

Then, you must build the main docker container as follows: `docker build -t edx .`

To run the docker container, input the command: `docker run -dit --name edx -p 443:443 -p 80:80 edx`

Then the server will run in the background. Proceed to `https://localhost/similarity_iframe.html` (this will change depending on the whether the server has a permanent url on the host machine).

To stop the server, input the following command: `docker stop edx`

The server runs on port 443 for SSL connections and port 80 for non-SSL. To set up a permanent link to the server, configure the host machine to listen to the ports and then make the data public.

The default server name is "www.edx-interventions". To change this, replace `www.edx-interventions` with the desired name from the line `ServerName www.edx-interventions` in `dev.conf`.
