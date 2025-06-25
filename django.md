# Работа с файлами FileField

Концепция хранения и использования статических файлов подразумевает что все статические файлы находятся 
в файловой системе. Информация о файле находится в базе данных в виде информации о пути к нему. Сервер при обработке
запросов будет автоматически отдавать статические файлы согласно указанным путям

В режиме разработки выдачей файлов может заниматься тестовый сервер, а реальных задачах этим занимается настоящий 
веб-сервер такой, как NGINX

### Настройка выдачи изображений в тестовой среде
1. Необходимо модифицировать urls. Сначала необходимо проверить состояние сервера в каком режиме он находится (разработка).
Необходимо выполнить проверку
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    #ссылки которые вернутся при выполнении static
    urlpatterns.extend(
        static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
    )
    
```
2. Указать переменные (MEDIA_URL, MEDIA_ROOT) в настройках приложения settings
```python
MEDIA_URL = 'media/' #путь по которому можно получить медиа через адресную строку
MEDIA_ROOT = BASE_DIR / 'uploads' #путь по которому будут, находится статичные файлы
    
```
## FileField
FileField - объект, который позволяет загрузить и сохранить файлы на диске.
Тип поля в models обозначается следующим образом
```python
    receipt = models.FileField(blank=True, null=True, upload_to="orders/receipts") #указывается маршрут куда сохранять файлы 
```
Файлы можно глобально разделить на два типа:
1. Это статика, которая идет в комплекте с приложением. В режиме тестирования необходимо также переназначить хранилище статики
```python
STATIC_URL = 'static/' #путь по которому можно получить медиа через адресную строку
STATIC_ROOT = BASE_DIR / 'uploads' #путь по которому будут, находится статичные файлы
    
```
2. Вторая группа статичных файлов - это media files, обычно они служат для отображения динамического контента
на странице. Обычно эти файлы постоянно меняются.


## ImageField
Для работы с изображениями в python есть специальный класс ImageField.  Но для начало работы с изображениями в django 
необходимо установить библиотеку pillow - отвечающую за работу с изображениями

Пример создания поля ImageField в models

```python
    preview = models.ImageField(blank=True, null=True, upload_to=product_preview_directory_path)
```
Где product_preview_directory_path - это кастомная функция отвечающая создание путей для файлов
```python
def product_preview_directory_path(instance: "Product", filename: str):
    return f"products/product_{instance.pk}/preview/{filename}"
```
Отображение в HTML разметке
```HTML
  {% product.preview %}
      <img src="{{ product.preview.url }}" alt="{{ product.preview.name }}">
  {% endif %}
```
Для загрузки файлов через форму необходимо выставить следующие настойки:
```HTML
 <form method="post" enctype="multipart/form-data">
```

### Загрузка нескольких изображений