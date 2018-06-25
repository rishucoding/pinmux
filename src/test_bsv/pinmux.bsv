
/*
   This BSV file has been generated by the PinMux tool available at:
   https://bitbucket.org/casl/pinmux.

   Authors: Neel Gala, Luke
   Date of generation: Sun Jun 24 12:09:36 2018
*/

package pinmux;

   // FunctionType: contains the active wires of a function.  That INCLUDES
   // GPIO (as GPIO is also a "Function").  These are what get muxed.
   // However, only GPIO "Functions" will end up with Register SRAMs.
   typedef struct{
      Bit#(1) outputval;      // output from function to pad            bit2
      Bit#(1) inputval;       // input  from pad to function            bit1
      Bit#(1) output_en;      // output enable from core to pad         bit0
   } FunctionType deriving(Eq,Bits,FShow);

   typedef struct{
      Bit#(1) outputval;      // output from core to pad                bit7
      Bit#(1) output_en;      // output enable from core to pad         bit6
      Bit#(1) input_en;       // input enable from core to io_cell      bit5
   } GenericIOType deriving(Eq,Bits,FShow);

   interface MuxSelectionLines;

      // declare the method which will capture the user pin-mux
      // selection values.The width of the input is dependent on the number
      // of muxes happening per IO. For now we have a generalized width
      // where each IO will have the same number of muxes.
     method  Action cell0_mux (Bit#(1) in);
     method  Action cell1_mux (Bit#(1) in);
     method  Action cell2_mux (Bit#(1) in);
      endinterface

      interface PeripheralSide;
      // declare the interface to the IO cells.
      // Each IO cell will have 8 input field (output from pin mux
      // and on output field (input to pinmux)
          // interface declaration between IO-0 and pinmux
    (*always_ready,always_enabled*) method Bit#(1) io0_cell_outen;
    (*always_ready,always_enabled*) method Bit#(1) io0_cell_out;
    (*always_ready,always_enabled,result="io"*) method 
                       Action io0_inputval (Bit#(1) in);
          // interface declaration between IO-1 and pinmux
    (*always_ready,always_enabled*) method Bit#(1) io1_cell_outen;
    (*always_ready,always_enabled*) method Bit#(1) io1_cell_out;
    (*always_ready,always_enabled,result="io"*) method 
                       Action io1_inputval (Bit#(1) in);
          // interface declaration between IO-2 and pinmux
    (*always_ready,always_enabled*) method Bit#(1) io2_cell_outen;
    (*always_ready,always_enabled*) method Bit#(1) io2_cell_out;
    (*always_ready,always_enabled,result="io"*) method 
                       Action io2_inputval (Bit#(1) in);
          // interface declaration between UART-0 and pinmux
    (*always_ready,always_enabled*) method  Action uart_tx (Bit#(1) in);
    (*always_ready,always_enabled*) method  Bit#(1) uart_rx;
          // interface declaration between GPIOA-0 and pinmux
    (*always_ready,always_enabled*) method  Action gpioa_a0_out (Bit#(1) in);
    (*always_ready,always_enabled*) method  Action gpioa_a0_outen (Bit#(1) in);
    (*always_ready,always_enabled*) method  Bit#(1) gpioa_a0_in;
    (*always_ready,always_enabled*) method  Action gpioa_a1_out (Bit#(1) in);
    (*always_ready,always_enabled*) method  Action gpioa_a1_outen (Bit#(1) in);
    (*always_ready,always_enabled*) method  Bit#(1) gpioa_a1_in;
    (*always_ready,always_enabled*) method  Action gpioa_a2_out (Bit#(1) in);
    (*always_ready,always_enabled*) method  Action gpioa_a2_outen (Bit#(1) in);
    (*always_ready,always_enabled*) method  Bit#(1) gpioa_a2_in;
          // interface declaration between TWI-0 and pinmux
    (*always_ready,always_enabled*) method  Action twi_sda_out (Bit#(1) in);
    (*always_ready,always_enabled*) method  Action twi_sda_outen (Bit#(1) in);
    (*always_ready,always_enabled*) method  Bit#(1) twi_sda_in;
    (*always_ready,always_enabled*) method  Action twi_scl_out (Bit#(1) in);
    (*always_ready,always_enabled*) method  Action twi_scl_outen (Bit#(1) in);
    (*always_ready,always_enabled*) method  Bit#(1) twi_scl_in;
   endinterface

   interface Ifc_pinmux;
      interface MuxSelectionLines mux_lines;
      interface PeripheralSide peripheral_side;
   endinterface
   (*synthesize*)
   module mkpinmux(Ifc_pinmux);

      // the followins wires capture the pin-mux selection
      // values for each mux assigned to a CELL

      Wire#(Bit#(1)) wrcell0_mux<-mkDWire(0);
      Wire#(Bit#(1)) wrcell1_mux<-mkDWire(0);
      Wire#(Bit#(1)) wrcell2_mux<-mkDWire(0);
      // following wires capture signals to IO CELL if io-0 is
      // allotted to it
      Wire#(Bit#(1)) cell0_mux_out<-mkDWire(0);
      Wire#(Bit#(1)) cell0_mux_outen<-mkDWire(0);
      Wire#(Bit#(1)) cell0_mux_in<-mkDWire(0);

      // following wires capture signals to IO CELL if io-1 is
      // allotted to it
      Wire#(Bit#(1)) cell1_mux_out<-mkDWire(0);
      Wire#(Bit#(1)) cell1_mux_outen<-mkDWire(0);
      Wire#(Bit#(1)) cell1_mux_in<-mkDWire(0);

      // following wires capture signals to IO CELL if io-2 is
      // allotted to it
      Wire#(Bit#(1)) cell2_mux_out<-mkDWire(0);
      Wire#(Bit#(1)) cell2_mux_outen<-mkDWire(0);
      Wire#(Bit#(1)) cell2_mux_in<-mkDWire(0);

      // following wires capture signals to IO CELL if uart-0 is
      // allotted to it
      // declare wruart_tx_*, set up as type 'out'
      Wire#(Bit#(1)) wruart_tx<-mkDWire(0);
      // declare wruart_rx_*, set up as type 'input'
      Wire#(Bit#(1)) wruart_rx<-mkDWire(0);

      // following wires capture signals to IO CELL if gpioa-0 is
      // allotted to it
      Wire#(Bit#(1)) wrgpioa_a0_out<-mkDWire(0);
      Wire#(Bit#(1)) wrgpioa_a0_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrgpioa_a0_in<-mkDWire(0);
      Wire#(Bit#(1)) wrgpioa_a1_out<-mkDWire(0);
      Wire#(Bit#(1)) wrgpioa_a1_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrgpioa_a1_in<-mkDWire(0);
      Wire#(Bit#(1)) wrgpioa_a2_out<-mkDWire(0);
      Wire#(Bit#(1)) wrgpioa_a2_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrgpioa_a2_in<-mkDWire(0);

      // following wires capture signals to IO CELL if twi-0 is
      // allotted to it
      // declare wrtwi_sda_*, set up as type 'inout'
      Wire#(Bit#(1)) wrtwi_sda_out<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi_sda_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi_sda_in<-mkDWire(0);
      // declare wrtwi_scl_io*, set up as type 'inout'
      Wire#(Bit#(1)) wrtwi_scl_out<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi_scl_outen<-mkDWire(0);
      Wire#(Bit#(1)) wrtwi_scl_in<-mkDWire(0);


      /*====== This where the muxing starts for each io-cell======*/
      // TODO: this needs to stop using GenericIOType and
      // set the output (and only the output) as a wire
       // output muxer for cell idx 0
      cell0_mux_out=wrcell0_mux==0?wrgpioa_a0_out:
			wrcell0_mux==1?wruart_tx_out:
			0;

      // TODO: here is needed something which sets a new
      // wire, cell0_mux_outen
      cell0_mux_outen=
            wrcell0_mux==0?wrgpioa_a0_outen: // bi-directional
			wrcell0_mux==1?wrgpioa_a0_out_en: // i think....
			0;

      rule assign_wrgpioa_a0_in_on_cell0(wrcell0_mux==0);
        wrgpioa_a0_in<=cell0_mux_in;
      endrule

      // TODO: this needs to stop using GenericIOType and
      // set the output (and only the output) as a wire
      // output muxer for cell idx 1
      cell1_mux_out=wrcell1_mux==0?wrgpioa_a1_out:
			wrcell1_mux==1?0: // uart_rx is an input
			wrtwi_sda_out;

      // TODO: here is needed something which sets a new
      // wire, cell1_mux_outen
      cell1_mux_outen=
            wrcell1_mux==0?gpioa_a1_outen: // bi-directional
			wrcell1_mux==1?0: // uart_rx is an input
			wrtwi_sda_out_en; // bi-directional

      rule assign_wrgpioa_a1_in_on_cell1(wrcell1_mux==0);
        wrgpioa_a1_in<=cell1_mux_in;
      endrule


      rule assign_wruart_rx_on_cell1(wrcell1_mux==1);
        wruart_rx<=cell1_mux_in;
      endrule


      rule assign_wrtwi_sda_in_on_cell1(wrcell1_mux==2);
        wrtwi_sda_in<=cell1_mux_in;
      endrule

      // TODO: this needs to stop using GenericIOType and
      // set the output (and only the output) as a wire
      // output muxer for cell idx 2
      cell2_mux_out=
            wrcell2_mux==0?wrgpioa_a2_out:
			wrcell2_mux==1?0:
			wrtwi_scl_out;

      // TODO: here is needed something which sets a new
      // wire, cell2_mux_outen
      cell2_mux_outen=
            wrcell2_mux==0?wrgpioa_a2_outen: // bi-directional
			wrcell2_mux==1?0:
			wrtwi_scl_outen; // bi-directional


      rule assign_wrgpioa_a2_in_on_cell2(wrcell2_mux==0);
        wrgpioa_a2_in<=cell2_mux_in;
      endrule


      rule assign_wrtwi_scl_in_on_cell2(wrcell2_mux==2);
        wrtwi_scl_in<=cell2_mux_in;
      endrule


      /*============================================================*/

    interface mux_lines = interface MuxSelectionLines

      method Action  cell0_mux(Bit#(1) in);
         wrcell0_mux<=in;
      endmethod

      method Action  cell1_mux(Bit#(1) in);
         wrcell1_mux<=in;
      endmethod

      method Action  cell2_mux(Bit#(1) in);
         wrcell2_mux<=in;
      endmethod

    endinterface;
    interface peripheral_side = interface PeripheralSide

      method io0_cell_out=cell0_mux_out;
      method io0_cell_outen=cell0_mux_outen;
      method Action  io0_inputval(Bit#(1) in);
         cell0_mux_in<=in;
      endmethod

      method io1_cell_out=cell1_mux_out;
      method io1_cell_outen=cell1_mux_outen;
      method Action  io1_inputval(Bit#(1) in);
         cell1_mux_in<=in;
      endmethod

      method io2_cell_out=cell2_mux_out;
      method io2_cell_outen=cell2_mux_outen;
      method Action  io2_inputval(Bit#(1) in);
         cell2_mux_in<=in;
      endmethod

      method Action  uart_tx(Bit#(1) in);
         wruart_tx<=in;
      endmethod
      method uart_rx=wruart_rx;

      method Action  gpioa_a0_out(Bit#(1) in);
         wrgpioa_a0_out<=in;
      endmethod
      method Action  gpioa_a0_outen(Bit#(1) in);
         wrgpioa_a0_outen<=in;
      endmethod
      method gpioa_a0_in=wrgpioa_a0_in;
      method Action  gpioa_a1_out(Bit#(1) in);
         wrgpioa_a1_out<=in;
      endmethod
      method Action  gpioa_a1_outen(Bit#(1) in);
         wrgpioa_a1_outen<=in;
      endmethod
      method gpioa_a1_in=wrgpioa_a1_in;
      method Action  gpioa_a2_out(Bit#(1) in);
         wrgpioa_a2_out<=in;
      endmethod
      method Action  gpioa_a2_outen(Bit#(1) in);
         wrgpioa_a2_outen<=in;
      endmethod
      method gpioa_a2_in=wrgpioa_a2_in;

      method Action  twi_sda_out(Bit#(1) in);
         wrtwi_sda_out<=in;
      endmethod
      method Action  twi_sda_outen(Bit#(1) in);
         wrtwi_sda_outen<=in;
      endmethod
      method twi_sda_in=wrtwi_sda_in;
      method Action  twi_scl_out(Bit#(1) in);
         wrtwi_scl_out<=in;
      endmethod
      method Action  twi_scl_outen(Bit#(1) in);
         wrtwi_scl_outen<=in;
      endmethod
      method twi_scl_in=wrtwi_scl_in;

     endinterface;
   endmodule
endpackage
