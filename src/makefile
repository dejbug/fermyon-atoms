# NOTE TO SELF: Remember that I'm using my custom patched version of pygrun!
#	... So it is not available on the cloud's build servers.

include config.mk
include library.mk

# stophere : ; @echo -n

.PHONY : all clean reset purge

all : app.wasm | grammars

include app.mk
include grammars.mk

clean : ; rm -rf $(TempDir)

reset : | clean ; rm -rf $(GrammarsDir) *.wasm

purge : | reset ; rm -rf __pycache__

$(TempDir) : ; @mkdir .temp

include tests.mk

.PHONY : nix

nix : ; @echo -n
