#!/bin/bash

while true; do
  cd  /repository
  git reset --hard HEAD
  git checkout master
  git pull origin master 

  cd  /code
  python  run.py

  echo "Waiting 1m..."
  sleep 1m
done
