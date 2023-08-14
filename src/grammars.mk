# include config.mk

.PHONY : grammars

grammars : $(ParserSources)

include library.mk

$(foreach name,$(GrammarNames),$(eval $(call writeGrammarTarget,$(name))))
