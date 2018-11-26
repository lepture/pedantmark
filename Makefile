.PHONY: clean-pyc clean-build docs

clean: clean-build clean-pyc clean-docs


clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info
	@rm -f mistune.c
	@rm -fr cover/


clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-docs:
	@rm -fr  docs/_build

docs:
	@$(MAKE) -C docs html

.PHONY: build
