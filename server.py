from enum import Enum

import fastapi
from python_on_whales import DockerClient

app = fastapi.FastAPI()

class ServiceEnum(str, Enum):
    web = "web"
    backend = "backend"

@app.post('/restart/{service}', summary='Restart service')
async def run(service: ServiceEnum):
    docker = DockerClient(compose_files=[f'docker-compose.{service}.yaml'])
    docker.compose.down(timeout=1)
    docker.compose.up(detach=True)

@app.post('/down/{service}', summary='Stop service')
async def run(service: ServiceEnum):
    docker = DockerClient(compose_files=[f'docker-compose.{service}.yaml'])
    docker.compose.down(timeout=1)

@app.post('/pull/{service}', summary='Pull docker image and restart service')
async def run(service: ServiceEnum):
    docker = DockerClient(compose_files=[f'docker-compose.{service}.yaml'])
    docker.compose.down(timeout=1)
    docker.pull(f'{service}')
    docker.compose.up(detach=True)

@app.post('/logs/{service}', summary='Get service logs')
async def run(service: ServiceEnum):
    docker = DockerClient(compose_files=[f'docker-compose.{service}.yaml'])
    logs = docker.compose.logs()
    return fastapi.Response(content=logs, headers={ 'Content-Type': 'text/plain' })
