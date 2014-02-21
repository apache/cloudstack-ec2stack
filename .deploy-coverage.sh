#!/bin/sh
cd ../
git config --global user.email "travis@travis-ci.org"
git config --global user.name "travis-ci"
git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/imduffy15/ec2stack gh-pages > /dev/null

# Commit and Push the Changes
cd gh-pages
git rm -rf *
cp -Rf ../ec2stack/cover/* .
git add -f .
git commit -a -m "[AUTO-PUSH] Latest coverage report on successful travis build"
git push -fq origin gh-pages > /dev/null
