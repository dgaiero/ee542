docker run --name webfrontend --device /dev/video0 -v $PWD/app:/app -p 80:5000 -p 7560:7560 docker-flask:latest 
