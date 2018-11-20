# DB Connection Toolbelt - DBConnecToolbelt

Offers a toolbelt for everyday work and scripts done by the BS&A team.

## Installation or Upgrade
To install the DBConnecToolbelt just execute the following:
~~~
pip3 install git+https://github.com/andresionek91/dbconnectoolbelt --upgrade
~~~

## What does this Toolbelt do?

### Connection to PostgreSQL
Use it to connect to our SQL databases. It returns connection objects using 
either `psycopg2`, `records` or `SQLAlchemy`.

~~~
from bsatoolbelt.connection import PostgreSQL
~~~

#### Available methods

* PostgreSQL
    * psycopg2 - *returns a connection object*
    * records - *returns a connection object*
    * sqlalchemy - *returns an engine object*
    * get_records_as_dict
    * execute_sql - *just execute SQL, doesn't return anything*
    * df_to_sql
    * create_index
    * insert_dict_record

~~~
from bsatoolbelt import utils
~~~

* utils.format_dict_str - Transform all dict values into strings
* dec2float - Checks all items of dictionary and converts Decimal types to float



## Setting-up Environmental Variables
### Running on Shell
1) Create a `.env` file on the same directory as the script you are building.
1) Add all env vars in the file as folowing:
    ~~~
    HOST=ec2.256...
    DATABASE=d8r31....
    ~~~       
1) Run the following shell command before running the script: 
    ~~~
    set -a; source .env;set +a
    ~~~

### Running on PyCharm
1) Go to Run menu, then Edit Configurations...
1) If there is no template created, click on + button then select Python
1) On Environment Variables, click on the folder button
1) Add all the variables then apply and exit the window

