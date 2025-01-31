# FinApp 

This project simulates a financial institution and how it tracks monetary transactions and financial account balances

## Requirements 

In order to run the project locally, you must have the following packages installed 

* Make 
  * [Make-GNU-Documentation](https://www.gnu.org/software/make/)
* Python 3.12.7
* Poetry 1.8.3
* Docker

## How to run 

This project uses MakeFile to simplify the runnable commands, you can check the commands that I used on this file

In terminal, you have to be in the fin-app folder to run the commands

* To run the unit tests, you have to install local dependencies on venv, and then you can run the tests command, run in the commands in the following order:
```
make local/install
make tests/unit
  ```

* To run the project on docker you must run this command on terminal:
```
make docker/local/enviroment
```


### About the project
I used Django framework in order to connect to external components, and I design the service using
hexagonal architecture, all the business logic is inside the domains, respecting domain driven design

Here we have three domains: Account, Transfer and Transactions 

Account: responsible for the account management 
Transactions: responsible to have all the cash in and out values to a single account
Transfer: responsible to transfer money between accounts, adding transactions of cash in and out to Accounts

