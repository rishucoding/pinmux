module adder(out, in1, in2);
	input in1, in2;
	output [1:0] out; 
	wire [1:0]w1;
	assign w1 = 2'b10; 
//	assign out = 2'b10 == w1 && in2;
	assign out = (2'b10 == (w1 && in2));
// Dump waves
initial begin
    $dumpfile("dump1.vcd");
   	$dumpvars(1, adder);
end
endmodule
