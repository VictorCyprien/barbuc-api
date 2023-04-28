.PHONY: all requirements tests

all: requirements

run:
	export FLASK_APP=run; export FLASK_ENV=development; flask run --host=0.0.0.0 --port=5001;

shell:
	export FLASK_APP=run; export FLASK_ENV=development; flask shell;

build_schemas:
	export FLASK_APP=run; flask openapi write specs/barbuc-spec.json;
	export FLASK_APP=run; flask openapi write specs/barbuc-spec.yaml;

clean:
	@echo
	@echo "---- Clean *.pyc ----"
	@find . -name \*.pyc -delete

clean_pip: clean
	@echo
	@echo "---- Clean packages ----"
	@pip freeze | grep -v "^-e" | cut -d "@" -f1 | xargs pip uninstall -y

cleaninstall: requirements clean_pip
	@echo
	@echo "---- Install packages from requirements.txt ----"
	@pip install -r requirements.txt
	@pip freeze
	@echo "---- Install packages from requirements.dev.txt ----"
	@pip install -r requirements.dev.txt
	@pip freeze
	@echo
	@echo "---- Install packages from setup ----"
	@$(shell echo ${PYTHON_ROCKSDB_FLAGS}) pip install -e ./

install:
	@echo
	@echo "---- Install packages from requirements.txt ----"
	@pip install -r requirements.txt
	@pip freeze
	@echo "---- Install packages from requirements.dev.txt ----"
	@pip install -r requirements.dev.txt
	@pip freeze
	@echo
	@echo "---- Install packages from setup ----"
	@$(shell echo ${PYTHON_ROCKSDB_FLAGS}) pip install -e ./

tests:
	pytest --cov=barbuc_api --cov-config=.coveragerc --cov-report=html:htmlcov --cov-report xml:cov.xml --cov-report=term \
		-vv --doctest-modules --ignore-glob=./main.py --log-level=DEBUG --junitxml=report.xml ./ ./tests


testsx:
	pytest -x -vv --doctest-modules --ignore-glob=./barbuc_api/main.py --log-level=DEBUG ./barbuc_api ./tests


build_docker_image:
	docker build -t barbuc-api . 


build_docker_container:
	docker run -d -p 5000:5000 --env-file .env --name barbuc-api --network barbuc-network barbuc-api
