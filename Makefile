CC=gcc
CXXFLAGS=-g -Wall -I./include
SRC=src
OBJDIR=obj
BINDIR=bin
INC_DIR=include

SRCFILES = avl-tree
SRCFILES_TSRC = $(addsuffix .c, $(SRCFILES))
SRCFILES_SRC = $(addprefix $(SRC)/, $(SRCFILES_TSRC))

SRCFILES_TOBJ = $(addsuffix .o, $(SRCFILES))
SRCFILES_OBJ = $(addprefix $(OBJDIR)/, $(SRCFILES_TOBJ))

DEP = $(SRCFILES_OBJ:.o=.d)

LIBS=
LINKS=$(addprefix -l, $(LIBS))

all: setup assn2-cli

setup:
	mkdir -p $(OBJDIR) $(BINDIR)

$(OBJDIR)/%.o: $(SRC)/%.c
	$(CC) $(CXXFLAGS) -c $< -o $@ $(LINKS)

assn2-cli: $(SRCFILES_OBJ)
	$(CC) $(CXXFLAGS) $? -o $(BINDIR)/assn2-cli $(LINKS)

clean:
	rm -f $(OBJDIR)/*.o $(BINDIR)/*
	rm -r obj bin
