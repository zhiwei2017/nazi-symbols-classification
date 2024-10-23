"""Main function for running the web service."""
# mypy: ignore-errors
import uvicorn
from app.application import create_application

app = create_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)  # nosec
