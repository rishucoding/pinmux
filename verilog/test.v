module test;
    equality eq (out, in1, in2);
    reg [1:0]in1;
    reg in2;
    wire out;
    
    initial begin
        # 0 in1 = 2'b00;
            in2 = 1;
        #10 in1 = 2'b10;
            in2 = 0;
        #20 in1 = 2'b11;
            in2 = 1;
    end 
// Dump waves
   initial begin
    $dumpfile("dump.vcd");
    $dumpvars(1, mkpinmux);
    end

endmodule 
