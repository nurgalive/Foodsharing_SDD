from enum import Enum

class City(Enum):
  MSC = 'Москва'
  SPB = 'Санкт-Петербург'
  UNKNOWN = 'Неизвестно'

city_aliases = {
  City.MSC: ['москва', 'мск', 'moscow', 'msc', 'моск'],
  City.SPB: ['питер', 'спб', 'санкт-петербург', 'spb', 'saint-petersburg'],
}

metro_stations = {
  City.MSC: [
    "авиамоторная", "автозаводская", "академическая", "александровский сад", "алексеевская", "алма-атинская",
    "алтуфьево", "аннино", "арбатская (арбатско-покровская линия)", "арбатская (филевская линия)", "аэропорт",
    "бабушкинская", "багратионовская", "баррикадная", "бауманская", "беговая", "белорусская", "беляево", "бибирево",
    "библиотека имени ленина", "борисово", "боровицкая", "ботанический сад", "братиславская",
    "бульвар адмирала ушакова", "бульвар дмитрия донского", "бульвар рокоссовского", "бунинская аллея",
    "варшавская", "вднх", "владыкино", "водный стадион", "войковская", "волгоградский проспект", "волжская",
    "волоколамская", "воробьевы горы", "выставочная", "выхино", "деловой центр", "динамо", "дмитровская",
    "добрынинская", "домодедовская", "достоевская", "дубровка", "жулебино", "зябликово", "измайловская",
    "калужская", "кантемировская", "каховская", "каширская", "киевская", "китай-город", "кожуховская",
    "коломенская", "комсомольская", "коньково", "красногвардейская", "краснопресненская", "красносельская",
    "красные ворота", "крестьянская застава", "кропоткинская", "крылатское", "кузнецкий мост", "кузьминки",
    "кунцевская", "курская", "кутузовская", "ленинский проспект", "лермонтовский проспект", "лубянка", "люблино",
    "марксистская", "марьина роща", "марьино", "маяковская", "медведково", "международная", "менделеевская",
    "митино", "молодежная", "монорельса выставочный центр", "монорельса телецентр",
    "монорельса улица академика королева", "монорельса улица милашенкова", "монорельса улица сергея эйзенштейна",
    "монорельсовой дороги тимирязевская", "мякинино", "нагатинская", "нагорная", "нахимовский проспект",
    "новогиреево", "новокосино", "новокузнецкая", "новослободская", "новоясеневская", "новые черемушки",
    "октябрьская", "октябрьское поле", "орехово", "отрадное", "охотныйряд", "павелецкая", "парк культуры",
    "парк победы", "партизанская", "первомайская", "перово", "петровско-разумовская", "печатники", "пионерская",
    "планерная", "площадь ильича", "площадь революции", "полежаевская", "полянка", "пражская",
    "преображенская площадь", "пролетарская", "проспект вернадского", "проспект мира", "профсоюзная",
    "пушкинская", "пятницкое шоссе", "речной вокзал", "рижская", "римская", "рязанский проспект", "савеловская",
    "свиблово", "севастопольская", "семеновская", "серпуховская", "славянский бульвар",
    "смоленская (арбатско-покровская линия)", "смоленская (филевская линия)", "сокол", "сокольники", "спартак",
    "спортивная", "сретенский бульвар", "строгино", "студенческая", "сухаревская", "сходненская", "таганская",
    "тверская", "театральная", "текстильщики", "теплый стан", "тимирязевская", "третьяковская", "тропарево",
    "трубная", "тульская", "тургеневская", "тушинская", "улица академика янгеля", "улица горчакова",
    "улица скобелевская", "улица старокачаловская", "улица 1905 года", "университет", "филевский парк", "фили",
    "фрунзенская", "царицыно", "цветной бульвар", "черкизовская", "чертановская", "чеховская", "чистые пруды",
    "чкаловская", "шаболовская", "шипиловская", "шоссе энтузиастов", "щелковская", "щукинская", "электрозаводская",
    "юго-западная", "южная", "ясенево"
  ],
  City.SPB: [
    "автово", "адмиралтейская", "академическая", "балтийская", "бухарестская", "василеостровская",
    "владимирская", "волковская", "выборгская", "горьковская", "гостиный двор", "гражданский проспект",
    "девяткино", "достоевская", "елизаровская", "звёздная", "звенигородская", "кировский завод",
    "комендантский проспект", "крестовский остров", "купчино", "ладожская", "ленинский проспект",
    "лесная", "лиговский проспект", "ломоносовская", "маяковская", "международная", "московская",
    "московские ворота", "нарвская", "невский проспект", "новочеркасская", "обводный канал",
    "обухово", "озерки", "парк победы", "парнас", "петроградская", "пионерская",
    "площадь александра невского 1", "площадь александра невского 2", "площадь восстания",
    "площадь ленина", "площадь мужества", "политехническая", "приморская", "пролетарская",
    "проспект большевиков", "проспект ветеранов", "проспект просвещения", "пушкинская", "рыбацкое",
    "садовая", "сенная площадь", "спасская", "спортивная", "старая деревня", "технологический институт 1",
    "технологический институт 2", "удельная", "улица дыбенко", "фрунзенская", "чёрная речка",
    "чернышевская", "чкаловская", "электросила"
  ],
}

def get_city(text):
  processed_text = text.lower()
  for city_name in city_aliases:
    for city_aliace in city_aliases[city_name]:
      if city_aliace in processed_text:
        return city_name

  for city_name in metro_stations:
    for metro_aliace in metro_stations[city_name]:
      if metro_aliace in processed_text:
        return city_name

  return City.UNKNOWN

stop_word = ['площадь', 'улица', 'проспект',]

def get_metro_station(text):
  processed_text = text.lower()

  for city_name in metro_stations:
    for metro_aliace in metro_stations[city_name]:
      if metro_aliace in processed_text:
        words = metro_aliace.split(' ')

        for word in words:
          if word in stop_word:
            continue

          return metro_aliace

  return 'unknown'