import models
import auth
import basemodels
from App import db_dependency
from fastapi import Request, APIRouter

router = APIRouter()

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
    res = auth.verify_token(query_params['userid'], headers['authorization'], db)
    print(res)
    