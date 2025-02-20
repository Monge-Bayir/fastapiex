from fastapi import FastAPI
from database import engine, session, Base
import models
import schemas
from typing import List
from sqlalchemy.future import select

# Инициализация приложения FastAPI
app = FastAPI()


# Событие запуска приложения
@app.on_event('startup')
async def startup():
    # Создание всех таблиц в базе данных при запуске приложения
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


# Событие остановки приложения
@app.on_event('shutdown')
async def shutdown():
    # Завершение сеанса и освобождение ресурсов базы данных
    await session.commit()
    await engine.dispose()


# Эндпоинт для получения всех рецептов
@app.get('/recipes', response_model=List[schemas.RecipesOut])
async def get_recipes():
    """
    Получить список всех рецептов.

    Returns:
        List[schemas.RecipesOut]: Список объектов рецептов.
    """
    # Выполнение запроса к базе данных для получения всех рецептов
    res = await session.execute(
        select(models.Recipes)
    )
    list_recipe = res.scalars().all()  # Извлечение всех рецептов из результата запроса
    return list_recipe  # Возврат списка рецептов


# Эндпоинт для добавления нового рецепта
@app.post('/add', response_model=schemas.RecipesOut)
async def add_recipes(recipe: schemas.RecipesIn) -> models.Recipes:
    """
    Добавить новый рецепт.

    Args:
        recipe (schemas.RecipesIn): Данные нового рецепта.

    Returns:
        models.Recipes: Добавленный объект рецепта.
    """
    # Создание нового объекта рецепта из переданных данных
    new_recipe = models.Recipes(**recipe.dict())
    async with session.begin():  # Начало сессии для добавления данных
        session.add(new_recipe)  # Добавление нового рецепта в сессию

    return new_recipe  # Возврат добавленного рецепта


# Эндпоинт для получения рецепта по ID
@app.get('/recipes/{id}', response_model=schemas.RecipesOut)
async def get_recipe_by_id(id: int):
    """
    Получить рецепт по его ID.

    Args:
        id (int): Идентификатор рецепта.

    Returns:
        schemas.RecipesOut: Объект рецепта или None, если не найден.
    """
    # Выполнение запроса к базе данных для получения рецепта по ID
    res = await session.execute(select(models.Recipes).filter(models.Recipes.id == id))
    recipe = res.scalar_one_or_none()  # Извлечение одного рецепта или None, если не найден
    return recipe  # Возврат найденного рецепта
