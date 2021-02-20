# Disclaimer
This is not the best code in the world. This is just a tribute. The goal of this obviously to achieve greatness but on the way there will be experimentation lazyness and missteps. If you have a look at this code please bear this in mind.

# Global Explorer
Global Explorer is a game which teaches the player about the world and the workings of travel, the job market and possibly other things. You as a player is an indiviual exporing the world with the clothes on your back, your `curriculum vitae` and a limited amout of funds. Survive and have fun.

The project structure is mainly intended as a platform do the following: 
* Experiment with data structures and libraries
* Use python
* Use python decorators
* Use types in python
* Play with VUE.js as for DOM manipulation
* Use websockets

## To run (with podman)
The simplest way to run this system is by installing `podman` or `docker`. This setup has been tested only using `podman` in `Fedora 33`. Rootless `podman` has `not` been tested with success.

### In shell
```
sudo sh build-container.sh
sudo sh run-container.sh
```
### In container shell
```
sh start.sh
```

## To run (with docker compose)
It is so easy. Just make sure you have docker and docker-compose installed. Run the following commands in your shell.
```
docker-compose create
docker-compose up -d
```

## To run (without podman)
To run without podman the requirements are as follows:
* python
* libs: pyyaml and websockets

### In shell
Preferrably run these in separate shells to make it easy to shut them down separately
```
sh start-backend.sh
```

```
sh start-frontend.sh
```
## Access a running instance
The frontend can be accessed on http://localhost:3000 and the backend is hosted on port 5000.

## Legacy notes
This project previously used `pywebview` as a means of presenting the interface. It proved to be a cumbersome dependencies and has since been removed. The system now relies on a websocket server and a static webserver to present state and data in a standard browser.