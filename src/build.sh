antlr='antlr'

buildParser() {
	$antlr -o build/$1/ -Dlanguage=Python3 weforum.g4
}

unusedGrammarFiles() {
	find build/$1/ -maxdepth 1 -type f | grep -vE 'clean\.sh|.*(.g4|(Lexer|Parser|Listener)\.py)'
}

main() {
	echo mkdir -p build/weforum/

	# $antlr -o build/weforum/ -Dlanguage=Python3 weforum.g4
	echo "hi"
}


buildParser weforum
rm -f `unusedGrammarFiles weforum`

