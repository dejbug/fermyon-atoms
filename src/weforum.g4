// https://github.com/antlr/antlr4/blob/master/doc/tool-options.md
// https://github.com/antlr/antlr4/blob/master/doc/python-target.md
// https://github.com/jszheng/py3antlr4book
// https://github.com/antlr/antlr4/blob/master/doc/index.md
parser grammar weforum;
options { tokenVocab=weforumLexer; } // use tokens from weforum-lexer.g4
r  : TOPIC ; // AUTHOR+ TITLE LINK;
