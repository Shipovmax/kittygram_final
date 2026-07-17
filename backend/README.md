### How to run the project:

Clone the repository and change into it on the command line:

```
git clone https://github.com/yandex-praktikum/kittygram_backend.git
```

```
cd kittygram_backend
```

Create and activate a virtual environment:

```
python3 -m venv env
```

* If you're on Linux/macOS

    ```
    source env/bin/activate
    ```

* If you're on Windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Install dependencies from requirements.txt:

```
pip install -r requirements.txt
```

Run migrations:

```
python3 manage.py migrate
```

Start the project:

```
python3 manage.py runserver
```
