# Database-toolkit

This library allows you to create databases (including temporal databases) based on the
PostgreSQL.

## Table of contents


* [Installation](#installation)
* [Quick start](#quick-start)
* [TODO list](#todo-list)


## Installation

Successful library operations require:
1. [Install PostgreSQL](https://www.postgresql.org/download/)

2. [Install GraphViz](https://www.graphviz.org/download/)(Optional)

3. [Register at Hugging Face](https://huggingface.co/) and get API key(Optional)

4. Install the library for creating the database
    ```sh
    pip install git+https://github.com/Easycoding-art/Database_toolkit.git
    ```

## Quick start

1. In a text document, specify a database description in the following form:

'''
$temporal$
property<property_id>{
    id(integer)[user: user_id]“not_null”,
    name(integer)
};
user<user_id>{
    user_id(integer),
    password(integer)
};
'''
-----------------------------------------------------------------------------------------
$temporal$ - Indicates that the database is temporal(imposes a number of restrictions). Not
required.
property and user - table names
In <> the primary key is written
In tables, the column names are listed comma separated. In () the data type is specified
PostgreSQL. In [] through & write the relationship to the column in “table : column" format. Additional information in “” lists separated by +(you can specify your own in SQL).
For example:
default - DEFAULT
not_null - NOT NULL
auto_inkrement - GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 )
There are no indentation restrictions.

2. Using the library, create a database by passing the PostgreSQL name, password and path to the file with the description of the database to the constructor.
and the path to the file with the description.

3. fill_fake_data method takes a dictionary of row number intervals as a 
tuple(For example: {'user':(1, 200), 'adress':(1, 140)}), language(default “ru_RU”), autofill mode
(True by default) and functions for generating data by keys that match the names of the
column names(For example: user = get_users). The signature of each function should be as follows:
def func(n: int) -> list
The names of the fields for which data is generated automatically: first_name, last_name,
full_name, email, password, phone_number, job, company, date, url, website.
Texts in Russian are created by the GetRandomText function.

4. set_query returns a dataframe with the result in response to an SQL query.

5. Alternatively, use the LLM assistant to create the database as in the example.
    ```sh
    import db_toolkit
    key = "hf_key"
    name = 'Social Network'
    description = 'The "Social Network" database is designed to manage and facilitate user interactions within an online platform.'
    agent = db_toolkit.LLMAssistant(key, name, description)
    agent.set_db('my_password', dev_mode=True)
    ```

## TODO list

- [X] Add creation of database schemas from user's description using LLM
- [ ] Add data generation from user's description using LLM