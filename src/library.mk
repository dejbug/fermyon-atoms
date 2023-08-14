# include config.mk

# deriveParserFiles(weforum) -> grammars/weforum/weforumLexer.py, etc.
define deriveParserFiles
$(GrammarsDir)/$1/$1Lexer.py $(GrammarsDir)/$1/$1Listener.py $(GrammarsDir)/$1/$1Parser.py
endef

# runPygrun(weforum)
# Depends on weforum parser files (grammars/weforum/*.py).
# Writes to stdout.
define runPygrun
cd $(GrammarsDir)/$(1) && $(PYGRUN) -e utf8 $(1) start --tokens ../../.cache/$(1).text
endef

# createPygrunOutputFile(.temp/weforum.out)
# Depends on weforum parser files (grammars/weforum/*.py).
# Writes to .temp/weforum.out .
define createPygrunOutputFile
$(eval _target = $(notdir $1))
$(eval _name = $(basename $(_target)))
cd $(GrammarsDir)/$(_name) && $(PYGRUN) -e utf8 $(_name) start --tokens ../../.cache/$(_name).text > ../../$(TempDir)/$(_target)
endef

define createPygrunOutputFile_nicer_but_test_me_first
$(eval _target = $(notdir $1))
$(eval _name = $(basename $(_target)))
$(call runPygrun,$(_name)) > ../../$(TempDir)/$(_target)
endef

define cleanUnnecessaryGrammarFiles
rm -f $(GrammarsDir)/**/*.tokens
rm -f $(GrammarsDir)/**/*.interp
endef

# grammarNameFromTestRule(test_weforum_sed) -> weforum
define grammarNameFromTestRule
$(word 2,$(subst _, ,$(filter test_%_sed test_%_gawk,$1)))
endef

# writeParserOutputRule(weforum)
# $(TempDir)/weforum.out : $(call deriveParserFiles,weforum) | $(TempDir) ; $(call createPygrunOutputFile,$@)
define writeParserOutputRule
$$(TempDir)/$1.out : $$(call deriveParserFiles,$1) | $$(TempDir) ; $$(call createPygrunOutputFile,$$@)
endef

# writeGrammarTarget(weforum) ->
# $(call deriveParserFiles,weforum) : weforum.g4
# 	$(ANTLR) -o grammars/$(basename $<) -Dlanguage=Python3 $<
# 	$(call cleanUnnecessaryGrammarFiles)
define writeGrammarTarget
$(call deriveParserFiles,$1) : $1.g4
	$(ANTLR) -o $(GrammarsDir)/$$(basename $$<) -Dlanguage=Python3 $$<
	$$(call cleanUnnecessaryGrammarFiles)
endef

# writeSimpleTests(weforum) ->
# test_weforum : $(call deriveParserFiles,weforum) ; $(call runPygrun,weforum)
# test_weforum_python : $(call deriveParserFiles,weforum) ; @python weforum.py
define writeSimpleTests
test_$1 : $(call deriveParserFiles,$1) ; $(call runPygrun,$1)
test_$1_python : $(call deriveParserFiles,$1) ; @python $1.py
endef

# writeSedTest(SED_weforum) -?
# .PHONY : test_weforum_sed
# test_weforum_sed : .temp/weforum.out ; @cat .temp/weforum.out | sed -E $(SED_weforum)
define writeSedTest
$(eval _sed = $1)
$(eval _name = $(word 2,$(subst _, ,$1)))
$(eval _in = $(TempDir)/$(_name).out)
.PHONY : test_$(_name)_sed
test_$(_name)_sed : $(TempDir)/$(_name).out ; @cat $(_in) | sed -E $$($(_sed))
endef

# writeGawkTest(weforum.gawk) ->
# @gawk -f weforum.gawk -- .temp/weforum.out
define writeGawkTest
$(eval _name = $(basename $1))
$(eval _in = $(TempDir)/$(_name).out)
$(eval _target = test_$(_name)_gawk)
.PHONY : $(_target)
$(_target) : $(_in) ; @$(GAWK) -f $1 -- $(_in)
endef



# Obsolete:


# writeRuleForTestFunction(test_weforum_sed) ->
# .PHONY : test_weforum_sed
# test_weforum_sed : .temp/weforum.out ; $(call test_weforum_sed,.temp/weforum.out)
define writeRuleForTestFunction
$(eval _name = $(call grammarNameFromTestRule,$1))
.PHONY : $1
$1 : $(TempDir)/$(_name).out ; $$(call $1,$(TempDir)/$(_name).out)
endef

# define test_weforum_gawk
# @$(GAWK) -f weforum.gawk -- $1
# endef
# TEST_FUNCTIONS := $(filter test_%_gawk,$(.VARIABLES))
# $(foreach name,$(TEST_FUNCTIONS),$(info $(call writeRuleForTestFunction,$(name))))
# $(foreach name,$(TEST_FUNCTIONS),$(eval $(call writeRuleForTestFunction,$(name))))
