from fastapi import FastAPI

app = FastAPI()

# Import routes after app is created to avoid circular imports
from api import routes
