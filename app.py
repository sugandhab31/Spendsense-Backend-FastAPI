from fastapi import FastAPI, Depends
from typing import Annotated
import models.models as models
from dao.db_config import engine, get_db
from sqlalchemy.orm import Session
import uvicorn
from routes.expenses import router as expenses_router
from routes.user import router as users_router

app = FastAPI()
app.include_router(expenses_router)
app.include_router(users_router)
models.Base.metadata.create_all(bind = engine)

# This base class contains a metadata attribute (Base.metadata), which collects information about all the tables and models defined.
# You use Base.metadata.create_all(engine) to create all tables in the database according to the defined models.

db_dependency = Annotated[Session, Depends(get_db)] 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 