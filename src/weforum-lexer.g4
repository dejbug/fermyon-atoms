// https://github.com/antlr/antlr4/blob/master/doc/tool-options.md
// https://github.com/antlr/antlr4/blob/master/doc/python-target.md
// https://github.com/jszheng/py3antlr4book
// https://github.com/antlr/antlr4/blob/master/doc/index.md

// https://github.com/jszheng/py3antlr4book/blob/master/12-sea_of_text/ModeTagsLexer.g4

lexer grammar weforumLexer;

TYPENAME : '"__typename":"' -> mode(ISLAND) ;

mode ISLAND ;
CLOSE : '"' -> mode(DEFAULT_MODE) ;
ID : [^"]+ ;
