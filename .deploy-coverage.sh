#!/bin/bash
cd ../
git config --global user.email "travisci@ianduffy.ie"
git config --global user.name "travis-ci"
git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/imduffy15/ec2stack gh-pages > /dev/null

# Commit and Push the Changes
cd gh-pages
rm -rf *
cp -Rf ../ec2stack/cover/* .
git add -f .
git commit -a -m "[AUTO-PUSH] Latest coverage report on successful travis build"
git push -fq origin gh-pages > /dev/null
