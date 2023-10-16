from django.http import Http404
from django.shortcuts import render

database = [
    {
        'id': 1,
        'feature': 'Электроэнергия',
        'type': 'кВт.ч',
        'describe': 'это — физический термин, широко распространённый в технике и в быту для определения количества электрической энергии, выдаваемой генератором в электрическую сеть или получаемой из сети потребителем.',
        'url_photo': 'https://gorod-ust-labinsk.ru/upload/iblock/035/p9ryj072mpbdxkwypjv1n5iojqjnbp93.jpg',
        'status': True
    },
    {
        'id': 2,
        'feature': 'Отопление',
        'type': 'ГКал',
        'describe': 'это — искусственный обогрев помещений с целью возмещения в них теплопотерь и поддержания на заданном уровне температуры, отвечающей условиям теплового комфорта и/или требованиям технологического процесса.',
        'url_photo': 'https://novyiy-urengoy.vodomirural.ru/upload/iblock/988/9884001f190f5e4f3acb4af675524dac.jpg',
        'status': True
    },
    {
        'id': 3,
        'feature': 'Холодное водоснабжение',
        'type': 'м3',
        'describe': 'это — круглосуточное обеспечение потребителя холодной питьевой водой надлежащего качества, подаваемой в необходимых объемах по присоединенной сети в жилое помещение либо до водоразборной колонки.',
        'url_photo': 'https://makipa.ru/media/upload/blog/blogimage/voda/vodapit-scaled_LMkiUfq.jpg',
        'status': True
    },
    {
        'id': 4,
        'feature': 'Горячее водоснабжение',
        'type': 'м3',
        'describe': 'это — обеспечение бытовых нужд населения и производственных потребностей в воде с повышенной (до 75 °С) температурой. Является одним из показателей качества жизни, важным фактором улучшения санитарно-гигиенических и культурно-бытовых условий жизни.',
        'url_photo': 'http://remoo.ru/wp-content/uploads/2019/02/schetchik-goryachej-vody-s-termodatchikom-1.jpg',
        'status': True
    },
    {
        'id': 5,
        'feature': 'Водоотведение',
        'type': 'м3',
        'describe': 'это — коммунальная услуга приема, транспортировки и очистки сточных вод. Использованная в квартирах вода через канализацию попадает в очистные сооружения, где ее прогоняют через систему фильтров и утилизируют (чаще всего сливают в реку).',
        'url_photo': 'https://gymnasia2.ru/wp-content/uploads/2/2/7/2278061f065487b4cab63fe697126816.jpeg',
        'status': True
    },
    {
        'id': 6,
        'feature': 'Лифт',
        'type': 'Человек',
        'describe': 'это — разновидность грузоподъёмной машины, предназначенная для вертикального или наклонного перемещения грузов на специальных платформах, передвигающихся по жёстким направляющим.',
        'url_photo': 'https://alum-ural.ru/images/th2_6.jpg',
        'status': True
    },
    {
        'id': 7,
        'feature': 'Домофон',
        'type': 'шт',
        'describe': 'это — электронная система, состоящая из устройств, передающих сигнал от вызывного блока к переговорному устройству.',
        'url_photo': 'https://www.tmk-pilot.ru/assets/2022/images/service/Montazhdomofonov/2022-06-30_192821.jpg',
        'status': True
    }
]


# Список
def Get_rent_calculation_s(request):
    response = {'data': database}
    return render(request, 'rent_calculation_s.html', response)


# Информация
def Get_rent_calculation(request, id):
    # Найдем объект в списке по 'id'
    rent_calculation = None
    for obj in database:
        if obj['id'] == id:
            rent_calculation = obj
            break

    if rent_calculation is None:
        raise Http404("Объект не найден")

    response = {'data': rent_calculation}

    return render(request, 'rent_calculation.html', response)


# Фильтрация
def Filter(request):
    # Преобразовать ключевое слово в строку для поиска в базе данных
    filter_keyword = str(request.GET.get('filter_keyword'))

    filtered_objects = [obj for obj in database if filter_keyword.lower() in obj['feature'].lower()]

    if filtered_objects == []:
        raise Http404("Объект не найден")

    response = {'data': filtered_objects[0]}

    return render(request, 'rent_calculation.html', response)
