import fastapi

app = fastapi.FastAPI()


@app.get('/')
async def index():
    return { 'version': 1.0, 'payload': 'data' }
