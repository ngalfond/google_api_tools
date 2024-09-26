#!/usr/bin/env bash

echo "What is your home address?
>"
read home
printf "export HOME_ADDRESS=\'${home}\'\n" >> ~/.bashrc
##
echo "What is your work address?
>"
read work
printf "export WORK_ADDRESS=\'${work}\'\n" >> ~/.bashrc
##
echo "What file do want to store historical data in?
>"
read log
printf "export LOG_FILE=\'${log}\'\n" >> ~/.bashrc
##
echo "What email address do you want to get alerts to?
>"
read contact
printf "export CONTACT=\'${contact}\'\n" >> ~/.bashrc
##

api='AIzaSyBUbL5MXEsIBWaCTodfTJl6XjQaEAPaCEg'
server='free.smtp.access@gmail.com'
login='ynqr qoxt omyw nlng'

printf "export GOOGLE_API_KEY=\'${api}\'\n" >> ~/.bashrc
printf "export SNMP_SERVER=\'${server}\'\n" >> ~/.bashrc
printf "export SNMP_LOGIN=\'${login}\'\n" >> ~/.bashrc

exec $SHELL
