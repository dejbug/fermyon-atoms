RELEASE ?=
SQUEEZE ?=

ParserNames ?= aldaily digidem ibtimes linkedin weforum

TempDir=.temp
GrammarsDir=grammars

ANTLR=antlr4
PYGRUN=pygrun
GAWK=gawk

GrammarSources := $(wildcard *.g4)
GrammarNames := $(GrammarSources:%.g4=%)
ParserSources := $(foreach name,$(GrammarNames),$(call deriveParserFiles,$(name)))
