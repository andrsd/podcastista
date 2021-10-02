all:
	@echo ""

create-venv:
	@python -m venv venv

syntax-check:
	@flake8 podcastista tests setup.py

test:
	@pytest .

coverage:
	@coverage run --source=podcastista -m pytest
	@coverage html

icon.icns:
	@mkdir -p icon.iconset
	@sips -z 512 512 podcastista/assets/icons/podcastista.png --out icon.iconset/icon_512x512.png
	@iconutil -c icns icon.iconset
	@rm -rf icon.iconset
