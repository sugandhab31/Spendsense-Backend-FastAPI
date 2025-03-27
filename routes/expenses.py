import models.models as models
import utils.auth as auth
import models.basemodels as basemodels
from fastapi import Request, APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from utils.database import get_db

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)] 

@router.post('/addexpense/')
def addexpense(expenses: basemodels.ExpensesBase, db: db_dependency, request: Request):
    try:
        headers = dict(request.headers)
        query_params = dict(request.query_params)
        res = auth.verify_token(query_params['userid'], headers['token'], db)
        print(res)
        db_expense = models.expenses(
            expense_name = expenses.expense_name,
            expense_amount = expenses.expense_amount,
            expense_currency = expenses.expense_currency,
            expense_category_id = expenses.expense_category_id,
            )
        db.add(db_expense)
        db.commit()
    except Exception as e:
        return e

@router.get("/getexpenses/")
def getexpenses(request: Request, db: db_dependency):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    res = auth.check_active_session(query_params['userid'], headers['authorization'], db)
    
    