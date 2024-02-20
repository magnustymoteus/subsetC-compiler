grammar C_Expressions;

// Parser rules
statement: exprStatement ';' | statement exprStatement ';' | ';';
exprStatement: expr;
expr: constantExpr | constant;
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
unaryExpr: unaryOperator expr | LPAREN expr RPAREN | constant;
unaryOperator: PLUS | MINUS | NOT | BITNOT;
constant: INT;

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

INT: [0-9]+;
WS: [ \t\r\n]+ -> skip;