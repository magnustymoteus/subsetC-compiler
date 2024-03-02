grammar C_Grammar;

/*
    expr: expression
    spec: specifier
    def: definition
    qual: qualifier
*/
// Parser rules

program: functionDef EOF;

functionDef: declarationSpec identifier LPAREN (parameterList)? RPAREN compoundStmt;
typeSpec: 'char' | 'int' | 'float';
typeQual: 'const';

declarationSpec: typeQual? typeSpec pointer*;
declaration: declarationSpec declarator ';'; //(',' declarator)*;
declarator: identifier LPAREN (parameterList)? RPAREN | identifier | identifier EQ assignmentExpr;

pointer: ARISK typeQual*;
initializer: assignmentExpr;

parameterList: parameterDeclaration | parameterList ',' parameterDeclaration;
parameterDeclaration: declarationSpec declarator?;

stmt: exprStmt | compoundStmt;
compoundStmt: LBRACE blockItem* RBRACE;
blockItem: declaration | stmt;
exprStmt: expr ';';
expr: constantExpr | assignmentExpr | expr ',' assignmentExpr;

assignmentExpr: conditionalExpr | unaryExpr assignmentOp assignmentExpr;
assignmentOp: EQ | '*=' | '/=' | '%=' | '+=' | '-=' | '>>=' | '<<=' | '&=' | '^=' | '|=';

constantExpr: conditionalExpr;
conditionalExpr: logicalOrExpr;
logicalOrExpr: logicalAndExpr | logicalOrExpr OR logicalAndExpr;
logicalAndExpr: bitwiseOrExpr | logicalAndExpr AND bitwiseOrExpr;
bitwiseOrExpr: logicalXorExpr | bitwiseOrExpr BITOR logicalXorExpr;
logicalXorExpr: bitwiseAndExpr | logicalXorExpr BITXOR bitwiseAndExpr;
bitwiseAndExpr: equalityExpr | bitwiseAndExpr AMP equalityExpr;
equalityExpr: relationalExpr | equalityExpr (ISEQ | ISNEQ) relationalExpr;
relationalExpr: shiftExpr | relationalExpr (GT | LT | GTEQ | LTEQ) shiftExpr;

shiftExpr: addExpr | shiftExpr (SL | SR) addExpr;
addExpr: multExpr | addExpr (PLUS | MINUS) multExpr;
multExpr: castExpr | multExpr (ARISK | DIV | MOD) castExpr;
castExpr: unaryExpr | LPAREN typeSpec RPAREN castExpr;
unaryExpr: postfixExpr | unaryOp castExpr;
postfixExpr: primaryExpr | postfixExpr (DOT | ARROW) identifier | postfixExpr postfixOp;
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

ID: [a-zA-Z_] [a-zA-Z_0-9]*;

INT: '0' | [1-9][0-9]*;
FLOAT: INT* '.' [0-9]*;
CHAR: '\'' . '\'' | '\'' '\\' ([abefnrtv0]|'\\'|'\''|'"'|'?') '\'';

// the space in [] is important
WS: [ \t\r\n]+ -> skip;
BLOCKCMT: '/*' .*? '*/' -> skip;
LINECMT: '//' ~[\r\n]* -> skip;
