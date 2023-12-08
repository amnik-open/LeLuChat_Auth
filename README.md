# LeLuChat_Auth
This is a Microservice of LeLuChat project, that is responsible for authentication. It also listens
for RPC request to create different types of users. This project is a part of whole LeLuchat 
project. You can follow it [here](https://github.com/amnik-open/LeLuChat).
## Development Environment
### Build Docker Image
`docker compose build`

### Test API
`docker compose run auth python manage.py test`

### Run Development Server
`docker compose up`

### REST API Design
Rest API design can be seen by Swagger UI 
[here](https://amnik-open.github.io/LeLuChat_Auth/).

![LeLuChat Architecture](docs/LeLuChat_Auth.png)
