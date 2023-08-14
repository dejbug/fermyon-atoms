# include config.mk

LibFiles := $(wildcard lib/*.py)

ReleaseGoals := release deploy

ifneq (,$(filter $(ReleaseGoals),$(MAKECMDGOALS)))
RELEASE := 1
endif

OptFlags := --strip-debug
ifeq (1,$(SQUEEZE))
OptFlags += -Oz
endif


app.wasm : $(ParserNames:%=%.py) | lib

%.o : %.c ; wasi-clang -o $@ -c $<
%.wagi : %.o ; wasi-clang -o $@ $^
%.wasi : %.py ; spin py2wasm $(basename $<) -o $@
%.wasm : %.wagi ; cp $< $@

ifeq (1,$(RELEASE))
%.wasm : %.wasi ; wasm-opt -o $@ $(OptFlags) $<
else
%.wasm : %.wasi ; cp $< $@
endif


.PHONY : lib

lib : $(LibFiles)


.PHONY : debug release

debug release : | all ;
