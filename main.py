from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the amazing DERC Vision API!"}

@app.get(path="/camera/{camera_id}")
async def camera_list(camera_id=None):
  return {"cameras":[]}

