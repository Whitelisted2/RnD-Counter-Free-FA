compiler:
	bison -d regexParser.y
	flex regexLexer.l
	gcc lex.yy.c regexParser.tab.c main.c -o $@
clean:
	rm -f lex.yy.c regexParser.tab.c regexParser.tab.h compiler