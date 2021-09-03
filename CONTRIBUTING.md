# Notes For Developers

## Developing

Clone the repository and install `podcastista` and its dependencies:

```
git clone https://github.com/andrsd/podcastista.git
cd podcastista
pip install -e .
```

Install additional development requirements:

```
pip install -r requirements/devel.txt
```

Setup connection to spotify:

```
TODO
```

Run unit tests with:

```
pytest .
```

Run code checks with:

```
flake8 .
```

Run unit tests with coverage report:

```
coverage run --source=podcastista -m pytest
coverage html
```

Open `htmlcov/index.html`

## Building the app

```
pyinstaller Podcastista.spec
```

This will create a distributable in `dist` directory.
