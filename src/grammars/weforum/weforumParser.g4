// https://github.com/antlr/antlr4/blob/master/doc/tool-options.md
// https://github.com/antlr/antlr4/blob/master/doc/python-target.md
// https://github.com/jszheng/py3antlr4book
// https://github.com/antlr/antlr4/blob/master/doc/index.md

// https://github.com/jszheng/py3antlr4book/blob/master/12-sea_of_text/ModeTagsLexer.g4

parser grammar weforumParser;

options { tokenVocab=weforumLexer; } // use tokens from weforum-lexer.g4

// r  : TYPENAME AUTHOR+ TITLE LINK;
// r  : TYPENAME {print("TYPENAME: " + $TYPENAME.text )} ;

/*
r  : article+ .*? ;
article : .*? item ;
item : String Colon String ;
*/

r  : article+ ;
article : Topic? Author+ Article TopicRef? AuthorsRef? ;
