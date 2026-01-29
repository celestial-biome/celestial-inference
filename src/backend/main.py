from fastapi import FastAPI

app = FastAPI(title="Celestial Inference API")

@app.get("/")
def read_root():
    return {"status": "ok", "project": "celestial-inference"}
    