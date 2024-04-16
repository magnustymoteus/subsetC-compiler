grammar C_Preprocessor;


// Directives
DEFINE       : '#' 'define';
INCLUDE      : '#' 'include';
IFNDEF       : '#' 'ifndef';
ENDIF        : '#' 'endif';

IDENTIFIER   : [a-zA-Z_] [a-zA-Z_0-9]*;
STRING       : '"' ~["\r\n]* '"';
HEADER       : '<' ~["\r\n]* '>';

LINECMT      : '//' ~[\r\n]* -> channel(HIDDEN);
BLOCKCMT: '/*' .*? '*/' -> channel(HIDDEN);
WS           : [ \t]+ -> channel(HIDDEN);
ANY: ~'\n';

// Parser rules
program : (line '\n'*)* EOF;
line: (directive | textLine);
directive : (defineDirective
          | includeDirective
          | ifndefDirective
          | endifDirective);

defineDirective : DEFINE IDENTIFIER definedSubject;
definedSubject: ~'\n'*;

includeDirective  : INCLUDE (STRING | HEADER);

ifndefDirective  : IFNDEF IDENTIFIER;

endifDirective   : ENDIF;

textLine : ~'\n'+?;
