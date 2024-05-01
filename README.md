## Execution
1. execute `pip install -r src/requirements.txt`
2. execute `make antlr`, this generates antlr files for the C grammar but also preprocessor
3. execute ie.`python3 -m src --targets llvm --path test.c --viz all --disable comments`
## Optional Features
* Project 2
  * const casting
* Project 4
  * else if
* Project 5
  * include guards
  * Do not generate code for conditionals that are never true.
  * Do not generate code for variables that are not used.
* Project 7
  * Structs that contain other structs as a value.
* Extra Warnings