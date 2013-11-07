CC	= gcc
CFLAGS	+= -O3
BIN_DIR	= ./bin
SRC_DIR	= ./src
DOC_DIR	= ./docs
INC_DIR	= ./include
LIB_DIR	= ./lib
INSTALL_DIR = /usr/local/bin
BIN	= siftfeat match dspfeat comp

all: $(BIN) libopensift.a

docs:
	doxygen Doxyfile

libopensift.a:
	make -C $(SRC_DIR) $@

$(BIN):
	make -C $(SRC_DIR) $@

clean:
	make -C $(SRC_DIR) $@;	\
	make -C $(INC_DIR) $@;	\

distclean: clean
	rm -f $(LIB_DIR)/*
	rm -f $(BIN_DIR)/*

docsclean:
	rm -rf $(DOC_DIR)/html/

install:
	cp -fv $(BIN_DIR)/* $(INSTALL_DIR)/

.PHONY: docs clean docsclean libopensift.a
