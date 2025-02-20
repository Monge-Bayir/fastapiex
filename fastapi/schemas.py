from pydantic import BaseModel

class BaseRecipes(BaseModel):
    name: str
    views: int
    time_cooking: int
    description: str
    ingredients: str


class RecipesIn(BaseRecipes):
    ...


class RecipesOut(BaseRecipes):
    id: int

    class Config:
        orm_mode = True