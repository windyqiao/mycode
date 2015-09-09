`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2015/09/01 13:55:42
// Design Name: 
// Module Name: testbench
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module testbench #(
		parameter integer DATA_WIDTH = 8,
		parameter integer FIFO_DATA_WIDTH = 9
	)
	(
	);

	reg rst;
	wire clk;
	wire din_clk;
	reg valid;
	wire [DATA_WIDTH - 1 : 0] din_8b;
	wire asi_out;
	wire [FIFO_DATA_WIDTH - 1 : 0] din;
	wire [FIFO_DATA_WIDTH - 1 : 0] rdata;
	wire [FIFO_DATA_WIDTH - 1 : 0] dout;
	wire ce;
	wire [4 : 0] ce_sr;
	wire output_ready;
	wire start;
	wire [9:0] sout_data;
	wire [9:0] sout_data_1;
	wire [7:0] din_8b_R_debug;

	reg [2 : 0] i;

	initial begin
		rst = 0;
		#9
		rst = 1;
	end

	assign sout_data_1 = {
			sout_data[0],
			sout_data[1],
			sout_data[2],
			sout_data[3],
			sout_data[4],
			sout_data[5],
			sout_data[6],
			sout_data[7],
			sout_data[8],
			sout_data[9]
		};

	// Add user logic here
	clkgen #(.clk_period(6)) xiaofeiclk_wr(.clk(din_clk));
	clkgen #(.clk_period(1)) xiaofeiclk_rd(.clk(clk));

	data_gen_counter #(
			.I2S_SENDER_TEST_DATA_WIDTH(DATA_WIDTH)
		) data_gen(
			.rst(rst),
			.clk(din_clk),
			.data_source(din_8b)
		);
	
	always @(posedge din_clk) begin
		if(rst == 0) begin
			i <= 0;
			valid <= 0;
		end
		else begin
			if(i == 3) begin
				valid <= 0;
			end
			else begin
				valid <= 1;
			end
			i <= i + 1;
		end
	end
	
	ts2asi #(
			.FIFO_DATA_WIDTH(9)
		) ts2asi_inst (
			.rst(rst),
			.clk(clk),
			.din_clk(din_clk),
			.valid(valid),
			.din_8b(din_8b),
			.asi_out(asi_out),
			.din(din),
			.rdata(rdata),
			.dout(dout),
			.ce(ce),
			.ce_sr(ce_sr),
			.output_ready(output_ready),
			.start(start),
			.sout_data(sout_data),
			.din_8b_R_debug(din_8b_R_debug)
		);
	// User logic ends
endmodule