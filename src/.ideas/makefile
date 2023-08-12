# NOTE TO SELF: Remember that I'm using my custom patched version of e.g. pygrun!
#	... So it is not available on the cloud's build servers.

ANTLR=antlr4
PYGRUN=pygrun -e utf8 weforum start --tokens ../../.cache/weforum.text
SED='s/.*"id":"([0-9]+)","*__typename":"([^"]+)"(,"(name|title|url)":"([^"]+)")?(,"(title|url)":"([^"]+)")?.*/  ID | \1\nTYPE | \2\nARG1 | \5\nARG2 | \8\n/p'

DIR_TEMP=.temp
DIR_GRAMMAR=grammars
DIR_GRAMMAR_WEFORUM=$(DIR_GRAMMAR)/weforum

.PHONY : all build clean
.PHONY : test_grammar_weforum_raw  test_grammar_weforum_sed  test_grammar_weforum_gawk
.PHONY : weforum_test  grammar_weforum  dir_grammar_weforum

define cleanUnnecessaryGrammarFiles
rm -f grammars/**/*.tokens
rm -f grammars/**/*.interp
endef

GRAMMARS := grammars/weforum weforum.g4 # grammars/aldaily aldaily.g4

define getGrammarArgs
$(eval ARG1 = $(shell echo $1*2-1 | bc))
$(eval ARG2 = $(shell echo $1*2 | bc))
$(wordlist $(ARG1),$(ARG2),$(GRAMMARS))
endef

define buildPythonGrammar
$(ANTLR) -o $1 -Dlanguage=Python3 $2
endef

define buildPythonGrammarByIndex
$(eval ARGS = $$(call getGrammarArgs,$1))
$(call buildPythonGrammar, $(word 1,$(ARGS)), $(word 2,$(ARGS)) )
endef

define buildPythonGrammarByIndex2
$(let arg1 arg2,$(call getGrammarArgs,$1),\
	$(call buildPythonGrammar,$(arg1),$(arg2)))
endef

ifeq (grammar,$(filter grammar,$(MAKECMDGOALS)))

	ifeq (weforum,$(filter weforum,$(MAKECMDGOALS)))

	define BUILD_GRAMMARS
	@echo 'building weforum'
	endef

	# else ifeq (aldaily,$(filter aldaily,$(MAKECMDGOALS)))

	# define BUILD_GRAMMARS
	# endef

	# else ifeq (ibtimes,$(filter ibtimes,$(MAKECMDGOALS)))

	# define BUILD_GRAMMARS
	# endef

	else

	$(error Which Grammar to build? [weforum, ...])

	endif

endif

# WEFORUM_PARSER_FILES := $(addprefix grammars/weforum/, weforumLexer.py weforumListener.py weforumParser.py)
WEFORUM_PARSER_FILES := \
	grammars/weforum/weforumLexer.py \
	grammars/weforum/weforumListener.py \
	grammars/weforum/weforumParser.py

# all : $(WEFORUM_PARSER_FILES)
all :
# 	@echo $(let arg1 arg2,$(call getGrammarArgs,1),$(arg1) $(arg2))
# 	@echo $(let arg1 arg2,$(call getGrammarArgs,2),$(arg1) $(arg2))
	$(call buildPythonGrammarByIndex,1)

$(WEFORUM_PARSER_FILES) : | grammar_weforum


grammar_weforum : weforum.g4 | dir_grammar_weforum
	$(call buildPythonGrammar, $(DIR_GRAMMAR_WEFORUM), weforum.g4)




clean : ; $(call cleanUnnecessaryGrammarFiles)






dir_grammar_weforum : ; @mkdir -p $(DIR_GRAMMAR_WEFORUM)




build : grammar_weforum

weforum_test : $(WEFORUM_PARSER_FILES)

build_grammar_weforums : | dir_grammar_weforum grammar_weforum

grammar : ; $(call BUILD_GRAMMARS)

test_grammar_weforum_raw :
	@cd $(DIR_GRAMMAR_WEFORUM) && $(PYGRUN)

test_grammar_weforum_sed :
	@cd $(DIR_GRAMMAR_WEFORUM) && $(PYGRUN) | sed -E $(SED)

test_grammar_weforum_gawk :
	@cd $(DIR_GRAMMAR_WEFORUM) && $(PYGRUN) > pygrun.out && gawk -f ../../weforum.gawk pygrun.out

md_temp : ; @mkdir -p $(DIR_TEMP)

$(DIR_TEMP)/weforum.out : | md_temp build_grammar_weforum
	@cd $(DIR_GRAMMAR_WEFORUM) && $(PYGRUN) > /tmp/$(notdir $@)
	@cp /tmp/$(notdir $@) $@



GRAMMARS = weforum aldaily ibtimes
PARSER_FILES = $(foreach grammar, $(GRAMMARS), $(call deriveParserFiles,$(grammar)))


# define setGrammarVars
# $(info $1: creating vars and targets)
# $(eval $1_PARSER_FILES = $$(call deriveParserFiles,$1))
# endef
# $(foreach grammar,$(GRAMMARS),$(eval $(call setGrammarVars,$(grammar))))

GRAMMAR ?=

blah :
	@echo $(test)
ifeq (,$(filter $(GRAMMARS), $(GRAMMAR)))
	@echo OK
else ifeq (al,$(GRAMMAR))
	@echo NO
else
	@echo Hmmm?
endif
# 	@echo $(weforum_PARSER_FILES)
# 	@echo $(GRAMMAR)





ifeq (t,$(word 1,$(MAKECMDGOALS)))

ifeq (w,$(word 2,$(MAKECMDGOALS)))

ifeq (s,$(word 3,$(MAKECMDGOALS)))
# $(info $(MAKECMDGOALS))
# $(info $(wordlist 4,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
$(info test_weforum_sed)
endif

endif

else
endif



test :
ifeq (,$(filter $(GRAMMARS),$(G)))
	$(info test what?)
else
	$(info ok)
# 	$(info $(filter $(GRAMMARS),$(G)))
	@echo $(foreach grammar,$(filter $(GRAMMARS),$(G)),test_$(grammar))
endif






define test_weforum_sed
@cat $1 | sed -E $(SED_weforum)
endef

define test_weforum_gawk
@$(GAWK) -f weforum.gawk $1
endef

define makeGrammarPhonies
.PHONY : test_$1
.PHONY : test_$1_sed
.PHONY : test_$1_gawk
endef

define makeGrammarRules
$(call makeGrammarPhonies,$1)
$(if $(filter test_$1_sed,$(.VARIABLES)),test_$1 : | test_$1_sed,$(warning no_test_$1_sed))
$(if $(filter test_$1_sed,$(.VARIABLES)),test_$1_sed : $(DIR_TEMP)/$1.out ; $(call test_$1_sed,$$<),)
$(if $(filter test_$1_gawk,$(.VARIABLES)),test_$1_gawk : $(DIR_TEMP)/$1.out ; $(call test_$1_gawk,$$<),$(warning no_test_$1_gawk))
endef

$(foreach grammar,$(GRAMMARS),$(eval $(call makeGrammarRules,$(grammar))))




# test_weforum_sed : $(DIR_TEMP)/weforum.out ; $(call test_weforum_sed,$$<)
# test_weforum_gawk : $(DIR_TEMP)/weforum.out ; $(call test_weforum_gawk,$$<)
# $(foreach grammar,$(GRAMMARS),$(eval $(call makeGrammarRules,$(grammar))))


TEST_FUNCTIONS := $(filter test_%_sed test_%_gawk,$(.VARIABLES))
$(info TEST_FUNTIONS : $(TEST_FUNCTIONS))

# $(info $(foreach rule,$(TEST_FUNCTIONS),$(call grammarNameFromTestRule,$(rule))))

