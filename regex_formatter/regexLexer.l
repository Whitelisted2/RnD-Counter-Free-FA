%{
#include "regexParser.tab.h"
#include<string.h>
%}
%%

p[0-9]+: {return DEFTOKEN;}

spec:(.*) {return RUNTIMEEQ;}

ugly_RE: {return UGLYTOKEN;}

bad_RE: {return BADTOKEN;}

good_RE: {return GOODTOKEN;}

[a-z]+ {
    yylval.str = strdup(yytext);
    return IDENTIFIER;}

\* {return STAR;}

\< {return LESSTHAN;}

> {return GREATERTHAN;}

\( {return OPENBRACKET;}

\) {return CLOSEDBRACKET;}

\| {return OR;}

[ \t] ;

\n {return NEWLINE;}

%%
int yywrap()
{
    return 1;
}