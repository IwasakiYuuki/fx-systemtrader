ifndef PROJECT_ID
		export PROJECT_ID=fx-systemtrader-dev
endif
ifndef SHORT_SHA
		export SHORT_SHA=default
endif

# 以下で指定したサブディレクトリ全てにmakeを行う．
SUBDIRS := \
	cloud_functions \
	dummy_api 

# テスト
check: $(SUBDIRS)
	@echo "check done"

# dockerイメージのビルド
build: $(SUBDIRS)
	@echo "build done"

# dockerイメージのプッシュ
push: $(SUBDIRS)
	@echo "push done"

# virtualenv環境の削除
clean: $(SUBDIRS)
	@echo "clean done"

# サブディレクトリへ再帰的にmakeを行う．
$(SUBDIRS):
	make -e -C $@ $(MAKECMDGOALS)

define spushd
pushd $1  > /dev/null
endef

define spopd
popd $1 > /dev/null
endef

.PHONY: check build push clean $(SUBDIRS) 
