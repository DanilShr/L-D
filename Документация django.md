# Документация в django
## Документация в административной панели django
Для работы с документацией в административной панели django необходимо установить дополнительный пакет
```python
pip install docutils
```
После установки необходимо подключить в настройках новое приложение
```python
'django.contrib.admindocs'
```
И подключить middleware
```python
'django.contrib.admindocs.middleware.XViewMiddleware'
```
Чтобы получить доступ к страницам документации требуется в настройках urls добавить ссылку на документацию
```python
path('admin/doc', include('django.contrib.admindocs.urls'))
```
## Документация в REST API
В api можно получить информацию об объекте нажав кнопку OPTIONS. Но при полученной информации будет пустое поле 
descriptions. Данное поле можно заполнить при помощи docstring в описании view модели 
```python
    '''
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    model:
    '''
```
Для подробной документации можно использовать специальным расширением для flake8
```python
pip install flake8
pip install flake8-docstrings
```
Линтер flake8 - это специальный инструмент для проверки кода на соответствие стиля pep8

## Open Api
Open api (swagger) - это свод правил который используется для описания restfull api. Open api используют для указания 
спецификации запросов и ответов которые должен возвращать сервер, а также его используют для описания путей,
форматов и прочей мета информации

Можно выделить два основных пакета для django rest framework которые позволяют генерировать open api:
1. DRF spectacular
```python
pip install drf-spectacular
```
После установки необходимо подключить приложение в настройках, а также нужно добавить настройки rest framework
```python
    'drf-spectacular',

#######################
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', #Этот объект будет использован как базовый 
                                                                  #класс для всех схем в rest api
}

SPECTACULAR_SETTINGS = {
    "TITLE": 'My Site Project API',
    "DESCRIPTION": 'My site with shop add adn custom auth',
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False, #настройка для того чтобы не показывать информацию по странице документации
}
```
Также необходимо в urls указать пути для получения документации
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shopapp.urls')),
    path('myauth/', include('myauth.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/', include('myapiapp.urls')),
]
```

Для указания дополнительной информации в swagger view класса можно использовать декоратор extend_schema, а также для
добавления информации по каждому из методов CRUD, необходимо переопределить родительский метод и добавить декоратор extend_schema
```python
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
##############################################
   @extend_schema(
        summary='Get one product by ID',
        description='Retrieve **product**, returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Product not found" ),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
    @extend_schema(
        summary='Update product',
        description='Update **product**, returns 401 or error product',
        responses={
            200: ProductSerializer,
            401: OpenApiResponse(description="Error update"),
        }
    )
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)


```