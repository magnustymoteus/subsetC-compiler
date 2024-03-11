grammar C_project3;

/*
    expr: expression
    spec: specifier
    def: definition
    qual: qualifier
*/
// Parser rules

/* TODO:
    - Store comments in AST
    - Add original C code after LLVM instruction in comment
    - Do the same for MIPS
    - Implement something so just the typedef types can be used
*/

program: (comment* (functionDef | declaration | typeDef) comment*)* EOF;

comment: BLOCKCMT | LINECMT;

functionDef: declarationSpec identifier LPAREN (parameterList)? RPAREN compoundStmt; // int func() {...}
typeSpec: 'char' | 'int' | 'float';
typeQual: 'const';

declarationSpec: typeQual? typeSpec pointer*; //e.g const char *
declaration: (declarationSpec | ID) declarator ';'; //e.g const int * num;
declarator: identifier LPAREN (parameterList)? RPAREN | identifier | identifier EQ assignmentExpr;
//e.g func(5,2) | num | num = 5

typeDef: TYPEDEF typeSpec ID ';'; //e.g typedef float speed;

pointer: ARISK typeQual*; // * const
initializer: assignmentExpr;

parameterList: parameterDeclaration | parameterList ',' parameterDeclaration; // e.g int num | int num, char ch,...
parameterDeclaration: declarationSpec declarator?; //e.g int num

printf: PRINTF LPAREN '"' FORMATTING* '",' (ID | literal)* RPAREN ';'; // printf("%d", 5);
stmt: exprStmt | compoundStmt;
compoundStmt: LBRACE blockItem* RBRACE; // {...}
blockItem: (declaration | stmt | printf) comment*; // ... /*...*/
exprStmt: expr ';';
expr: constantExpr | assignmentExpr | expr ',' assignmentExpr; // ... | ... | a = 1, b = 2

assignmentExpr: conditionalExpr | unaryExpr assignmentOp assignmentExpr;
assignmentOp: EQ | '*=' | '/=' | '%=' | '+=' | '-=' | '>>=' | '<<=' | '&=' | '^=' | '|=';

constantExpr: conditionalExpr;
conditionalExpr: logicalOrExpr;
logicalOrExpr: logicalAndExpr | logicalOrExpr OR logicalAndExpr; // ... | (x < y) || (y > z)
logicalAndExpr: bitwiseOrExpr | logicalAndExpr AND bitwiseOrExpr; // ... | (x < y) && (y | z)
bitwiseOrExpr: logicalXorExpr | bitwiseOrExpr BITOR logicalXorExpr; // ... | (x | y) | (x != y)
logicalXorExpr: bitwiseAndExpr | logicalXorExpr BITXOR bitwiseAndExpr; // ... | (x != y) ^ (x & y)
bitwiseAndExpr: equalityExpr | bitwiseAndExpr AMP equalityExpr; // ... | (x & y) & (x == y)
equalityExpr: relationalExpr | equalityExpr (ISEQ | ISNEQ) relationalExpr; // ... | (x == y) == (x < y)
relationalExpr: shiftExpr | relationalExpr (GT | LT | GTEQ | LTEQ) shiftExpr; // ... | (x < y) < (x << y)

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

ID: [a-zA-Z_] [a-zA-Z_0-9]*;

INT: '0' | [1-9][0-9]*;
FLOAT: INT* '.' [0-9]*;
CHAR: '\'' . '\'' | '\'' '\\' ([abefnrtv0]|'\\'|'\''|'"'|'?') '\'';

// the space in [] is important
WS: [ \t\r\n]+ -> skip;

// comments
BLOCKCMT: '/*' .*? '*/';
LINECMT: '//' ~[\r\n]*;