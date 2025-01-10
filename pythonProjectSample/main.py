from fastapi import FastAPI,status

from controller.user import user_route
from utils.utils import response_model

app = FastAPI()
app.include_router(user_route,prefix='/api',tags=['User'])

@app.get('/api/health')
def get_health():
    return response_model(status.HTTP_200_OK,{"message":"Application is working fine"})