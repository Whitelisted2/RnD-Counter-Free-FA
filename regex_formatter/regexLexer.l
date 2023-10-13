%{
#include "regexParser.tab.h"
#include<string.h>
%}
%%

[a-z]+ {
    yylval.str = strdup(yytext);
    return IDENTIFIER;}

\* {return STAR;}

\< {return LESSTHAN;}

> {return GREATERTHAN;}

\( {return OPENBRACKET;}

\) {return CLOSEDBRACKET;}

\| {return OR;}

[ \t\n] ;

%%
int yywrap()
{
    return 1;
}