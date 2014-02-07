# Makefile for cloudstack-ec2api


SHELL    = /bin/sh

PYTHON   = python

SETUP        = setup.py
BUILD_CMD    = build
INSTALL_CMD  = install
TEST_CMD     = test
SDIST_CMD    = sdist
BDISTEGG_CMD = bdist_egg
REGISTER_CMD = register
UPLOAD_CMD   = upload


GIT = git

RST2HTML = rst2html.py --strict

DIST_VERSION   = $(shell $(PYTHON) setup.py --version)
RELEASE_BRANCH = master
RELEASE_REMOTE = origin

all: clean dist

help:
####@echo "Please use \`make <target>' where <target> is one of"
####@echo "  clean     To remove temporary build files and compile Python files"
####@echo "  dist      to make cloudstack-ec2api source distribution"
####@echo "  install   to install cloudstack-ec2api"
####@echo "  register  to Create/update cloudstack-ec2api v$(DIST_VERSION) pypi page."
####@echo "  release   to tag and release a new version of cloudstack-ec2api to pypi"
####@echo "  upload    to upload the source distribution to pypi"
####@echo "            (to use a release got tagged but the upload to pypi failed)"
####@echo "  MANIFEST.in"
####@echo "            to make MANIFEST.in from the list of files tracked by git"
####@echo "  README.html"
####@echo "            to make convert README.rst to html and test the result"
####@echo "            in your browser"

build: clean
####@echo "Building squeleton package..."
####$(PYTHON) $(SETUP) $(BUILD_CMD)
####@echo

clean:
####@echo "Removing build and dist directories, and pyc files..."
####rm -rf ./docs/_build/*
####rm -rf ./build/
####rm -rf ./dist/
####rm -rf ./v
####rm -f README.html
####rm -f HISTORY.html
####rm -f distribute-*.egg
####find . -name "*.pyc" -print0 | xargs -0 rm
####@echo

dist: clean
####@echo "Building src distribution of skeleton..."
####$(PYTHON) $(SETUP) $(SDIST_CMD)
####@echo

install: clean
####$(PYTHON) $(SETUP) $(INSTALL_CMD)

readme: README.html HISTORY.html

register: README.html HISTORY.html
####@echo "Creating or updating skeleton v$(DIST_VERSION) pypi page."
####$(PYTHON) $(SETUP) $(REGISTER_CMD)

release: clean MANIFEST.in readme tag upload
####@echo "Version $(DIST_VERSION) released."
####@echo

tag:
####@echo "Tagging version $(DIST_VERSION)..."
####$(GIT) pull $(RELEASE_REMOTE) $(RELEASE_BRANCH)
####$(GIT) tag v$(DIST_VERSION)
####$(GIT) push $(RELEASE_REMOTE) v$(DIST_VERSION)
####@echo

upload:
####@echo "Uploading source distribution to pypi..."
####$(PYTHON) $(SETUP) $(REGISTER_CMD) $(SDIST_CMD) $(UPLOAD_CMD)
####@echo

upload-egg-%:
####@echo "Uploading to pypi egg distribution for $(PYTHON$*)..."
####$(PYTHON$*) $(SETUP) $(REGISTER_CMD) $(BDISTEGG_CMD) $(UPLOAD_CMD)
####@echo

MANIFEST.in:
####@echo "Update MANIFEST.in..."
####$(GIT) ls-files --ignore --exclude="*.py" --exclude="*.rst" --exclude="*.conf" --exclude="LICENSE" | sed -e 's/^/include /g' > ./MANIFEST.in
####@echo

%.html: %.rst
####@echo "Making $@..."
####$(RST2HTML) $^ > $@
####$(PYTHON) -c "import os, webbrowser as w; w.open('file://%s/$@' % os.getcwd());"

.PHONY: MANIFEST.in clean tag
