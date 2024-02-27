all: antlr-regen test

.PHONY: antlr
antlr:
	cd grammars && java -jar ../src/antlr_files/antlr-4.13.1-complete.jar -o ../src/antlr_files -Dlanguage=Python3 -visitor -no-listener C_Grammar.g4

.PHONY: antlr-cleanup
antlr-cleanup:
	rm -rf src/antlr_files/*.py src/antlr_files/*.tokens src/antlr_files/*.interp

.PHONY: antlr-regen
antlr-regen: antlr-cleanup antlr

.PHONY: test
test:
	python3 -m pytest