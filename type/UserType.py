import strawberry
# import typing



@strawberry.type
class User :
    id: str
    name: str
    email: str
    password: str

           