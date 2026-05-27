.PHONY: install test test-fast lint run clean

install:
	pip install -r requirements.txt

test:
	pytest -v

test-fast:
	pytest -v -m "not integration"

run:
	streamlit run src/ui/streamlit_app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	rm -rf logs/*.log