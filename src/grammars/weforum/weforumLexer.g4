// https://github.com/antlr/antlr4/blob/master/doc/tool-options.md
// https://github.com/antlr/antlr4/blob/master/doc/python-target.md
// https://github.com/jszheng/py3antlr4book
// https://github.com/antlr/antlr4/blob/master/doc/index.md

// https://github.com/jszheng/py3antlr4book/blob/master/12-sea_of_text/ModeTagsLexer.g4

lexer grammar weforumLexer;

/*
// Topic : '"__typename":"Topic"' ;
// Author : '"__typename":"Author"' ;
// Article : '"__typename":"Article"' ;
// ArticleUrl : '"url":' ;
// ArticleTitle : '"title":' ;

String : '"' .+? '"' ;
Colon : ':' ;
// Comma : ',' ;
// ANY : .+? -> skip ;
*/


/*
fragment VALUE : .+? ;

TOPIC_OPEN : '"__typename":"Topic","title":"' -> mode(TOPIC_MODE) ;
AUTHOR_OPEN : '"__typename":"Author",' -> mode(AUTHOR_MODE) ;
ARTICLE_OPEN : '"__typename":"Article",' -> mode(ARTICLE_MODE) ;
ANY : . -> skip ;

mode TOPIC_MODE ;
TOPIC_MODE_CLOSE : '"' -> mode(DEFAULT_MODE) ;
Topic : ~["]+ ;

mode AUTHOR_MODE ;
Author : '"name":"' VALUE '"' -> mode(DEFAULT_MODE) ;

mode ARTICLE_MODE ;
Article : '"url":"' VALUE '","title":"' VALUE '"' -> mode(DEFAULT_MODE) ;
*/


fragment String : '"' .+? '"' ;

Topic : '"id":"' [0-9]+ '","__typename":"Topic","title":' String ',"url":' String ;
Author : '"id":"' [0-9]+ '","__typename":"Author","name":' String ;
Article : '"id":"' [0-9]+ '","__typename":"Article","url":' String ',"title":' String ;

TopicRef : '"topic":{"__ref":"Topic:' .+? '"' ;
AuthorsRef : '"authors":[' .+? ']' ;

ANY : . -> skip ;
