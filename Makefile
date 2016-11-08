define ALL
	update-requirements
	update-wheelhouse
endef
ALL:=$(shell echo $(ALL))  # to remove line-feeds

define REQUIREMENTS_FILES
	requirements-dev.txt
	requirements.txt
endef
REQUIREMENTS_FILES:=$(shell echo $(REQUIREMENTS_FILES))

define REQUIREMENTS_IN
	requirements.in
endef
REQUIREMENTS_IN:=$(shell echo $(REQUIREMENTS_IN))

define REQUIREMENTS_IN_DEV
	requirements-dev.in
	requirements-test.in
	requirements.in
endef
REQUIREMENTS_IN_DEV:=$(shell echo $(REQUIREMENTS_IN_DEV))

offline?=0


all: $(ALL)

.PHONY: update-requirements

ifeq (1,$(offline))
PIP_NO_INDEX:=--no-index
endif

FIND_LINKS:=-f virtualenv_support

update-requirements: $(REQUIREMENTS_FILES)
	python setup.py pip_sync $(FIND_LINKS) $(PIP_NO_INDEX) -r requirements-dev.txt

requirements.txt: $(REQUIREMENTS_IN)
	python setup.py pip_compile $(FIND_LINKS) $(PIP_NO_INDEX) -o $@ -c "$^"

requirements-dev.txt: $(REQUIREMENTS_IN_DEV)
	python setup.py pip_compile $(FIND_LINKS) $(PIP_NO_INDEX) -o $@ -c "$^"

.PHONY: update-wheelhouse
update-wheelhouse: bootstrap-virtualenv.py
bootstrap-virtualenv.py: requirements.txt bootstrap-virtualenv.in
	python setup.py virtualenv_bootstrap_script -o $@ -r $<
