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

 