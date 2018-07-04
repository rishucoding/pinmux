module test;
reg in1,in2;
wire [1:0] out;
adder a (out, in1, in2);
initial begin
	#0 in1 = 0; in2 = 0;
	#5 in1 = 1 ; in2 = 1;
	#10 in1 = 1 ;in2 = 0;
end

initial begin
#20 $finish;
end


endmodule

	
