// File: pmux_tb4.v
// Generated by MyHDL 0.10
// Date: Mon Jul  9 22:24:43 2018


`timescale 1ns/10ps

module pmux_tb4 (

);



reg in_d = 0;
reg sel_a = 0;
reg sel_b = 0;
reg sel_c = 0;
reg sel_d = 0;
reg in_a = 0;
reg in_b = 0;
reg clk = 0;
reg in_c = 0;
reg out = 0;



always @(posedge clk) begin: PMUX_TB4_PRINT_DATA
    $write("%h", in_a);
    $write(",");
    $write("%h", in_b);
    $write(",");
    $write("%h", in_c);
    $write(",");
    $write("%h", in_d);
    $write(",");
    $write("%h", sel_a);
    $write(",");
    $write("%h", sel_b);
    $write(",");
    $write("%h", sel_c);
    $write(",");
    $write("%h", sel_d);
    $write(",");
    $write("%h", out);
    $write("\n");
    if (sel_a) begin
        if ((out == in_a) !== 1) begin
            $display("*** AssertionError ***");
        end
    end
    else if (sel_b) begin
        if ((out == in_b) !== 1) begin
            $display("*** AssertionError ***");
        end
    end
    else if (sel_c) begin
        if ((out == in_c) !== 1) begin
            $display("*** AssertionError ***");
        end
    end
    else if (sel_d) begin
        if ((out == in_d) !== 1) begin
            $display("*** AssertionError ***");
        end
    end
end


initial begin: PMUX_TB4_CLK_SIGNAL
    reg sel_set;
    while (1'b1) begin
        sel_set = 1'b0;
        clk <= (!clk);
        if (clk) begin
            in_a <= (!in_a);
            if (in_a) begin
                in_b <= (!in_b);
                if (in_b) begin
                    in_c <= (!in_c);
                    if (in_c) begin
                        in_d <= (!in_d);
                        if (in_d) begin
                            sel_set = 1'b1;
                        end
                    end
                end
            end
        end
        if (sel_set) begin
            sel_a <= (!sel_a);
            if (sel_a) begin
                sel_b <= (!sel_b);
                if (sel_b) begin
                    sel_c <= (!sel_c);
                    if (sel_c) begin
                        sel_d <= (!sel_d);
                    end
                end
            end
        end
        # (20 / 2);
    end
end


always @(sel_a, sel_b, sel_c, sel_d, in_a, in_b, in_c, in_d) begin: PMUX_TB4_PMUX40_0_MAKE_OUT
    if (sel_a) begin
        out <= in_a;
    end
    else if (sel_b) begin
        out <= in_b;
    end
    else if (sel_c) begin
        out <= in_c;
    end
    else if (sel_d) begin
        out <= in_d;
    end
    else begin
        out <= 1'b0;
    end
end

endmodule