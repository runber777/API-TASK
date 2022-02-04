import os
import sys

import pygame
import requests


class MapSettings:
    def __init__(self):
        self.lat = 55.124111
        self.lon = 51.765334
        self.zoom = 20
        self.type = "map"
        self.search_result = None



def map_create(MapSettings):
    mp = MapSettings()
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
    running = True
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass
        else:
            continue

        map_file = map_create(MapSettings)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
