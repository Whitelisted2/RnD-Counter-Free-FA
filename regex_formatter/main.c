#include<stdio.h>
#include "regexParser.tab.h"
extern FILE* yyin;
int yylex();
int yyparse();
int main(int argc, char* argv[]) {
	++argv, --argc;  /* skip over program name */
	if (argc > 0) yyin = fopen( argv[0], "r" );
    else yyin = stdin;
	int state = yyparse();
	fclose(yyin);
	return 0;
}