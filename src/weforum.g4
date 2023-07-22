grammar weforum;

fragment String : '"' .+? '"' ;

Topic : '"id":"' [0-9]+ '","__typename":"Topic","title":' String ',"url":' String ;
Author : '"id":"' [0-9]+ '","__typename":"Author","name":' String ;
Article : '"id":"' [0-9]+ '","__typename":"Article","url":' String ',"title":' String ;

TopicRef : '"topic":{"__ref":"Topic:' .+? '"' ;
AuthorsRef : '"authors":[' .+? ']' ;

ANY : . -> skip ;

start  : article+ ;
article : Topic? Author* Article TopicRef? AuthorsRef? ;
