# Herodotus - Content Archival Software
![Herodotus](https://github.com/alaskanpuffin/herodotus-web/raw/master/src/assets/logo.png)

Herodotus has been designed as easy to use archival software, created to serve as an offline information reference when internet access in unavailable. Herodotus is not designed to be a personal "wayback machine", instead its focus is on providing a handy offline reference for text-based content. Powered by MeiliSearch, users are able to easily and quickly search archived content.

Herodotus has been designed with simplicity in mind. Whether disaster strikes and internet is unavaible, or you simply want an offline record of your favorite articles or personal notes, Herodotus provides a means of efficiently finding the necessary information when you need it most.

# Technical Details
The entire Herodotus project is split up between two repositories.
## Herodotus Core
The [Herodotus Core](https://github.com/alaskanpuffin/herodotus-core) repository contains all the backend code for the api and communications with the MeiliSearch server. The backend is written in Python and uses the [Django](https://www.djangoproject.com/) web framework. For the api, [Django Rest Framework](https://www.django-rest-framework.org/) is used along with [django-rest-knox](https://github.com/James1345/django-rest-knox) for authentication.

## Herodotus Web
The [Herodotus Web](https://github.com/alaskanpuffin/herodotus-web) repository contains the official front-end for the project. Powered by [Vue.js](https://vuejs.org/), Herodotus is a single page application designed for simplicity and usability. 

# Installation
Due to the split nature of Herodotus, the easiest method of installation is using Docker. Included in the root of this repository is a file named [docker-compose.yml](https://github.com/alaskanpuffin/herodotus-core/blob/master/docker-compose.yml). This file serves as a base template for getting Herodotus up and running.

## Setup Steps
- Install Docker Engine using the appropriate guide found [here](https://docs.docker.com/engine/install/).
- Install Docker Compose using the appropriate guide found [here](https://docs.docker.com/compose/install/).
- Copy [docker-compose.yml](https://github.com/alaskanpuffin/herodotus-core/blob/master/docker-compose.yml) to a directory on the machine.
- Replace the following environment variables in the docker-compose file:
  - <MEILI_MASTER_KEY> = MeiliSearch master key/password, can be any random string. There are two instances of this variable, both must be the same.
  - <SECRET_KEY> = Random key required by Django. Can be any random string.
  - <HERODOTUS-CORE-IP/HOSTNAME> = Change <HERODOTUS-CORE-IP/HOSTNAME> to the IP address or hostname of the server running herodotus. If the IP address or hostname of the server changes, you will need to update this value. Setting a static IP address on the server is recommended.
- After making the necessary changes, run `docker-compose up`. Note: Docker may require root priviledges, if you receive an error, try running the previous command as sudo. 
- Congratulations! Herodotus has been installed, you can access the web interface by opening the IP address or hostname of the server in a browser. The default user credentials are Username: `admin` Password: `admin`.

## Screenshots
![screen1](https://user-images.githubusercontent.com/38274055/93726297-b8db4a00-fb61-11ea-870c-1e21634c9b4e.jpg)

![screen2](https://user-images.githubusercontent.com/38274055/93726306-c1cc1b80-fb61-11ea-96af-064300e2c3a6.jpg)

![screen3](https://user-images.githubusercontent.com/38274055/93726303-bd076780-fb61-11ea-8481-fbd376114077.jpg)

![screen4](https://user-images.githubusercontent.com/38274055/93726305-c09aee80-fb61-11ea-9abf-5d72a9b2e480.jpg)

Demo Video: https://youtu.be/7BvKh9GpGXk


## Attribution
Icon by [Freepik](https://www.flaticon.com/authors/freepik)
