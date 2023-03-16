import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.core.management.base import BaseCommand
from food.models import Recipe, Ingredient, Menu, Category


base_url = 'https://1000.menu/'
base_img_url = 'https://static.1000.menu'


def parse_resipy_page(res):
    soup = BeautifulSoup(res.text, 'lxml')

    name = soup.find('h1')

    # description = soup.find(class_='description is-citation')
    # print(description.text)

    persons = soup.find(class_="hidden yield")
    # print(persons.text)

    recipe = soup.find(class_='instructions')
    resipe_steps = recipe.text.split('Шаг')
    clean_recipe_steps = []
    recipy_steps = {}
    for step in resipe_steps:

        if step not in [' ', '  ']:
            clean_recipe_steps.append(step.strip())
            stripped_step = step.strip()

            splited_step = stripped_step.split(':', 1)
            try:
                recipy_steps[splited_step[0]] = splited_step[1]
            except IndexError:
                pass

    calories_soup = soup.find(class_='calories')
    caloryes = int(calories_soup.text.split(' ')[0])

    img = soup.find(class_='result-photo bl photo')
    img_link = img.get('src').split('img')[1]
    clean_link = "img/" + img_link
    img_full_link = urljoin(base_img_url, clean_link)

    ingredients_soup = soup.find_all(class_="ingredient list-item")
    ingridients = {}
    for ingredient in ingredients_soup:
        units = {}
        product = str(ingredient.meta.get('content'))
        ingredient_name = product.split(' - ')[0]
        quantity_with_weght = product.split(' - ')[1]
        ingredient_unit = quantity_with_weght.split(' ')[1]
        if ingredient_unit == 'по':
            ingredient_unit = 'по вкусу.'
        ingredient_weght = quantity_with_weght.split(' ')[0]
        units['count'] = ingredient_weght
        units['unit'] = ingredient_unit
        ingridients[ingredient_name] = units

    return {
        'recipy': recipy_steps,
        'persons_count': int(persons.text),
        'ingridients': ingridients,
        'call': caloryes,
        'img_url': img_full_link
    }, name.text


def parse_resipy_page_urls(response):
    links = re.findall(r'<a class="h5" href="(.+)" target="', response.text)
    full_links = []
    for link in links:
        full_link = urljoin(base_url, link)
        full_links.append(full_link)
    return full_links


def main():
    dinner_urls_page = 'https://1000.menu/catalog/lyogkii-ujin?ms=1&str=&cat_es_inp%5B%5D=10090&es_tf=0&es_tt=14&es_cf=0&es_ct=2000'
    # dinner_url = 'https://1000.menu/cooking/50341-pp-kurica-zapechennaya-s-ovoshchami-v-duxovke'

    response = requests.get(dinner_urls_page)
    dishes_urls = parse_resipy_page_urls(response)
    all_dishes = {}
    for dish_url in dishes_urls:
        response = requests.get(dish_url)

        dish_info, dish_name = parse_resipy_page(response)
        all_dishes[dish_name] = dish_info
        print(f'dish_name: {dish_name}')
        print(f'dish_info: {dish_info}')

        recipe, created = Recipe.objects.get_or_create(
            name=dish_name,
            description=dish_info['recipy']['1'],
            calories=dish_info['call']
        )
        if not created:
            menu = Menu.objects.order_by('?')[0]
            category = Category.objects.order_by('?')[0]
            recipe.menu = menu
            recipe.category = category
            recipe.save()
            for ingredient in dish_info['ingridients']:
                recipe.ingredient.create(name=ingredient)

class Command(BaseCommand):
    help = 'Start parse recipes'

    def handle(self, *args, **options):
        main()
