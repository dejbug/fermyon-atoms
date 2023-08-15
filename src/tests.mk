# include library.mk

SED_weforum='s/.*"id":"([0-9]+)","*__typename":"([^"]+)"(,"(name|title|url)":"([^"]+)")?(,"(title|url)":"([^"]+)")?.*/  ID | \1\nTYPE | \2\nARG1 | \5\nARG2 | \8\n/p'
SED_linkedin='s/.*<div class="mb.*/\nSTART\n/; s/.*<img.*data-delayed-url="([^"]+).*/IMG: \1/; s|.*?<h2[^>]*>([^>]+)</h2>.*|TITLE: \1|; s/.*?<p[^>]*>([^<]+).*/TEXT: \1/'

GawkFiles := $(wildcard *.gawk)

$(foreach name,$(GrammarNames),$(eval $(call writeParserOutputRule,$(name))))
$(foreach name,$(GrammarNames),$(eval $(call writeSimpleTests,$(name))))
$(foreach file,$(GawkFiles),$(eval $(call writeGawkTest,$(file))))
$(foreach sed,$(filter SED_%,$(.VARIABLES)),$(eval $(call writeSedTest,$(sed))))

# Replace "eval" by "info" to debug.
