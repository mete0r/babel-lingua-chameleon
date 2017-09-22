define ALL
	update-requirements
endef
ALL:=$(shell echo $(ALL))  # to remove line-feeds

define REQUIREMENTS_FILES
	requirements-dev.txt
	requirements-docs.txt
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
	requirements-docs.in
	requirements-test.in
	requirements.in
endef
REQUIREMENTS_IN_DEV:=$(shell echo $(REQUIREMENTS_IN_DEV))

offline?=0

ifeq (1,$(offline))
PIP_NO_INDEX:=--no-index
endif

FIND_LINKS:=-f virtualenv_support
VENV	:= . bin/activate &&


.PHONY: all
all: $(ALL)

.PHONY: update-requirements
update-requirements: .pip-sync
.pip-sync: $(REQUIREMENTS_FILES)
	$(VENV) pip-sync $(FIND_LINKS) $(PIP_NO_INDEX) requirements-dev.txt
	$(VENV) pip freeze > .pip-sync

requirements.txt: $(REQUIREMENTS_IN)
	$(VENV)	pip-compile $(FIND_LINKS) $(PIP_NO_INDEX) $(pip-compile-options) -o $@ $^
	$(VENV)	pip wheel $(FIND_LINKS) $(PIP_NO_INDEX) --no-deps -r $@ -w virtualenv_support

requirements-test.txt: $(REQUIREMENTS_IN_TEST)
	$(VENV) pip-compile $(FIND_LINKS) $(PIP_NO_INDEX) $(pip-compile-options) -o $@ $^
	$(VENV) pip wheel $(FIND_LINKS) $(PIP_NO_INDEX) --no-deps -r $@

requirements-docs.txt: $(REQUIREMENTS_IN_DOCS)
	$(VENV) pip-compile $(FIND_LINKS) $(PIP_NO_INDEX) $(pip-compile-options) -o $@ $^
	$(VENV) pip wheel $(FIND_LINKS) $(PIP_NO_INDEX) --no-deps -r $@

requirements-dev.txt: $(REQUIREMENTS_IN_DEV)
	$(VENV) pip-compile $(FIND_LINKS) $(PIP_NO_INDEX) $(pip-compile-options) -o $@ $^
	$(VENV) pip wheel $(FIND_LINKS) $(PIP_NO_INDEX) --no-deps -r $@

.PHONY: bootstrap-virtualenv
bootstrap-virtualenv.py: requirements.txt bootstrap-virtualenv.in
	python setup.py virtualenv_bootstrap_script -o $@ -r $<


.PHONY: notebook
notebook:
	$(VENV)	jupyter notebook --notebook-dir=notebooks
