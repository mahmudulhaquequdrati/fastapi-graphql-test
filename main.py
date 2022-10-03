import strawberry


from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from controllers.users import Mutation, Query


# @strawberry.type
# class Query:
#     @strawberry.field
#     def hello(self) -> str:
#         return "Hello World"


schema = strawberry.Schema(Query, Mutation)


graphql_app = GraphQLRouter(schema)


app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
