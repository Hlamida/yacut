Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Hlamida/yacut
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создайте базу данных, выполнив последовательно команды:
```
flask shell
```
```
from yacut import db
```
```
db.create_all()
```
```
exit()
```

Запустите сервер на http://127.0.0.1:5000:
```
flask run --reload
```



Технологический стек:
Python, Flask, SQLAlchemy

Автор: Кулагин Александр
```
https://github.com/Hlamida
```



