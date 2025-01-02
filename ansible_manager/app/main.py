from fastapi import FastAPI
from app.routes import ansible_routes

app = FastAPI(title="Ansible Manager API")

app.include_router(ansible_routes.router, prefix="/api/ansible", tags=["ansible"]) 