SOURCE_PATH = ideation_cli

install:
	@poetry install

cli:
	@poetry run python -m ideation_cli.cli

black:
	@echo "Formatting with black..."
	@poetry run black .

# Check-in code after formatting
checkin: black ## Perform a check-in after formatting the code
    ifndef COMMIT_MESSAGE
		$(eval COMMIT_MESSAGE := $(shell bash -c 'read -e -p "Commit message: " var; echo $$var'))
    endif
	@git add --all; \
	  git commit -m "$(COMMIT_MESSAGE)"; \
	  git push

# Check code formatting using Black
check-black: ## Check code formatting with Black
	@echo "Checking code formatting with Black..."
	@poetry run black --check .

# Source directories for tests
TESTS_SOURCE:=tests/

# Detailed pytest target with coverage and cache clear
test: ## Run pytest with coverage and clear cache
	@echo "Running pytest with coverage and cache clear..."
	@PYTHONPATH=src/ poetry run pytest \
		--cache-clear \
		--cov=. \
		$(TESTS_SOURCE) \
		--cov-report=term \
		--cov-report=html

PYLINT_OPTIONS ?=
# --disable=all --enable=missing-function-docstring
# Runs pylint checks
pylint:  ## Runs pylint
	@echo "Running pylint checks..."
	@PYTHONPATH=$(SOURCE_PATH) poetry run pylint $(PYLINT_OPTIONS)  $(SOURCE_PATH)

aquatic_games:
	@echo "Creating aquatic games..."
	@ideation-cli --theme "Create concept for a Game Jam, with the theme 'Fish' and Ethics and sustainability."  \
		--ideation-technique oblique_strategy \
		--image \
		--game-type "Space Invaders" \
		--count 1 \
		--randomize \
		--path ideas/aquatic \
		--temperature 1.2

aquatic_pause_menu:
	@echo "Creating pause menu..."
	@ideation-cli \
		--image \
		--game-type "Ridiculous Fishing" \
		--name "Pause Menu" \
		--task "A whirlpool in the ocean, devouring ships" \
		--count 5 \
		--path ideas/aquatic

rpg_games:
	@echo "Creating RPG games..."
	@ideation-cli --theme "$$(cat prompts/rpg_game_jam_2025.md)"  \
		--ideation-technique oblique_strategy \
		--image \
		--game-type "RPG" \
		--count 5 \
		--randomize \
		--path ideas/rpggamejam \
		--temperature 1.2
