import os
import sys

import pygame
import requests
import math


def reverse_geocode(ll):
    geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={ll}&format=json"

    # Выполняем запрос к геокодеру, анализируем ответ.
    geocoder_request = geocoder_request_template.format(**locals())
    response = requests.get(geocoder_request)

    if not response:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))

    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первый топоним из ответа геокодера.
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


class MapSettings:
    def __init__(self):
        self.lat = 51.765334
        self.lon = 55.124111
        self.zoom = 15
        self.type = "map"
        self.search_result = None

    def ll(self):
        return "{0},{1}".format(self.lon, self.lat)

    def set_zoom(self, new_zoom):
        self.zoom += new_zoom


def map_create(mp):
    map_request = "http://static-maps.yandex.ru/1.x/"
    params = {
        'll': mp.ll(),
        'z': mp.zoom,
        'l': mp.type
    }

    if mp.search_result:
        params['pt'] = f'{mp.search_result.point[0]},{mp.search_result.point[1]},pm2grm'

    response = requests.get(map_request, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(2)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapSettings()
    map_file = map_create(mp)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    if mp.zoom != 2:
                        mp.set_zoom(-1)
                if event.key == pygame.K_PAGEUP:
                    if mp.zoom != 19:
                        mp.set_zoom(1)
                if event.key == pygame.K_LEFT:
                    mp.lon -= 0.02 * math.pow(2, 13 - mp.zoom)
                if event.key == pygame.K_RIGHT:
                    mp.lon += 0.02 * math.pow(2, 13 - mp.zoom)
                if event.key == pygame.K_UP:
                    if mp.lat < 85:
                        mp.lat += 0.008 * math.pow(2, 13 - mp.zoom)
                if event.key == pygame.K_DOWN:
                    if mp.lat > -85:
                        mp.lat -= 0.008 * math.pow(2, 13 - mp.zoom)
        map_file = map_create(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()

