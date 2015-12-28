`timescale 1 ns / 1 ps

module axi4_stream_slave_v1_0 #
	(
		// Users to add parameters here

		// User parameters ends
		// Do not modify the parameters beyond this line


		// Parameters of Axi Slave Bus Interface S00_AXIS
		parameter integer C_S00_AXIS_TDATA_WIDTH = 32
	)
	(
		// Users to add ports here
		input wire rclk,
		input wire ren,
		output wire [C_S00_AXIS_TDATA_WIDTH - 1 : 0] rdata,
		output wire r_ready,
		output wire error_full,
		output wire error_empty,
		output wire fifo_wren,

		// User ports ends
		// Do not modify the ports beyond this line


		// Ports of Axi Slave Bus Interface S00_AXIS
		input wire s00_axis_aclk,
		input wire s00_axis_aresetn,
		output wire s00_axis_tready,
		input wire [C_S00_AXIS_TDATA_WIDTH - 1 : 0] s00_axis_tdata,
		input wire [(C_S00_AXIS_TDATA_WIDTH / 8) - 1 : 0] s00_axis_tstrb,
		input wire s00_axis_tlast,
		input wire s00_axis_tvalid
	);

	// Instantiation of Axi Bus Interface S00_AXIS
	axi4_stream_slave_v1_0_S00_AXIS # ( 
			.C_S_AXIS_TDATA_WIDTH(C_S00_AXIS_TDATA_WIDTH)
		) axi4_stream_slave_v1_0_S00_AXIS_inst (
			.rclk(rclk),
			.ren(ren),
			.rdata(rdata),
			.r_ready(r_ready),
			.error_full(error_full),
			.error_empty(error_empty),
			.fifo_wren(fifo_wren),

			.S_AXIS_ACLK(s00_axis_aclk),
			.S_AXIS_ARESETN(s00_axis_aresetn),
			.S_AXIS_TREADY(s00_axis_tready),
			.S_AXIS_TDATA(s00_axis_tdata),
			.S_AXIS_TSTRB(s00_axis_tstrb),
			.S_AXIS_TLAST(s00_axis_tlast),
			.S_AXIS_TVALID(s00_axis_tvalid)
		);

	// Add user logic here

	// User logic ends

	endmodule