FRONTEND = frontend
BACKEND = backend
CACHE = cache
CONFIGS = configs
VENV = venv
BUILD = build

all:
	make frontend-build
	make backend-build

frontend-build:
	mkdir $(BUILD) -p
	cd $(FRONTEND) && npm run build
	mv $(FRONTEND)/dist $(BUILD)/

backend-build:
	mkdir $(BUILD)/static_root -p
	sed -i "s/DEBUG = True/DEBUG = False/g" $(BACKEND)/backend/settings.py
	cd $(BACKEND) && python manage.py collectstatic

clean:
	rm -rf build

.PHONY: frontend-build backend clean