module top_counter #(
    parameter int G_WIDTH = 9
)(
    input   logic                   clk,
    input   logic                   rst_n,
    input   logic                   enable,
    output  logic[G_WIDTH-1 : 0]    dout,
    output  logic                   carry
);

logic[G_WIDTH-1 : 0] s_cnt = '0;

always_ff @(posedge clk or negedge rst_n)begin
    if (!rst_n) begin
        s_cnt <= '0;
        carry <= '0;
    end else if (enable) begin
        if (s_cnt < G_WIDTH'(G_WIDTH)) begin
            s_cnt <= s_cnt + 1'b1;
            carry <= '0;
        end else begin
            s_cnt <= '0;
            carry <= '1;
        end
    end
end

assign dout = s_cnt;

endmodule