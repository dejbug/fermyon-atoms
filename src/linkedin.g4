grammar linkedin;

// Start : '<div' .*? '>' ;
Start : '<div class="mb-1.5 flex flex-row">' ;
Stop : '<div class="content-hub-tagged-topics' ;

// Img : '<img ' .*? 'data-delayed-url="'' .+? "' .*? '>' ;
Img : '<img' .*? '>' ;
Title : '<h2' .*? '</h2>' ;
Text : '<p class="content-description' .*? '</p>' ;

ANY : . -> skip ;

/*
fragment String : '"' .+? '"' ;
fragment Integer : [0-9]+ ;
fragment Date : [0-9]+ '-' [0-9]+ '-' [0-9]+ 'T' [0-9]+ ':' [0-9]+ ':' [0-9]+ 'Z' ;

Topic : '"id":"' Integer '","__typename":"Topic","title":' String ',"url":' String ;
Author : '"id":"' Integer '","__typename":"Author","name":' String ;
Article : '"id":"' Integer '","__typename":"Article","url":' String ',"title":' String ;

TopicRef : '"topic":{"__ref":"Topic:' .+? '"' ;
AuthorsRef : '"authors":[' .+? ']' ;

Description : '"description":' String ;
PublishedAt : '"publishedAt":"' Date '"' ;

ANY : . -> skip ;

start  : Description* article+ ;
article : Topic? Author* Article
	(Description | PublishedAt | TopicRef | AuthorsRef )* ;
*/

start : (ANY* article)* ;
article : Start Img Title Text Stop ;
