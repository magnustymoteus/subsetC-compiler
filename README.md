## Execution
1. execute `pip install -r src/requirements.txt`
2. execute `make antlr`, this generates antlr files for the C grammar but also preprocessor
3. execute ie.`python3 -m src --targets llvm --path test.c --viz all --disable comments`
   * Compile test.c to LLVM IR
   * Generate visualization for everything (CST, AST, CFG, symbol tables)
   * disable comments in output (which happens by default)
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
  * Unions.
* Extra visualizations
  * CFG
  * LLVM CFG for each function
  * CST
* Extra Warnings
  * Warning when a condition is never true
  * Warning when there are too many initialized elements in an array
  * Warning when a pointer discards const qualifier
* Detailed warnings & errors
  * format: [filename]:[line]:[column]:[preprocessing_error | syntax_error | semantic_error | semantic_warning]: [message]