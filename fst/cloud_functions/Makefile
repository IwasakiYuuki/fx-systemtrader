SUBDIRS := $(wildcard */)

install: $(SUBDIRS)
	@echo "install done"
	
check: $(SUBDIRS)
	@echo "clean done"

clean: $(SUBDIRS)
	@echo "clean done"

$(SUBDIRS):
	make -C $@ $(MAKECMDGOALS)

.PHONY: install clean $(SUBDIRS) 
