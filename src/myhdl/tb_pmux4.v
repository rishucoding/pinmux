module tb_pmux4;

reg clk;
wire out;
reg ins_in_d;
reg ins_in_c;
reg ins_in_a;
reg ins_in_b;
reg sels_sel_a;
reg sels_sel_b;
reg sels_sel_c;
reg sels_sel_d;

initial begin
    $from_myhdl(
        clk,
        ins_in_d,
        ins_in_c,
        ins_in_a,
        ins_in_b,
        sels_sel_a,
        sels_sel_b,
        sels_sel_c,
        sels_sel_d
    );
    $to_myhdl(
        out
    );
end

pmux4 dut(
    clk,
    out,
    ins_in_d,
    ins_in_c,
    ins_in_a,
    ins_in_b,
    sels_sel_a,
    sels_sel_b,
    sels_sel_c,
    sels_sel_d
);

endmodule
