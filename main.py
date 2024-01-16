from datetime import datetime
from enum import Enum
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title='Trading App'
)

users = [
    {'id': 1, 'role': 'admin', 'name': 'Bob'},
    {'id': 2, 'role': 'investor', 'name': 'John'},
    {'id': 3, 'role': 'trader', 'name': 'Matt', 'degree': [
        {'id': 1, 'created_at': '2020-01-01', 'type_degree': 'expert'}
    ]}
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime.date
    type_degree: str


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: List[Degree]


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in users if user.get('id') == user_id]


all_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12}
]

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trades(trades: List[Trade]):
    all_trades.extend(trades)
    return {'status': 200, 'data': all_trades}


# @app.post('/trades')
# def get_trades(limit: int = 1, offset: int = 0):
#     return trades[offset:][:limit]


# users2 = [
#     {'id': 1, 'role': 'admin', 'name': 'Bob'},
#     {'id': 2, 'role': 'investor', 'name': 'John'},
#     {'id': 3, 'role': 'trader', 'name': 'Matt'}
# ]
#
# @app.post('/users/user_id')
# def change_username(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get('id') == user_id, users2))[0]
#     current_user['name'] = new_name
#     return {'status': 200, 'data': current_user}