from foodscrape.logger import get_logger
from foodscrape.scrape.models import Ingredient, Recipe, RecipeIngredient
from foodscrape.scrape.service import get_recipes_by_ingredients, scrape_recipe

logger = get_logger(__name__)


def test_scrape_recipe(database):
    url = "https://www.food.com/recipe/barbs-zucchini-patties-99731"
    scrape_recipe(url)


def test_get_recipes_by_ingredients(database):
    ingredient1 = Ingredient("Chicken")
    ingredient2 = Ingredient("Rice")
    ingredient3 = Ingredient("Cheese")
    ingredient4 = Ingredient("Tortilla")

    r1 = RecipeIngredient("1", "Chicken", "")
    r2 = RecipeIngredient("2", "Rice", "")
    r3 = RecipeIngredient("1", "Cheese", "")
    r4 = RecipeIngredient("1", "Tortilla", "")

    ingredient1 = ingredient1.save()
    ingredient2 = ingredient2.save()
    ingredient3 = ingredient3.save()
    ingredient4 = ingredient4.save()

    r1.ingredient_id = ingredient1.id
    r2.ingredient_id = ingredient2.id
    r3.ingredient_id = ingredient3.id
    r4.ingredient_id = ingredient4.id

    recipe1 = Recipe("Chicken and Rice", ingredients=[r1, r2])
    recipe2 = Recipe("Quesadilla", ingredients=[r3, r4])

    r1 = RecipeIngredient("1", "Chicken", "")
    r3 = RecipeIngredient("1", "Cheese", "")
    r4 = RecipeIngredient("1", "Tortilla", "")
    r1.ingredient_id = ingredient1.id
    r3.ingredient_id = ingredient3.id
    r4.ingredient_id = ingredient4.id

    recipe3 = Recipe("Chicken Quesadilla", ingredients=[r1, r3, r4])

    recipe1.save()
    recipe2.save()
    recipe3.save()

    ingredients = get_recipes_by_ingredients(["Cheese", "Tortilla", "Chicken"])

    assert recipe2 in ingredients
    assert recipe3 in ingredients
    assert recipe1 not in ingredients
