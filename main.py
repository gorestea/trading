from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from auth.auth import auth_backend
from auth.db import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title='Trading App'
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)






#
# users = [
#     {'id': 1, 'role': 'admin', 'name': 'Bob'},
#     {'id': 2, 'role': 'investor', 'name': 'John'},
#     {'id': 3, 'role': 'trader', 'name': 'Matt', 'degree': [
#         {'id': 1, 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'}
#     ]}
# ]
#
#
# class DegreeType(Enum):
#     newbie = 'newbie'
#     expert = 'expert'
#
#
# class Degree(BaseModel):
#     id: int
#     created_at: datetime
#     type_degree: str
#
#
# class User(BaseModel):
#     id: int
#     role: str
#     name: str
#     degree: Optional[List[Degree]] = 'None'
#
#
# @app.get("/users/{user_id}", response_model=List[User])
# def get_user(user_id: int):
#     return [user for user in users if user.get('id') == user_id]
#
#
# all_trades = [
#     {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
#     {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12}
# ]
#
# class Trade(BaseModel):
#     id: int
#     user_id: int
#     currency: str = Field(max_length=5)
#     side: str
#     price: float = Field(ge=0)
#     amount: float
#
#
# @app.post('/trades')
# def add_trades(trades: List[Trade]):
#     all_trades.extend(trades)
#     return {'status': 200, 'data': all_trades}
#
#
# # @app.post('/trades')
# # def get_trades(limit: int = 1, offset: int = 0):
# #     return trades[offset:][:limit]
#
#
# # users2 = [
# #     {'id': 1, 'role': 'admin', 'name': 'Bob'},
# #     {'id': 2, 'role': 'investor', 'name': 'John'},
# #     {'id': 3, 'role': 'trader', 'name': 'Matt'}
# # ]
# #
# # @app.post('/users/user_id')
# # def change_username(user_id: int, new_name: str):
# #     current_user = list(filter(lambda user: user.get('id') == user_id, users2))[0]
# #     current_user['name'] = new_name
# #     return {'status': 200, 'data': current_user}