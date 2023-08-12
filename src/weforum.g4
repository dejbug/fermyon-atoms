grammar weforum;

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

start  : article+ ;
article : Topic? Author* Article
	(Description | PublishedAt | TopicRef | AuthorsRef )* ;
