from fastapi import FastAPI
from mission_planner_router import mission_planner_router
import uvicorn
app= FastAPI()

app.include_router(mission_planner_router)

if __name__ == '__main__':
    uvicorn.run(app, port= 7000, host='0.0.0.0')