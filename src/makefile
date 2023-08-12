# NOTE TO SELF: Remember that I'm using my custom patched version of e.g. pygrun!
#	... So it is not available on the cloud's build servers.

ANTLR=antlr4
PYGRUN=pygrun
GAWK=gawk


DIR_TEMP=.temp
DIR_GRAMMAR=grammars
DIR_GRAMMAR_WEFORUM=$(DIR_GRAMMAR)/weforum

GRAMMARS := weforum # aldaily ibtimes

WEFORUM_PARSER_FILES = $(call deriveParserFiles,weforum)


# Library

define deriveParserFiles
grammars/$1/$1Lexer.py grammars/$1/$1Listener.py grammars/$1/$1Parser.py
endef

define createPygrunOutputFile
$(eval TARGET = $(notdir $1))
$(eval NAME = $(basename $(TARGET)))
cd grammars/$(NAME) && $(PYGRUN) -e utf8 $(NAME) start --tokens ../../.cache/$(NAME).text > ../../$(DIR_TEMP)/$(TARGET)
endef

define cleanUnnecessaryGrammarFiles
rm -f grammars/**/*.tokens
rm -f grammars/**/*.interp
endef

define grammarNameFromTestRule
$(word 2,$(subst _, ,$(filter test_%_sed test_%_gawk,$1)))
endef

define makeGrammarRuleFromTestFunction
$(eval NAME = $(call grammarNameFromTestRule,$1))
.PHONY : $1
$1 : $(DIR_TEMP)/$(NAME).out ; $(call $1,$(DIR_TEMP)/$(NAME).out)
endef


.PHONY : all clean reset

all : test_weforum_sed

clean :
	rm -f $(DIR_TEMP)/weforum.out

reset : | clean
	rm -rf grammars


$(call deriveParserFiles,weforum) : weforum.g4
	$(ANTLR) -o grammars/$(basename $<) -Dlanguage=Python3 $<
	$(call cleanUnnecessaryGrammarFiles)

$(DIR_TEMP)/weforum.out : $(call deriveParserFiles,weforum)

%.out : ; $(call createPygrunOutputFile,$@)


# Tests

SED_weforum='s/.*"id":"([0-9]+)","*__typename":"([^"]+)"(,"(name|title|url)":"([^"]+)")?(,"(title|url)":"([^"]+)")?.*/  ID | \1\nTYPE | \2\nARG1 | \5\nARG2 | \8\n/p'

define test_weforum_sed
@cat $1 | sed -E $(SED_weforum)
endef

define test_weforum_gawk
@$(GAWK) -f weforum.gawk -- $1
endef


# Tests / Rules Autogen

TEST_FUNCTIONS := $(filter test_%_sed test_%_gawk,$(.VARIABLES))
$(foreach name,$(TEST_FUNCTIONS),$(eval $(call makeGrammarRuleFromTestFunction,$(name))))
