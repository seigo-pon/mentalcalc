#!/bin/sh

rm skill.zip
cd ./skill
cp ../calc.py .
cp ../mental_calc.py .
zip ../skill.zip .  -r
