from fastapi import FastAPI

app = FastAPI(
    title="Support Ticket System",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "message": "Support Ticket System API is running"
    }


    