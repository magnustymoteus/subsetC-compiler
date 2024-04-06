grammar C_project4;

/*
    expr: expression
    spec: specifier
    def: definition
    qual: qualifier
*/
// Parser rules

program: (functionDef | declaration)* EOF;

functionDef: declarationSpec identifier LPAREN (parameterList)? RPAREN compoundStmt;
typeSpec: 'char' | 'int' | 'float' | typedefName | enumSpec;
typeQual: 'const';
storageClassSpec: 'typedef';
declarationSpec: storageClassSpec? typeQual? typeSpec pointer?;
declaration: declarationSpec declarator? SEMICOL; //(',' declarator)*;
declarator: identifier | identifier EQ assignmentExpr | LPAREN parameterList? RPAREN;

enumSpec: 'enum' identifier (LBRACE enum (',' enum)* RBRACE)?;
enum: identifier;

typedefName: identifier;

pointer: (ARISK typeQual?)+;
initializer: assignmentExpr;

parameterList: parameterDeclaration | parameterList ',' parameterDeclaration;
parameterDeclaration: declarationSpec declarator?;

stmt: exprStmt | compoundStmt | printfStmt | iterationStmt | jumpStmt | selectionStmt;

selectionStmt: 'if' LPAREN expr RPAREN compoundStmt ('else' (compoundStmt | selectionStmt))? | 'switch' LPAREN expr RPAREN LBRACE labeledStmt* RBRACE;

iterationStmt: 'while' LPAREN expr RPAREN compoundStmt | 'for' LPAREN forCondition RPAREN compoundStmt;
forCondition: (forDeclaration | expr?) SEMICOL expr? SEMICOL expr?;
forDeclaration: declarationSpec declarator?;

labeledStmt: 'case' constantExpr COL blockItem* | 'default' COL blockItem*;

jumpStmt: 'continue' SEMICOL | 'break' SEMICOL;

// temporary, remove when introducing function calls (?)
printfStmt: 'printf' LPAREN '"' printfFormat '"' ',' (identifier | literal) RPAREN SEMICOL;
printfFormat: PRINTF_FORMATTING;
//

compoundStmt: LBRACE blockItem* RBRACE;
blockItem: declaration | stmt;
exprStmt: expr? SEMICOL;
expr: assignmentExpr | expr ',' assignmentExpr;

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
primaryExpr: identifier | literal | LPAREN expr RPAREN;
unaryOp: PLUS | MINUS | NOT | BITNOT | DPLUS | DMINUS | AMP | ARISK;

identifier: ID;
literal: intLiteral | charLiteral | floatLiteral;
intLiteral: INT;
charLiteral: CHAR;
floatLiteral: FLOAT;

// Lexer rules
SEMICOL: ';';
COL: ':';

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
WS: [ \t\r\n]+ -> channel(HIDDEN);

BLOCKCMT: '/*' .*? '*/' -> channel(HIDDEN);
LINECMT: '//' ~[\r\n]* -> channel(HIDDEN);

PRINTF_FORMATTING: '%' [sdxfc];