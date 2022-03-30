# What is it

This project is add on to the Opennebula, which allow to create auto stands to the developers.

## Installation

I assume that you have already installed the repository.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install env.

```bash
python -m pip install -r requirements.txt
```

## First steps

Before the starting of the application you must appoint ENV variables in Linux

```bash
export LDAP_USER="uid=admin,cn=users,cn=accounts,dc=example,dc=com"
export LDAP_PASSWORD="your_admin_password"
export SECRET_KEY="SeCrEt_KeY"
export DATABASE="/tmp/flsite.db"
```

or in Windows

```console
SET LDAP_USER="uid=admin,cn=users,cn=accounts,dc=example,dc=com"
SET LDAP_PASSWORD="your_admin_password"
SET SECRET_KEY="SeCrEt_KeY"
SET DATABASE="/tmp/flsite.db"
```

and after that create your Data Base in python terminal


```python
import app.py

create_db()

```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Comming soon
Добавить подключение к лдап 

Добавить подключение к jenkins

Вынести всю конфигурацию и секреты 

OAuth2 

Уязвимость sql injection

## License
[MIT](https://choosealicense.com/licenses/mit/)