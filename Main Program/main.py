import pygame
import pygame.locals
import requests, json, io
import Module
import MealInfo, ClassInfo

data = io.open('config.json', mode='r', encoding='utf-8').read()
conf = json.loads(data)

mod_mealinfo = MealInfo.MealInfo(
    conf['Open-NEIS-API']['KEY'],
    conf['Open-NEIS-API']['SD_SCHUL_CODE'],
    conf['Open-NEIS-API']['ATPT_OFCDC_SC_CODE']
)
mod_classinfo = ClassInfo.ClassInfo(
    conf['Open-NEIS-API']['KEY'],
    conf['Open-NEIS-API']['SD_SCHUL_CODE'],
    conf['Open-NEIS-API']['ATPT_OFCDC_SC_CODE']
)

mod_mealinfo.set_date(2019,11)
mod_classinfo.set_date(2019,11,27)

for row in mod_classinfo.get(2, 3):
    print('%2s학년 %s반 :%2s교시 %s' % (row['GRADE'], row['CLRM_NM'][0:2], row['PERIO'], row['ITRT_CNTNT']))

#for meal in mod_mealinfo.get(26):
#    print(meal['MMEAL_SC_NM'])
#    print(meal['DDISH_NM'])



'''
pygame.init()

WND_W = 90 * 6
WND_H = 160 * 6

surf = pygame.display.set_mode((WND_W, WND_H))
#mConsole = Console.Console()

loop = True
while loop:
    for e in pygame.event.get():
        if e.type == pygame.locals.QUIT:
            loop = False

    surf.fill((0, 0, 0))
    pygame.display.flip()
/'''
#pygame.quit()


