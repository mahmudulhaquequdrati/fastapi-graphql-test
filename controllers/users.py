import typing
from auth.auth_bearer import verify_jwt
from auth.auth_handler import signJWT
from config.db import connection
import strawberry
from type.SignUp import SignIn,Token
from strawberry.permission import BasePermission
from strawberry.types import Info 
from type.UserType import User
from bson import ObjectId
# create the database and collection
db = connection["test"]
collection = db["users"]
user= db["user"]


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        result = verify_jwt(info.context["request"].headers.get("Authorization"))
        return result




@strawberry.type
class Query:
    def getAllUsers(self) -> list[User]:
              users = []
              for user in collection.find():
                  users.append(User(id=user["_id"], name=user["name"],
                         email=user["email"], password=user["password"]))
              return users

    allUsers: list[User] = strawberry.field(
        resolver=getAllUsers, permission_classes=[IsAuthenticated])


    @strawberry.field
    def user(self, id: str) -> User:
        user = collection.find_one({"_id": ObjectId(id)})
        return User(id=user["_id"], name=user["name"],email=user["email"], password=user["password"])
      


@strawberry.type
class Mutation:
    @strawberry.mutation
    def createUser(self, name: str, email: str, password: str) -> User:
        user = {"name": name, "email": email, "password": password}
        result = collection.insert_one(dict(user))
        id = result.inserted_id
        user = collection.find_one({"_id": ObjectId(id)})
        result = User(id=user["_id"], name=user["name"],
                      email=user["email"], password=user["password"])

        return result

        
    @strawberry.mutation
    def updateUser(self, id: str, name: str, email: str, password: str) -> User:
        user = {"name": name, "email": email, "password": password}
        collection.update_one({"_id": ObjectId(id)}, {"$set": user})
        user["_id"] = id
        return User(id=user["_id"], name=user["name"], email=user["email"], password=user["password"])

    @strawberry.mutation
    def deleteUser(self, id: str) -> bool:
        collection.delete_one({"_id": ObjectId(id)})
        return True        

    @strawberry.mutation

    # signup and user and then send the token in token format
    def signUp(self, email: str, password: str) -> Token:
        usera = {"email": email, "password": password}
        result = user.insert_one(usera)
        id = result.inserted_id
        newuser = user.find_one({"_id": ObjectId(id)})
        inserted_email = str(newuser["email"])
        sendingToken = signJWT(str(inserted_email))
        return Token(token=sendingToken['token'])


    @strawberry.mutation
    #delete all the user from the database
    def deleteAllUser(self) -> bool:
        user.delete_many({})
        return True


    @strawberry.mutation
    def signIn(self, email: str, password: str) -> Token:

        def check_user(data: SignIn) -> bool:
            fuser = user.find_one({"email": data.email, "password": data.password})
            if fuser:
                return True
            return False

        if check_user(SignIn(email=email, password=password)):
            token = signJWT(email)
            return Token(token=token['token'])
        else :
            return "Invalid email or password"
 