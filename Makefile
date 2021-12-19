PROJECT="message_generator"
DEPLOY="deploy"
TEST_PARAMS="-v"
GUI_PARAM="--gui"
GUI_VAL="tk"

.PHONY: clean test dist

all:
	echo "All"
run:
	python -m ${PROJECT}.main ${RUNTIME_GUI} ${GUI_PARAM} ${GUI_VAL}
clean:
	[ -d ${DEPLOY}/build ]      && rm ${DEPLOY}/build -r
	[ -d ${DEPLOY}/dist ]       && rm ${DEPLOY}/dist -r
	[ -d ${DEPLOY}/${PROJECT} ] && rm ${DEPLOY}/${PROJECT} -r
test:
	python -m test.test_core.py ${TEST_PARAMS}
dist:
	cd ${DEPLOY} && python setup.py bdist
makedoc:
	sphinx-build -b html doc/sphinx
setup:
	pip install -r requirements.txt
