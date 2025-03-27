from fastapi import FastAPI, Depends
from typing import Annotated
import models
from database import engine, get_db
from sqlalchemy.orm import Session
import uvicorn
from routes.expenses import router as expenses_router

app = FastAPI()
app.include_router(expenses_router)
models.Base.metadata.create_all(bind = engine)

# This base class contains a metadata attribute (Base.metadata), which collects information about all the tables and models defined.
# You use Base.metadata.create_all(engine) to create all tables in the database according to the defined models.

db_dependency = Annotated[Session, Depends(get_db)]
    
'''
{
  "username": "string",
  "password": "string",
  "repeat_password": "string",
  "fullname": "string",
  "disbled": true
}
'''
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 