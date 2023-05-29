from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
import boto3
import os
from uuid import uuid4
import time

app = FastAPI()
handler = Mangum(app)

#Get dynamoDB table 
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

# Create pydantic model
class TaskModel(BaseModel):
    data: str
    task_id: Optional[str] = None
    user_id: Optional[str] = None
    done: bool = False

@app.get("/")
async def root():
    return {"message": "GET"}

@app.get("/get_task/<str:task_id>")
async def get_task(task_id):
    item = table.get_item(Key={"task_id": task_id}).get("Item")
    if not item:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    else:
        return {"task": item}

@app.delete("/delete_task/<str:task_id>")
async def delete_task(task_id):
    item = table.delete_item(Key={"task_id": task_id})

    if not item:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    else:
        return {f"Task {task_id} deleted!"}

@app.post("/create_task")
async def create_task(task_request: TaskModel):
    task_item = {
        "user_id": task_request.user_id,
        "task_id": uuid4().hex,
        "data": task_request.data,
        "created_time": int(time.time()),
        "done": False
    }

    table.put_item(Item=task_item)
    return {"task_item": task_item}

@app.put("/update_task")
async def update_task(task_request: TaskModel):
    response = table.update_item(
                Key={"task_id": task_request.task_id},
                UpdateExpression="set data=:d",
                ExpressionAttributeValues={
                    ':d': task_request.data},
                ReturnValues="UPDATED_NEW")

    return response['Attributes'] 
