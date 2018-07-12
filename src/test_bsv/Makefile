### Makefile for the cclass project

TOP_MODULE:=mkpinmux
TOP_FILE:=pinmux.bsv
TOP_DIR:=./
WORKING_DIR := $(shell pwd)

BSVINCDIR:= .:%/Prelude:%/Libraries:%/Libraries/BlueNoC
default: gen_verilog

check-blue:
	@if test -z "$$BLUESPECDIR"; then echo "BLUESPECDIR variable not set"; exit 1; fi; 

###### Setting the variables for bluespec compile #$############################
BSVCOMPILEOPTS:= -check-assert -suppress-warnings G0020 -keep-fires -opt-undetermined-vals -remove-false-rules -remove-empty-rules -remove-starved-rules 
BSVLINKOPTS:=-parallel-sim-link 8 -keep-fires
VERILOGDIR:=./verilog/
BSVBUILDDIR:=./bsv_build/
BSVOUTDIR:=./bin
################################################################################

########## BSIM COMPILE, LINK AND SIMULATE TARGETS ##########################
.PHONY: check-restore
check-restore:
	@if [ "$(define_macros)" != "$(old_define_macros)" ];	then	make clean ;	fi;

.PHONY: gen_verilog 
gen_verilog: check-restore check-blue 
	@echo Compiling mkTbSoc in Verilog for simulations ...
	@mkdir -p $(BSVBUILDDIR); 
	@mkdir -p $(VERILOGDIR); 
	bsc -u -verilog -elab -vdir $(VERILOGDIR) -bdir $(BSVBUILDDIR) -info-dir $(BSVBUILDDIR) $(define_macros) -D verilog=True $(BSVCOMPILEOPTS) -verilog-filter ${BLUESPECDIR}/bin/basicinout -p $(BSVINCDIR) -g $(TOP_MODULE) $(TOP_DIR)/$(TOP_FILE) 2>&1 | tee bsv_compile.log
	@echo Compilation finished

#############################################################################

.PHONY: clean
clean:
	rm -rf $(BSVBUILDDIR) *.log $(BSVOUTDIR) ./bbl*
	rm -rf verilog obj_dir bsv_src

