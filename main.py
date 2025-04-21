import uvicorn 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"project": "POKE QUEUE REQUEST"}
@app.get("/version")
async def root():
    return {"version": "0.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)