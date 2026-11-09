NAME = pac-man.py
RUN  = uv run

all: run

install:
	uv sync

run:
	$(RUN) $(NAME) config.json

debug:
	$(RUN) -m pdb $(NAME) config.json

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__ .mypy_cache dist build .ruff_cache

lint:
	$(RUN) flake8 . --exclude .venv
	$(RUN) mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

format:
	$(RUN) ruff format .

package:
	$(RUN) pyinstaller pac-man.spec --noconfirm
	$(RUN) python -m zipfile -c dist/pac-man-linux.zip dist/pac-man

.PHONY: install run debug clean lint format
