grammar C_Expressions;

// Parser rules
program: statement* EOF;
statement: exprStatement ';' | ';';
exprStatement: expr;
expr: constantExpr;
constantExpr: conditionalExpr;
conditionalExpr: logicalOrExpr;
logicalOrExpr: logicalAndExpr | logicalOrExpr OR logicalAndExpr;
logicalAndExpr: bitwiseOrExpr | logicalAndExpr AND bitwiseOrExpr;
bitwiseOrExpr: logicalXorExpr | bitwiseOrExpr BITOR logicalXorExpr;
logicalXorExpr: bitwiseAndExpr | logicalXorExpr BITXOR bitwiseAndExpr;
bitwiseAndExpr: equalityExpr | bitwiseAndExpr BITAND equalityExpr;
equalityExpr: relationalExpr | equalityExpr (ISEQ | ISNEQ) relationalExpr;
relationalExpr: shiftExpr | relationalExpr (GT | LT | GTEQ | LTEQ) shiftExpr;
shiftExpr: addExpr | shiftExpr (SL | SR) addExpr;
addExpr: multExpr | addExpr (PLUS | MINUS) multExpr;
multExpr: unaryExpr | multExpr (MUL | DIV | MOD) unaryExpr;
unaryExpr: unaryOperator expr | literal | parenExpr;
parenExpr: LPAREN expr RPAREN;
unaryOperator: PLUS | MINUS | NOT | BITNOT;
literal: INT;

// Lexer rules
LPAREN: '(';
RPAREN: ')';

PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';

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
BITAND: '&';
BITOR: '|';
BITNOT: '~';
BITXOR: '^';

SL: '<<';
SR: '>>';

INT: '0' | [1-9][0-9]*;
WS: [\t\r\n]+ -> skip;
