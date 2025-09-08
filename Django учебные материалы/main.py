import re

# 2. Проверка на палиндром
# Задача: Напишите функцию, которая проверяет, является ли строка палиндромом (читается одинаково слева направо и справа налево).



def pallindrome(word):
    cleaned = word.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


word = input('Введите слово')
result  = pallindrome(word)
print(result)


# 3. Подсчёт вхождений элемента в списке
# Задача: Напишите функцию, которая подсчитывает количество вхождений элемента в списке.

def count(elem):
    result = list.count(elem)
    return result

elem = input('Введите элемент')
list = [1,2,3,2,4,2,21,1,3,4,5]
print(count(elem))

