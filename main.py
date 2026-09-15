from fastapi import FastAPI

from app.api.routes.agent import router as agent_router


app = FastAPI(
    title="Business Central AI Agent"
)


app.include_router(agent_router)