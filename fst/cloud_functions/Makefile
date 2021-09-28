SHELL=/bin/bash
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
SUBDIRS := $(wildcard */)
OPTIONS := install check clean


define check
	cd $1; \
	. venv/bin/activate && python -m pytest; \
	deactivate

endef

define clean
	cd $1; \
	rm -rf ./venv

endef

define create-venv-rule
$(1): $(1)$(VENV)/touchfile

endef


check: $(SUBDIRS)
	$(foreach d,$^,$(call check,$(d)))

$(foreach d,$(SUBDIRS),$(eval $(call create-venv-rule,$(d))))

%/$(VENV): %/$(VENV)/touchfile

%/$(VENV)/touchfile: %/requirements.txt
	python3 -m venv $*/$(VENV)
	$*/$(PIP) install -r $^
	touch $@

clean:
	$(foreach d,$^,$(call clean,$(d)))

build:
	@echo "Nothing to do"

push:
	@echo "Nothing to do"


.PHONY: check clean
