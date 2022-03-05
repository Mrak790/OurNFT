# OurNFT

Windows:

1. Install venv for creating virtual environments:
   
```python
pip install virtualenv
```
2. Create new environment called 'ournft-env':
   
```python
python -m venv ournft-env
```
3. Go to directory with repository and turn the environment on:
   
```python
./ournft-env/Scripts/activate
``` 
To turn off the environment:

```python
deactivate
```

4. Install all required modules (use after activating environment)
```python
pip install -r requirements.txt
```
5. Ask for file with secrets in our chat.

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver