# pythonの環境の切り分けにvirtualenvを使う．
# pythonやpipもvenvの中のものを使う．
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTHONPATH := ./src

# Dockerイメージの名前・バージョン・タグなどの情報
DOCKER_IMAGE_NAME = dummy-api
DOCKER_IMAGE_VERSION = latest 

# GCPプロジェクトIDやCloud Buildのハッシュなどの情報
# 親Makefileからの引継ぎなのでビルド内では共通 
DOCKER_REGISTRY = gcr.io
DOCKER_USERNAME = $(PROJECT_ID)
DOCKER_IMAGE_SHORT_SHA = $(SHORT_SHA)  

DOCKER_IMAGE = $(DOCKER_REGISTRY)/$(DOCKER_USERNAME)/$(DOCKER_IMAGE_NAME)


# pytestによる単体テスト
check: $(VENV)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest


# dockerイメージのビルド（checkを通過するのが必須）
build: 
	docker build \
			-t $(DOCKER_IMAGE):$(DOCKER_IMAGE_VERSION) \
			-t $(DOCKER_IMAGE):$(DOCKER_IMAGE_SHORT_SHA) .

push: build
	docker push $(DOCKER_IMAGE) 


# virtualenv環境の削除
IMAGES = $(shell docker images | awk '{if($$1=="$(DOCKER_IMAGE)"){print $$3}}')
clean:
ifneq (,$(IMAGES))
	docker rmi -f $(IMAGES)
endif
	if [ -d $(VENV) ]; then \
		rm -rf ./venv; \
	fi


# venv
$(VENV): $(VENV)/touchfile


# venv内にtouchfileというからファイルを作る．
# requirements.txtが更新されたらtouchfileよりも新しくなるので
# venv自体が更新される．
$(VENV)/touchfile: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	touch venv/touchfile

.PHONY: check build push clean $(VENV)
