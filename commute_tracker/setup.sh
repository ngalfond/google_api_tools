#!/usr/bin/env bash

declare -A env_vars

env_vars['home address']=HOME_ADDRESS
env_vars['work address']=WORK_ADDRESS
env_vars['log file']=LOG_FILE
env_vars['email contact']=CONTACT
env_vars['API key']=GOOGLE_API_KEY


for i in "${!env_vars[@]}"
do
    if [[ -n ${!env_vars[$i]} ]]; then
        echo "Your $i already exists, do you want to replace it? (y/n)"
        read response
        if [ ${response} = "n" ]; then
            :
        elif [ ${response} = "y" ]; then
            sed -i "/${env_vars[$i]}/d" ~/.bash_profile
            printf "What is your new $i?\n>"
            read val
            printf "export ${env_vars[$i]}=\'${val}\'\n" >> ~/.bash_profile
        else
            echo "invalid response"
        fi
    else
        printf "What is your $i?\n>"
        read input
        printf "export ${env_vars[$i]}=\'${input}\'\n" >> ~/.bash_profile
    fi
done

sed -i "/SNMP_SERVER/d" ~/.bash_profile
sed -i "/SNMP_LOGIN/d" ~/.bash_profile
server='free.smtp.access@gmail.com'
login='wygh lbzb ravz vapu'
printf "export SNMP_SERVER=\'${server}\'\n" >> ~/.bash_profile
printf "export SNMP_LOGIN=\'${login}\'\n" >> ~/.bash_profile

exec $SHELL
