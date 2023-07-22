antlr='antlr'

buildParser() {
	# mkdir -p grammars/$1/
	$antlr -o grammars/$1/ -Dlanguage=Python3 weforum.g4
}

unusedGrammarFiles() {
	find grammars/$1/ -maxdepth 1 -type f | grep -vE 'clean\.sh|.*(.g4|(Lexer|Parser|Listener)\.py)'
}

buildParser weforum
rm -f `unusedGrammarFiles weforum`
