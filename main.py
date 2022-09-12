# имитация игру в Scrabble
from random import choice
dict_alfa = {}
russian_word = []

def loading_from_text_files():
    """
      загрузка из текстовых файлов dict_alfa, russian_word
    """
    with open('russian_word.txt','r',encoding="utf-8") as file:
        for line in file.readlines():
            line = line.rstrip('\n')
            russian_word.append(line )
    with open('dict_alfa.txt', 'r', encoding="utf-8") as file:
        for line in file.readlines():
            line = line.rstrip('\n')
            lines = line.split(':')
            dict_alfa[lines[0]] = int(lines[1])

def chek_name(name):
    """
    проверка имени на корректность
    """
    while True:
        input_name = input(f'{name} \n')
        if not input_name.isnumeric() and not ' ' in input_name:
            return   input_name
            break
        else:
          print("Не правельное имя")

def handing_random_letters(amount_letters):
    """
    Генерирует буквы в случайном порядке из словаря  dict_alfa
    :param amount_letters: Количество букв, которых нужно с генерировать в случайном порядке
    :return:Список букв с генерированных в случайном порядке
    """
    random_list_player = []
    while True:
        if len(dict_alfa) == 0:
            print('буквы кончились')
            break
        if amount_letters <= 0: break
        data = choice(list(dict_alfa.keys()))
        dict_alfa[data] = dict_alfa[data] - 1
        random_list_player.append(data)
        amount_letters -= 1
        if dict_alfa[data] <= 0:
            del dict_alfa[data]

    return random_list_player

def deleting_guessed_letters(random_list_player, guessed_letters):
    """
    Удаление отгаданного слова по буквам если они есть
    :param random_list_player: Список букв от куда нужно удалить слово по буквам
    :param guessed_letters: Отгаданное слово
    :return: Чистый список букв
    """
    cont = 0
    for s in guessed_letters:
        if s in random_list_player:
            cont += 1
    if len(guessed_letters) == cont:
        for s in guessed_letters:
            random_list_player.remove(s)
        return random_list_player
    else:
        return random_list_player

def scoring(string):
    """
    Расчет баллов в зависимости от длены угаданного слова
    :param string: угаданное слово
    :return: баллы
    """
    if len(string) == 4:
         return 6
    elif len(string) == 5:
         return 7
    elif len(string) == 6:
         return 8
    else:
        return len(string)

def player_move(random_list_player, neme_player, count):
    """
    Производит ход игрока
    :param random_list_player: Список букв с генерированных в случайном порядке
    :param neme_player: Имя игрока
    :param count: Количество букв в списке букв с генерированных в случайном порядке
    :return: Количество баллов полученных за отгаданное слово
    """
    balls_player = 0
    move_count = 0
    while True:
        if move_count == 0: answer = input(f'Ходит {neme_player}: \n')
        if move_count != 0: answer = input()
        while not answer: answer = input(f'Ну введи что не будь {neme_player}: \n')
        if answer == 'stop':
            balls_player = -1
            print('-------------------------------')
            return [balls_player, random_list_player]

        if answer in russian_word:
            random_list_player = deleting_guessed_letters(random_list_player, answer)
            if count > len(random_list_player):

                print(f'Такое слово есть. \n{neme_player} получает {scoring(answer)} баллов.')
                balls_player =  scoring(answer)
                random_list_player = random_list_player + handing_random_letters(count - len(random_list_player) + 1)
                print(f'Добавляю буквы"', ', '.join(random_list_player), '"')
                print('-------------------------------')
                return [balls_player, random_list_player]
            elif move_count == 0:
                move_count = 1
                print(f'Буквы не совподают, попробуй ещё раз.')
            else:
                print(f'Буквы не совподают. \n{neme_player} не получает очков.')
                random_list_player = random_list_player + handing_random_letters(count - len(random_list_player) + 1)
                print(f'Добавляю буквы"', ', '.join(random_list_player), '"')
                print('-------------------------------')
                return [balls_player, random_list_player]

        elif  move_count == 0 :
            move_count = 1
            print(f'Такого слова нет, попробуй ещё раз.')
        else:
            print(f'Такого слова нет. \n{neme_player} не получает очков.')
            random_list_player = random_list_player + handing_random_letters(count - len(random_list_player) + 1)
            print(f'Добавляю буквы"', ', '.join(random_list_player), '"')
            print('-------------------------------')
            return [balls_player, random_list_player]


if __name__ == '__main__':
    # Здесь происходит вся логика игры
    loading_from_text_files()
    print('Привет. Мы начинаем играть в Scrabble')
    balls_player1 = 0
    balls_player2 = 0
    neme_player1 = chek_name('Как зовут первого игрока? ')
    neme_player2 = chek_name('Как зовут второго игрока? ')
    print(f'{neme_player1} vs {neme_player2} (раздаю случайные буквы)')
    count = 7
    random_list_player1 = handing_random_letters(count)
    random_list_player2 = handing_random_letters(count)
    print(f'{neme_player1} - буквы "',', '.join(random_list_player1),'"')
    print(f'{neme_player2} - буквы "', ', '.join(random_list_player2), '"')
    print('-------------------------------')
    while True:
        #  Начинается логика хода игрока1
        rez = player_move(random_list_player1, neme_player1, count)
        balls = rez[0]
        random_list_player1 = rez[1]
        if balls >= 0:
            balls_player1 += balls
        else:
            break
        #  Начинается логика хода игрока2
        rez = player_move(random_list_player2, neme_player2, count)
        balls = rez[0]
        random_list_player2 = rez[1]
        if balls >= 0:
            balls_player2 += balls
        else:
            break
        count += 1
    if balls_player1 > balls_player2:
        print(f'Выиграл {neme_player1}.\n Счет {balls_player1}:{balls_player2}')
    elif balls_player1 == balls_player2:
        print(f'Ничья.\n Счет {balls_player1}:{balls_player2}')
    else:
        print(f'Выиграл {neme_player2}.\n Счет {balls_player1}:{balls_player2}')


