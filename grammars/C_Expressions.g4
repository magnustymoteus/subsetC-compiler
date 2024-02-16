grammar C_Expressions;

// Parser rules
expr: term (('+' | '-') term)*;
term: factor (('*' | '/') factor)*;
factor: NUMBER | '(' expr ')' | ('-' | '+') factor;

// Lexer rules
NUMBER: [0-9]+ ('.' [0-9]+)?;
INTEGER: []
WS: [ \t\r\n]+ -> skip;