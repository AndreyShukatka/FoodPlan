import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.core.management.base import BaseCommand
from food.models import Recipe, Ingredient, Menu, Category
import os
from urllib.parse import urljoin, urlsplit


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


def download_img(url, folder):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    file_name = os.path.basename(urlsplit(url).path)
    img_path = os.path.join(folder, file_name)
    with open(img_path, 'wb') as file:
        file.write(response.content)
    img_path = os.path.join('/dishes/', file_name)
    return img_path

def main():
    # dinner_urls_page = 'https://1000.menu/catalog/lyogkii-ujin?ms=1&str=&cat_es_inp%5B%5D=10090&es_tf=0&es_tt=14&es_cf=0&es_ct=2000'
    dinner_urls_page = 'https://1000.menu/catalog/zvanji-uzhin'

    response = requests.get(dinner_urls_page)
    dishes_urls = parse_resipy_page_urls(response)
    all_dishes = {}
    for dish_url in dishes_urls:
        response = requests.get(dish_url)
        dish_info, dish_name = parse_resipy_page(response)
        all_dishes[dish_name] = dish_info

    folder = 'media/dishes'
    for dish in all_dishes:
        name = dish
        calories = all_dishes[dish]['call']

        img_url = all_dishes[dish]['img_url']
        img_path = download_img(img_url, folder)


        recepy_text = ''
        for step_index, cooking_step in enumerate(all_dishes[dish]['recipy']):
            if step_index == 0:
                recepy_text = f'{recepy_text} <p>{all_dishes[dish]["recipy"][cooking_step]}</p>'
                recepy_prev_text = all_dishes[dish]['recipy'][cooking_step]
            else:
                recepy_text = f'{recepy_text} <p>{step_index}. {all_dishes[dish]["recipy"][cooking_step]}</p>'

        for one_dish in all_dishes[dish]['ingridients']:
            ingredient_name = one_dish
            ingredient_unit = all_dishes[dish]['ingridients'][one_dish]['unit']
            try:
                ingredient_quantity = float(all_dishes[dish]['ingridients'][one_dish]['count'])
            except ValueError:
                ingredient_quantity = 0

        recipe, created = Recipe.objects.get_or_create(
            name=name,
            calories=calories,
        )

        if created:
            menu = Menu.objects.order_by('?')[0]
            category = Category.objects.get(name='Ужины')
            recipe.description = recepy_text
            recipe.preview_text = recepy_prev_text
            recipe.menu = menu
            recipe.image = img_path
            recipe.category.add(category)
            recipe.save()
            for one_dish in all_dishes[dish]['ingridients']:
                ingredient_name = one_dish
                ingredient_unit = all_dishes[dish]['ingridients'][one_dish]['unit']
                try:
                    ingredient_quantity = float(all_dishes[dish]['ingridients'][one_dish]['count'])
                except ValueError:
                    ingredient_quantity = 0

                recipe.ingredient.create(name=ingredient_name, unit = ingredient_unit ,quantity = ingredient_quantity)
        else:
            recipe.preview_text = recepy_prev_text
            recipe.description = recepy_text
            recipe.image = img_path
            recipe.save()

class Command(BaseCommand):
    help = 'Start parse recipes'

    def handle(self, *args, **options):
        main()
