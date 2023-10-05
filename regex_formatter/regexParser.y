%{
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
int yylex();
int yyerror(char* msg);
int charcount=0;
char tr[4];
int ind;
%}

%union{
	char *str;
}

%token <str> IDENTIFIER
%token DEFTOKEN RUNTIMEEQ UGLYTOKEN BADTOKEN GOODTOKEN STAR LESSTHAN GREATERTHAN OPENBRACKET CLOSEDBRACKET OR NEWLINE
%type <str> regex regterm base factor

%start program

%%

//Program
program: term program_tail

program_tail: newline_tail term program_tail | newline_tail

term: DEFTOKEN RUNTIMEEQ NEWLINE DEFTOKEN UGLYTOKEN equation NEWLINE DEFTOKEN BADTOKEN equation NEWLINE DEFTOKEN GOODTOKEN equation NEWLINE

newline_tail: NEWLINE newline_tail | %empty

equation: regex {
	for(int i=0;i<strlen($1);i++)
	{
		if($1[i]=='#') printf("%d",charcount);
		else printf("%c",$1[i]);
	}
	printf(";\n");
	free($1);
	charcount=0;
} | %empty

//regex: LESSTHAN IDENTIFIER GREATERTHAN | OPENBRACKET regex CLOSEDBRACKET | regex OR regex | regex regex | regex STAR

regex: regex OR regterm {
	//$$= RatExpOnnLetters(#,"union",[$1,$3])
	$$=malloc((strlen($1)+strlen($3)+32)*sizeof(char));
	strcpy($$,"RatExpOnnLetters(#,\"union\",[\0");
	strcat($$,$1);
	strcat($$,",\0");
	strcat($$,$3);
	strcat($$,"])\0");
	free($1);
	free($3);
} | regterm {
	$$=$1;
}

regterm: regterm factor {
	$$=malloc((strlen($1)+strlen($2)+34)*sizeof(char));
	strcpy($$,"RatExpOnnLetters(#,\"product\",[\0");
	strcat($$,$1);
	strcat($$,",\0");
	strcat($$,$2);
	strcat($$,"])\0");
	free($1);
	free($2);
} | factor {
	$$=$1;
}

factor: base STAR {
	$$=malloc((strlen($1)+28)*sizeof(char));
	strcpy($$,"RatExpOnnLetters(#,\"star\",\0");
	strcat($$,$1);
	strcat($$,")\0");
	free($1);
} | base {
	$$=$1;
}

base: OPENBRACKET regex CLOSEDBRACKET {
	$$=$2;
} | LESSTHAN IDENTIFIER GREATERTHAN {
	ind=0;
	for(int i=0;i<strlen($2);i++)
	{
		ind=ind*26+($2[i]-96);
	}
	if(ind>charcount) charcount=ind;
	$$=malloc(29*sizeof(char));
	strcpy($$,"RatExpOnnLetters(#,[],[\0");
	sprintf(tr,"%d",ind);
	strcat($$,tr);
	strcat($$,"])\0");
}

%%


int yyerror(char* msg){
	printf("Not accepted\n");
}
