PROJECT="sockgen"

# Directories
DIST_DIR="dist"
BUILD_DIR="build"
TEST_DIR="__test__"
DEPLOY="deploy"
REQ="requirements"

# Runtime Parameters
GUI_PARAM="--gui"
GUI_VAL="tk"

# Test Parameter
TEST_PARAMS="-v"

# Applications
PY="python3"
PIP="pip3"
SPHINX="sphinx-build"

# Parameters
LINT_IGNORE="E501,W293"

.PHONY: clean test dist

all: build

clean:
	rm -rf ${PROJECT}/__pycache__
	rm -rf ${TEST_DIR}/__pycache__
	rm -rf ${DIST_DIR}
	rm -rf ${BUILD_DIR}
	rm -rf *.pyc
	rm -rf *.egg
	rm -rf *.egg-info

install:
	${PIP} install -r "${REQ}/dev.txt"
	${PIP} install -r "${REQ}/prod.txt"

run:
	${PY} -m ${PROJECT}.main ${RUNTIME_GUI} ${GUI_PARAM} ${GUI_VAL}

lint:
	${PY} -m flake8 --ignore ${LINT_IGNORE} ${PROJECT}

test:
	${PY} -m unittest ${TEST_DIR}/main_test.py -v

build:
	${PY} setup.py sdist bdist_wheel

publish:
	${PY} -m twine upload dist/*

publish_test:
	${PY} -m twine check dist/* && ${PY} -m twine upload --repository testpypi dist/*

doc:
	${SPHINX} -b html doc/sphinx
