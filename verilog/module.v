module equality(out, in1, in2);
    input [1:0 ]in1;
    input in2;
    output out;
   // assign in1 = 2'b10;
   // assign in2 = 1;
    assign out = in1 == 2'b10 && in2;
endmodule
