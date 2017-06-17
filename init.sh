#!/bin/bash


VIRTUAL_ENV_BASE="virtual_env"



if [ ! -d $VIRTUAL_ENV_BASE ]; then 
  virtualenv -p /usr/local/bin/python3 $VIRTUAL_ENV_BASE 
  . $VIRTUAL_ENV_BASE/bin/activate

  pip install yahoo-finance
  pip install PyMySQL
fi


