from bs4 import BeautifulSoup
import requests
from random import choice


class Parser:

    def __init__(self, url):
        self.dishes_info = None
        self.bluda_names = None
        self.dishes = None
        self.soup = None
        self.url = url

        self.prepare_parser()
        self.get_bludo_tab()

    def prepare_parser(self):
        r = requests.get(self.url)

        if r.status_code == 200:
            self.soup = BeautifulSoup(r.text, "html.parser")

    def parse_url(self, url):
        r = requests.get(url)

        return BeautifulSoup(r.text, "html.parser")

    def get_divs_by_classes(self, class_, text):
       return text.findAll("div", class_=class_)

    def get_div_by_class(self, class_, text):
        return text.find("div", class_=class_)
    
    def get_a_by_classes(self, class_, text):
        return text.findAll("a", class_=class_)
    
    def get_bludo_tab(self):

        tab = self.get_divs_by_classes("tabItem", self.soup)[0]

        self.dishes = self.get_divs_by_classes("ingredientItem", tab)
        self.bluda_names = []
        
        self.dishes_info = {}
        for dish in self.dishes:
            dishes_recipes = {}
            dish_name = dish.findAll("h2", class_="ingredientItemH2")
            if len(dish_name) > 0:
                
                self.bluda_names.append(dish_name[0].text)
                dish_name = dish_name[0].text
                all_dishes_div = dish.find("div")
                recipes = all_dishes_div.findAll("a", href=True)
                for recipe in recipes:
                    dishes_recipes.update({recipe.text : recipe["href"]})

                self.dishes_info.update({dish_name : dishes_recipes})

    def get_available_recipes(self, dish_type):
        if dish_type in self.dishes_info:
            dish_list = list(self.dishes_info[dish_type].keys())
            dish_str = ""
            k = 1
            for dish in dish_list:
                dish_str += dish
                if k % 4 == 0:
                    dish_str += ",\n"
                else:
                    dish_str += ", "
                k += 1
            return dish_str
        
    def get_recipe_info(self, user_text):
        keys = self.dishes_info.keys()
        for k in keys:
            
            if user_text in self.dishes_info[k]:
                dish_href = self.dishes_info[k][user_text]
                worker = self.parse_url('https://povar.ru{}'.format(dish_href))
                recipes = self.get_divs_by_classes("recipe", worker)
                recipe = choice(recipes)
                
                base_url = "https://povar.ru"

                url = recipe.find("a", class_="listRecipieTitle", href=True)['href']

                worker = self.parse_url(base_url + url)
                name = worker.find("h1", class_="detailed").text
                
                ingredients = worker.find("ul", class_="detailed_ingredients").text
                steps = worker.findAll("div", class_="detailed_step_description_big")
                step_str = ""
                
                for step in steps:
                    step_str += step.text
                    step_str += "\n"

                img_src_div = worker.find("div", class_="bigImgBox")
                img_src = img_src_div.find("img", src=True)["src"]

                return_dict = {
                    "dishName": name,
                    "ingredients": ingredients,
                    "steps": step_str,
                    "imgSrc": img_src,
                    "url": base_url + url,
                    }
                return return_dict

        return None

            
            
            



        

                
            
        
            

    
