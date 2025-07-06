# Эффективное взаимодействие с БД
## Оптимизация работы с БД
Оптимизация работы с БД подрузомевает соблюдение нескольких принципов:
1. Индексы - индексы в бд нужны для ускорения сортировки и фильтрации строк. Они представляют собой струткуры данных 
которые хранятся отдельно от строк основной таблицы и содержат в себе информацию о том какие записи где находятся и какую 
информацию содержат. Установка индекса на определенное поле сильно ускорит скорость обработки запросов.
```python
name = models.CharField(max_length=100, db_index=True)
```
2. Нормализация БД

## Логирование SQL запросов
Для настройки логирования запросов необходимо проинициализировать в настройках правила для логирования
```python
LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
           '()': 'django.utils.log.RequireDebugTrue', #специальный фильтр позволяющий выводить логи только если в настройках приложения указан DEBUG
        },
    },
    'handlers': {
        'console': { #обработчик который использует уровень DEBUG, также он отсеевает логи в случае если приложение не в debug режиме
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': { #взаимодействие с бд должно использовать обработчик console
            'level': 'DEBUG',
            'handler': ['console'],
        },
    },
}
}
```

## Транзакции
Для того чтобы исопльзовать транзакции в django необходимо использовать декоратор transaction из модуля django.db для 
создания атомарных запросов (т.е. запросы которые выполняются как одно целое, и если где-то произойдет ошибка, транзакция
откатит запрос)
```python
from django.db import transaction


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with product")
        user = User.objects.get(username="admin")
        products: Sequence[Product] = Product.objects.all()
        order, created = Order.objects.get_or_create(
            delivery_address="ul Ivanova, d 8",
            promocode="NEW123",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Created order {order}")
```

## Оптимизация запросов
### Подгрузка данных по выбранному параметру
Для того чтобы получить данные по определенным полям в виде кортежа необходимо воспользоваться values_list
```python
users_info = User.objects.values_list("pk", "username")
```
Если запрашивается один элемент можно указать флаг flat=True для того чтобы сформировать результаты запроса в один список

**defer** - функция позволяющая делать ленивую загрузку только в момент когда данный объект используется, она возращает объект
и позволят установить поля которые не требуются при выборке
```python
products: Sequence[Product] = Product.objects.defer("description", "price", "created_at")
```
```sqlite-sql
SELECT "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."discount", "shopapp_product"."archived", "shopapp_product"."preview" FROM "shopapp_product" ORDER BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC; args=(); alias=default
```

**only** - функция обратная **defer** позволяет выбрать только определенное поле

## Массовые вставки и обновления
В django массовые вставки и обновления можно делать при помощи bulk_create, bulk_update

```python
        info = [
            ('Smartphone 1', 2999),
            ('Iphone 2', 3922),
            ('Realme', 2000),
        ]

        product = [
            Product(name=name, price=price)
            for name, price in info
        ]

        result = Product.objects.bulk_create(product)
```
Функция update
```python
        result = Product.objects.filter(
            name__contains="Smartphone",
        ).update(discount=10)
```