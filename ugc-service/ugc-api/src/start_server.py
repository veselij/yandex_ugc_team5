from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from api.v1.films import router

app = FastAPI(
    title="API film watch timestamp",
    description="API service for receiving film watch timestamp",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(router, prefix="/api/v1", tags=["Films"])

if __name__ == "__main__":
    uvicorn.run(app=app, debug=True, host="127.0.0.1", port=8000)
