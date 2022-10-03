import strawberry

@strawberry.type
class SignUp:
    id: str
    email: str
    password: str

@strawberry.type
class SignIn:
    email: str
    password: str

@strawberry.type
class Token:
    token: str
