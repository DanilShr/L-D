# Rest api
Rest - (representation state transfer) это архитектурный стиль который работает поверх протокола HTTP обеспечивая
межсетвое взаимодействие. 

Rest api - это api которое реализованно по принципам REST.

Для создания rest api в django используется djangorestframework, и перед началом работы с ним необходимо его установить 
командой 
```python
pip install djangorestframework
```
Также необходимо подключить 'rest_framework' в настройки приложения
Дополнительно в настройках указываются сами настройки rest в данном случае настраивается пагинация. Пагинация позволяет
сократить нагрузку на базу данных выдавая лишь ограниченной пул данных 
```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
```
Пример создания приложения с использованием rest api:
```python
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view


@api_view() #декоратор, который помечает как api view функция
def hello_world_view(request: Request) -> Response:
    return Response({"message": "Hello World!"})
```

Пример создания класса в Rest framework при помощи APIView
```python
class GroupsListView(APIView):
    def get(self, request: Request) -> Response:
        groups = Group.objects.all()
        data = [group.name for group in groups]
        return Response({"groups": data})

    def post(self, request: Request) -> Response:
        pass
```

### Серилизатор
Серилизатор в django rest framework это инструмент, который позволяет преобразовывать сложные типы данных такие как 
модели django в форматы которые можно передавать по сети (json, html). Также они позволяются проверять полученный от 
клиента данные на соответствие требованиям.

Пример использования:
```python
#serializers
from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = 'pk', 'name'


#views
class GroupsListView(APIView):
    def get(self, request: Request) -> Response:
        groups = Group.objects.all()
        serialized = GroupSerializer(groups, many=True)
        return Response({"groups": serialized.data})
```

### Mixins в REST

Mixins - предоставляют различную функциональность которую можно добавить к своим view классам. Он предоставляет различные
инструменты:
1. Хэширование данных
2. Авторизации
3. Валидации данных

Пример использования mixins. Mixins можно использовать только с объектом GenericAPIView
```python
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin


class GroupsListView(ListModelMixin, GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)
```

Есть объект ListCreateAPIView который позволяет отображать и создавать объекты модели

```python
class GroupsListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
```

## ViewSet
ViewSet это инструмент в django rest имеющий весь необходимый функционал для выполнения CRUD операций
```python
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,

    ]
    search_fields = ['name', 'description']
    filterset_fields = ('name', 'price', 'description', 'discount')
```

## Filter
Для того чтобы настроить фильтрацию в django api необходимо установить соответсвующую библиотеку
```python
pip install django-filter
```
В настройках приложения необходимо подключить новое приложение
```python
'django_filters',
```
Также в настройках Rest Framework необходимо указать фильтрацию по умолчанию
```python
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ]
```
В views указываем filterset_fields - это поля по котором будет проходить фильтрация
```python
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_fields = ('name', 'price', 'description', 'discount')
```

Также можно реализовать поисковый фильтр по заданным полям, для этого необходимо подключить библиотеку SearchFilter

```python
from rest_framework.filters import SearchFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer 
    filter_backends = [
        SearchFilter,
    ] # указываем какой фильтр на бэкэнде будет использоваться 
    search_fields = ['name', 'description'] #указываем поля по которым будет происходить поиск
```
Сортировка является частью фильтрации и также указывается в поле filter_backend с указанием полей по которым будет 
проводиться фильтрация
```python
    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,

    ]
    ordering_fields = ['name', 'price', 'description', 'discount']
```