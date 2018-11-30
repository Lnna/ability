#! /usr/bin/env bash


read -p "please input name" -t 5 -n 4 -s pwd

echo -e "\npwd is: $pwd It is a test." > test.txt

echo `date` > test.txt
