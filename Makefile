define ALL
	update-requirements
endef
ALL:=$(shell echo $(ALL))  # to remove line-feeds

define REQUIREMENTS_FILES
	requirements-dev.txt
	requirements-test.txt
	requirements.txt
endef
REQUIREMENTS_FILES:=$(shell echo $(REQUIREMENTS_FILES))

define REQUIREMENTS_IN
	requirements.in
endef
REQUIREMENTS_IN:=$(shell echo $(REQUIREMENTS_IN))

define REQUIREMENTS_IN_TEST
	requirements-test.in
	requirements.in
endef
REQUIREMENTS_IN_TEST:=$(shell echo $(REQUIREMENTS_IN_TEST))

define REQUIREMENTS_IN_DEV
	requirements-dev.in
	requirements-test.in
	requirements.in
endef
REQUIREMENTS_IN_DEV:=$(shell echo $(REQUIREMENTS_IN_DEV))

offline?=0

ifeq (1,$(offline))
PIP_NO_INDEX:=--no-index
endif

FIND_LINKS:=-f virtualenv_support


.PHONY: all
all: $(ALL)

.PHONY: update-requirements
update-requirements: $(REQUIREMENTS_FILES)
	python setup.py pip_sync $(FIND_LINKS) $(PIP_NO_INDEX) -r requirements-dev.txt

requirements.txt: $(REQUIREMENTS_IN)
	. bin/activate && pip-compile $(FIND_LINKS) $(PIP_NO_INDEX) $(pip-compile-options) -o $@ $^
	. bin/activate && pip wheel $(FIND_LINKS) $(PIP_NO_INDEX) --no-deps -r $@ -w virtualenv_support

requirements-test.txt: $(REQUIREMENTS_IN_TEST)
	. bin/activate && pip-compile $(FIND_LINKS) $(PIP_NO_INDEX) $(pip-compile-options) -o $@ $^
	. bin/activate && pip wheel $(FIND_LINKS) $(PIP_NO_INDEX) --no-deps -r $@

requirements-dev.txt: $(REQUIREMENTS_IN_DEV)
	. bin/activate && pip-compile $(FIND_LINKS) $(PIP_NO_INDEX) $(pip-compile-options) -o $@ $^
	. bin/activate && pip wheel $(FIND_LINKS) $(PIP_NO_INDEX) --no-deps -r $@

.PHONY: bootstrap-virtualenv
bootstrap-virtualenv.py: requirements.txt bootstrap-virtualenv.in
	python setup.py virtualenv_bootstrap_script -o $@ -r $<
