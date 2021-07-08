#!/bin/bash

echo "tD9#Lk4.u" | dropdb -U postgres trivia_test
echo "tD9#Lk4.u" | createdb -U postgres trivia_test
echo "tD9#Lk4.u" | psql -U postgres trivia_test < trivia.psql
python test_flaskr.py
