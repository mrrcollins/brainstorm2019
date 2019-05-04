# Using MySQL and GAM to manage student accounts

Here are the scripts and notes from my presentation for BrainStorm Sandusky 2019 on managing student accounts.

The presentation [is available in Google Slides](https://docs.google.com/presentation/d/1P5umFjlrmPQ-DIM9-Du77Ards1tqbZM8ZIgZTXknsBQ/preview)

# Prerequisites

Python needs the MySQLdb module:

    sudo apt update
    sudo apt install python-pip python-dev libmysqlclient-dev
    sudo pip install mysqlclient

Python xlwt module to create Excel files:

    sudo pip install xlwt

# Scripts and files

* [anonschedule.csv](anonschedule.csv) - A sample schedule file

# GAM - Command Line Google Apps Manager

[jay0lee/GAM: command line management for Google G Suite](https://github.com/jay0lee/GAM)

[GAM Bulk Operations](https://github.com/jay0lee/GAM/wiki/BulkOperations)

No command line? No problem, use [Google Cloudshell](https://console.cloud.google.com/cloudshell/)
