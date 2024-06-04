# Compiler Project
* [LLVM IR 1-7 Video](https://youtu.be/pVn3mJ-2uyw)
* [MIPS Video](https://youtu.be/FEFQrp8MiuE)
## Authors
* Patryk Pilichowski
* Valérie Jacobs
* Hendrik De Bruyn
## Execution
1. execute `pip install -r src/requirements.txt`
2. execute `make antlr`, this generates antlr files for the C grammar but also preprocessor
3. make your .c file you want to compile, i.e `test.c`
4. execute ie.`python3 -m src --targets llvm --path test.c --viz all --disable comments`
   * Compile test.c to LLVM IR
   * Generate visualization for everything (CST, AST, CFG, symbol tables)
   * disable comments in output (which happens by default)
* To see all possible flags, run `python3 -m src`
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

## Test Outputs
* Output of the compilable tests can be located in `src/tests`, which includes the llvm output and the visualization of CST, AST, symbol tables, CFG.
* The visualizations are both in `.png` and `.gv` formats. (LLVM CFG is only in `.gv`).
* Note: for some LLVM outputs there may be variables that do not show up, that is because some of the tests contain dead code (and the DeadCodeVisitor removes them as instructed in the assignments).
