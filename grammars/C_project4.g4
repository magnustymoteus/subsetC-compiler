grammar C_project4;

/*
    expr: expression
    spec: specifier
    def: definition
    qual: qualifier
    stmt: statement
*/
// Parser rules

/* TODO:
    - Store comments in AST
    - Add original C code after LLVM instruction in comment
    - Do the same for MIPS
    - Implement something so just the typedef types can be used
*/

program: (comment* (functionDef | declaration | typeDef | enumSpec) comment*)* EOF;

comment: BLOCKCMT | LINECMT;

functionDef: declarationSpec identifier LPAREN (parameterList)? RPAREN compoundStmt; // int func() {...}
typeSpec: 'char' | 'int' | 'float';
typeQual: 'const';

declarationSpec: typeQual? typeSpec pointer*; //e.g const char *
declaration: ((declarationSpec | ID) declarator | enumDecl) ';'; //e.g const int * num;
declarator: identifier LPAREN (parameterList)? RPAREN | identifier | identifier EQ assignmentExpr;
//e.g func(5,2) | num | num = 5

enumSpec: ENUM identifier? LBRACE enumList RBRACE identifier? ';' ; // enum enumName { enumList }
enumDecl: ENUM identifier (identifier | identifier EQ assignmentExpr); // enum enumName (id | id = ...) ;
enumList: enumerator | enumList ',' comment* enumerator; // | MONDAY, TUESDAY, ...
enumerator:  (identifier | identifier EQ constantExpr) comment* ; // MONDAY | MONDAY = 1


typeDef: TYPEDEF typeSpec ID ';'; //e.g typedef float speed;

pointer: ARISK typeQual*; // * const
initializer: assignmentExpr;

parameterList: parameterDeclaration | parameterList ',' parameterDeclaration; // e.g int num | int num, char ch,...
parameterDeclaration: declarationSpec declarator?; //e.g int num


//////////////////////////////////////////////
stmt: (exprStmt | compoundStmt | selectionStmt | iterationStmt | jumpStmt | labeledStmt) comment*;

compoundStmt: LBRACE blockItem* RBRACE comment*; // {...} /*...*/
blockItem: comment* (declaration | stmt | printf | enumSpec ) comment*; // ... /*...*/

printf: PRINTF LPAREN '"' FORMATTING* '",' (ID | literal)* RPAREN ';'; // printf("%d", 5);

exprStmt: expr ';';
expr: constantExpr | assignmentExpr | expr ',' assignmentExpr; // ... | ... | a = 1, b = 2
assignmentExpr: conditionalExpr | unaryExpr assignmentOp assignmentExpr;
assignmentOp: EQ | '*=' | '/=' | '%=' | '+=' | '-=' | '>>=' | '<<=' | '&=' | '^=' | '|=';

/// if 'if'-statement without braces is allowed -> change compoundStmt to stmt
selectionStmt: IF LPAREN expr RPAREN compoundStmt (ELSE compoundStmt)? | SWITCH LPAREN expr RPAREN stmt; // if(i=0){} (else {}) |

labeledStmt: (CASE constantExpr ':' stmt | DEFAULT ':' stmt) comment*;

iterationStmt: WHILE LPAREN expr RPAREN compoundStmt | FOR LPAREN expr? ';' expr? ';' expr? RPAREN compoundStmt;

jumpStmt: (CONTINUE | BREAK) ';';

///////////////////////////////////////////////

///////////////////////////////////////////////
constantExpr: conditionalExpr;
conditionalExpr: logicalOrExpr;
logicalOrExpr: logicalAndExpr | logicalOrExpr OR logicalAndExpr; // ... | (x < y) || (y > z)
logicalAndExpr: bitwiseOrExpr | logicalAndExpr AND bitwiseOrExpr; // ... | (x < y) && (y | z)
bitwiseOrExpr: logicalXorExpr | bitwiseOrExpr BITOR logicalXorExpr; // ... | (x | y) | (x != y)
logicalXorExpr: bitwiseAndExpr | logicalXorExpr BITXOR bitwiseAndExpr; // ... | (x != y) ^ (x & y)
bitwiseAndExpr: equalityExpr | bitwiseAndExpr AMP equalityExpr; // ... | (x & y) & (x == y)
equalityExpr: relationalExpr | equalityExpr (ISEQ | ISNEQ) relationalExpr; // ... | (x == y) == (x < y)
relationalExpr: shiftExpr | relationalExpr (GT | LT | GTEQ | LTEQ) shiftExpr; // ... | (x < y) < (x << y)
///////////////////////////////////////////////

shiftExpr: addExpr | shiftExpr (SL | SR) addExpr; // ... | (x << y) << (x + y)
addExpr: multExpr | addExpr (PLUS | MINUS) multExpr; // ... | (x + y) + (x * y)
multExpr: castExpr | multExpr (ARISK | DIV | MOD) castExpr; // ... | (x * y) * (int)(y + z)
castExpr: unaryExpr | LPAREN typeSpec RPAREN castExpr; // ... | (int) x
unaryExpr: postfixExpr | unaryOp castExpr; // ... | -((double)x)
postfixExpr: primaryExpr | postfixExpr (DOT | ARROW) identifier | postfixExpr postfixOp; // ... | person->name | ...
postfixOp: DPLUS | DMINUS;
primaryExpr: identifier | literal | parenExpr;
parenExpr: LPAREN expr RPAREN;
unaryOp: PLUS | MINUS | NOT | BITNOT | DPLUS | DMINUS | AMP | ARISK;

identifier: ID;
literal: intLiteral | charLiteral | floatLiteral;
intLiteral: INT;
charLiteral: CHAR;
floatLiteral: FLOAT;

// Lexer rules
LPAREN: '(';
RPAREN: ')';

LBRACE: '{';
RBRACE: '}';

PLUS: '+';
MINUS: '-';
ARISK: '*';
DIV: '/';
MOD: '%';

DPLUS: '++';
DMINUS: '--';
DOT: '.';
ARROW: '->';

EQ: '=';

GT: '>';
LT: '<';
GTEQ: '>=';
LTEQ: '<=';
ISEQ: '==';
ISNEQ: '!=';

AND: '&&';
OR: '||';
NOT: '!';
AMP: '&';
BITOR: '|';
BITNOT: '~';
BITXOR: '^';

SL: '<<';
SR: '>>';

PRINTF: 'printf';
FORMATTING: '%s' | '%d' | '%x' | '%f' | '%c';

TYPEDEF: 'typedef';

IF: 'if';
ELSE: 'else';

FOR: 'for';
WHILE: 'while';

CONTINUE: 'continue';
BREAK: 'break';
SWITCH: 'switch';
CASE: 'case';
DEFAULT: 'default';

ENUM: 'enum';

ID: [a-zA-Z_] [a-zA-Z_0-9]*;

INT: '0' | [1-9][0-9]*;
FLOAT: INT* '.' [0-9]*;
CHAR: '\'' . '\'' | '\'' '\\' ([abefnrtv0]|'\\'|'\''|'"'|'?') '\'';

// the space in [] is important
WS: [ \t\r\n]+ -> skip;

// comments
BLOCKCMT: '/*' .*? '*/';
LINECMT: '//' ~[\r\n]*;