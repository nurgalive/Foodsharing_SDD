from tgbot.models import User, Post
import re

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

# все категории
all_cats = {
  'изделия из муки': ['мука', 'макароны', 'хлеб', 'хлебушек', 'хлебный', 'чебурек', 'лаваш', 'батон', 'булка', 'калач', 'лепешка', 'булочка', 'сдоба', 'плюшка', 'рожки', 'галеты', 'крекеры', 'печенье', 'пряники', 'баранки', 'бублики',  'соломка', 'сушки', 'сухари', 'сухарики', 'тесто', 'Сочни', 'маффины', 'Куличи', 'Булочки', 'Багеты', 'Чиабатта', 'Фокачча', 'Ватрушки', 'Коржики', 'Пряники', 'Рогалики', 'Пончики', 'Слойки', 'Панкейки', 'тарталетка', 'круасан', 'украинский'],

  'молочные продукты': ['молоко', 'сгущенка', 'сливки', 'сливки', 'сметана', 'творог', 'творожная', 'сырки ', 'ацидофилин', 'йогурт', 'кефир', 'кумыс', 'пахта', 'простокваша', 'ряженка', 'сыворотка', 'брынза', 'сыр', 'мороженое', 'пломбир', 'эскимо', 'масло', 'маргарин', 'кефирный'],

  'овощи': ['лук', 'морковь','свекла', 'картофель', 'баклажаны', 'брюква', 'кабачки', 'капуста', 'картошка', 'лук-порей', 'морковь', 'помидор', 'пастернак', 'патиссоны', 'перец', 'петрушка', 'ревень','редис', 'редька', 'репа', 'салат', 'сельдерей', 'спаржа', 'томаты', 'укроп', 'хрен', 'черемша', 'чеснок', 'шпинат', 'щавель', 'огурцы', 'брокколи', 'броколи', 'овощи', 'травы', 'биобальзам', 'прополис', 'жмых', 'имбирь', 'стевия', 'морковка', 'зелень', 'мята'],

  'фрукты': ['абрикосы', 'айва', 'алыча', 'ананас', 'бананы', 'вишня', 'гранат', 'груша', 'инжир', 'кизил', 'персики', 'рябина', 'слива', 'сливы', 'хурма', 'черешня', 'шелковица', 'яблоки', 'апельсин', 'грейпфрут', 'лимон', 'мандарин', 'фрукты', 'варенье', 'джем', 'повидло', 'варенье', 'урюк', 'курага', 'изюм', 'чернослив', 'финики', 'арбуз', 'дыня', 'тыква'],

  'готовые блюда': ['Рулет', 'Котлеты', 'Суп', 'Блюдо', 'Оладьи', 'Салаты', 'Пироги', 'Десерты','Торты', 'мороженое', 'Блины', 'Выпечка', 'Запеканка', 'Закуски', 'Жареные', 'Тушеные', 'духовке', 'Кексы', 'Каши', 'кашка', 'Запеченная', 'Пирожки', 'Блюдо', 'Окрошка', 'шаурма', 'шаверма', 'Мимоза', 'Сочни', 'маффины', 'Винегрет', 'Мимоза', 'Оливье', 'шубой', 'Шарлотки', 'Манники',  'Куличи', 'Беляши', 'капкейки', 'чизкейки', 'медовик', 'наполеон', 'Хачапури', 'чебуреки', 'штрудель', 'Безе', 'Брауни', 'Вафли', 'Пицца', 'панкейки', 'Драники', 'Сырники', 'Пельмени', 'Манты', 'Котлеты', 'Тефтели', 'Фрикадельки', 'голубцы', 'Холодец', 'Шашлыки', 'гарниры', 'спагетт', 'пасты', 'Борщи', 'щи', 'солянка', 'Рассольник', 'харчо', 'Окрошки', 'свекольники', 'Омлеты', 'яичница', 'бутерброд', 'Гренки', 'Запеканки', 'Суши' , 'роллы', 'желе, муссы', 'крамбл', 'гамбургер', 'порошковый', 'смесь', 'чипсы', 'снэки', 'студень', 'обеды', 'первое', 'второе', 'печенюшки', 'бульон'],

  'сыры': ['Эдам', 'Гауда', 'Маасдам', 'Тильзитер', 'Голландский', 'сыр', 'брынза'],

  'грибы':['белые', 'лисички', 'маслята', 'опята', 'подосиновики', 'рыжики', 'шампиньоны', 'грибы'],

  'крупы и бобовые': ['пшеница', 'рожь', 'гречиха', 'кукуруза', 'овес', 'просо', 'рис', 'ячмень', 'бобы', 'горошек', 'фасоль', 'горох', 'соя', 'фасоль', 'чечевица', 'гречневая', 'кукурузная', 'овсяная', 'геркулес', 'толокно', 'пшенная', 'рисовая', 'перловая', 'ячменевая', 'манная', 'пшеничная', 'булгур', 'кускуса'],

  'кондитерские изделия': ['батончики', 'драже', 'ирис', 'карамель', 'конфеты', 'зефир', 'мармелад', 'пастила', 'халва', 'халва', 'шоколад', 'вафли', 'пирожное', 'торт', 'Сникерс', 'Баунти', 'Пряники', 'Рогалики', 'Пончики', 'Слойки', 'Сахарозаменители', 'тортик'],

  'мясные продукты': ['мясо', 'телятина', 'баранина', 'грудинка', 'корейка ', 'буйволятина', 'верблюжатина  ', 'говядина', 'вырезка', 'вымя', 'печень', 'почки', 'сердце', 'язык', 'оленина', 'свинина', 'ножки', 'шпик', 'яка', 'колбаса', 'ветчина', 'окорок', 'сардельки', 'сосиски', 'фарш', 'паштет', 'пельмени', 'рулька', 'сало', 'козлятины', 'кролик', 'баран', 'корова', 'крольчатина', 'студень', 'кости', 'косточки', 'рёбра', 'ребра'],

  'напитки': ['лимонад', 'жигулевское', 'пиво', 'квас', 'вино', 'шампанское', 'водка', 'коньяк', 'настойка', 'наливка', 'ликёр', 'пунш', 'чай', 'кофе', 'газировка', 'минералка', 'вода', 'компот', 'сок', 'кисель', 'коктейли', 'смузи', 'компоты', 'джин', 'виски', 'сидр'],

  'орехи и семечки': ['арахис', 'грецкие', 'орехи', 'миндаль', 'подсолнечник', 'фундук', 'семечки'],
  
  'соусы': ['соус', 'майонез', 'уксус', 'васаби', 'кетчуп'],

  'птица': ['гуси', 'индейки', 'куры', 'перепёлки', 'утки', 'окорочек', 'филе', 'желудок', 'яйцо'],

  'рыба и морепродукты': ['вобла', 'горбуша', 'карп', 'килька', 'лещ', 'минтай', 'мойва', 'окунь', 'осетр', 'балык', 'пикша', 'сайра', 'сельдь', 'селедка', 'скумбрия', 'снеток', 'ставрида', 'судак', 'треска', 'тунец', 'угорь', 'щука ', 'кальмар', 'краб', 'креветка', 'моллюск', 'мидии', 'ластоногих', 'морская-капуста', 'икра', 'консервы-рыбные', 'рыбка'],

  'сырье': ['агар', 'дрожжи', 'желатин', 'отруби', 'какао-порошок', 'какао', 'крахмал', 'патока', 'пектин', 'порошок', 'мёд', 'сахар-сырец', 'сахар-песок', 'сахар-рафинад', 'соль', 'уксус'],

  'ягоды': ['брусника', 'виноград', 'голубика', 'ежевика', 'земляника', 'клюква', 'крыжовник', 'малина', 'морошка', 'облепиха', 'смородина', 'черника', 'шиповник', 'оливки', 'шиповник'],

  'лекарства': ['Мерифатин', 'аспирин', 'парацетамол', 'Кетостерил', 'L-карнитин', 'BCAA'],

  'консервы': ['консервы', 'консервная'],

  'unknown': [],

  'общее': ['продукты', 'просрочка', 'набор'],

  'упаковка' : ['банки', 'крышки']
}

morph_cats = {}

# проводим морфологичесикй разбор категорий
for category in all_cats:
  foods = []

  for food in all_cats[category]:
    words = food.split(' ')
    normalized_words = []

    for word in words:
      p = morph.parse(word)

      if p[0]:
        normalized_words.append(p[0].normal_form)
        #print(p[0].normal_form)

    foods.append(normalized_words)

  morph_cats[category] = foods

# ищем вхождение категории в тексте
def get_food_category(text):
  detected_cats = {}

  # подготавливаем входной текст
  # убираем все лишние знаки
  text_words_list = re.findall(r'[А-яЁё]+', text)

  # делаем морфологичесикй разбор слов
  morph_text_list = []
  for w in text_words_list:
    if len(w) < 3:
      continue
    p = morph.parse(w)
    if p[0]:
      morph_text_list.append(p[0].normal_form)
  
  #print(morph_text_list)

  for category in morph_cats:
    for food in morph_cats[category]:
      for word in food:
        if (len(word) <= 2):
          continue

        #print("Current word: " + word)
        
        if word in morph_text_list:
          #print("Found word " + word + " in category " + category)
          # если категории еще нет в словаре, то создать новую категорию
          if category not in detected_cats:
            detected_cats[category] = 1
          else:
            # если категория уже есть, то увелить её частоту на один
            detected_cats[category] = 1 + detected_cats[category]
          break

  if len(detected_cats) == 0:
    return 'unknown'

  sorted(detected_cats, key=detected_cats.get, reverse=True)

  #print(detected_cats)

  #return list(detected_cats.keys())

  # берем категорию, продукты из которой чаще всего встречались в тексте
  category_with_max_match = max(detected_cats, key=detected_cats.get)

  # сколько раз встретилась максимальная категория
  category_with_max_match_count = detected_cats[category_with_max_match]
  return category_with_max_match

# update category for post
def update_category():
  posts = Post.objects.all()
  for post in posts:
    result = get_food_category(post.text)
    Post.objects.filter(pk=post.post_id).update(category=result)  