ENV_FILE=.env
NEW_DIR=alembic\versions

ENV_VARS=\
    APP_CONFIG__DB__URL=postgresql+asyncpg://postgres:postgres@localhost:5432/frame\
    \
    APP_CONFIG__DB__ECHO=0\
    \
    APP_CONFIG__TEST_DB__URL=postgresql+asyncpg://postgres:postgres@localhost:5432/test_frame\
    \
    APP_CONFIG__TEST_DB__ECHO=0\


ifeq ($(OS),Windows_NT)
  ACTIVATOR = .venv\Scripts\activate
else
  ACTIVATOR = .venv/bin/activate
endif

all: setup

setup:
	@echo "Making virtual environment .venv..."
	python -m venv .venv
	@echo "Activating .venv and installing Poetry..."
	 $(ACTIVATOR) && \
	pip install poetry && \
	poetry install
	@echo "Making .env file..."
	echo $(ENV_VARS) > $(ENV_FILE)
	@echo "Making alembic/versions directory..."
	mkdir $(NEW_DIR)
	@echo "Process completed!"
