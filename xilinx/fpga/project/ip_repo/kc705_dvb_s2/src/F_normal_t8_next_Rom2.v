
`timescale 1ns / 1ps
module F_normal_t8_next_Rom2(
input	          							clk_1x,
input	          							rst_n,
//////////////////////////////////////////////////////////////
input										rd_en,
input				[4:0]				rdaddr,
output		reg			[127:0]				rd_q
);

always @(posedge clk_1x)begin
	if(~rst_n)begin
		rd_q <= 128'b0;
	end
	else if(rd_en == 1'b1)begin
		case(rdaddr)
			5'h0f: rd_q <= 128'b00110101000110011010011111001000001010111010110110001111111001100010111101111010011110010010001110111110101010010011100000001110;
			5'h0e: rd_q <= 128'b11101001111111101110011000111000110000000001010000010111000010100101100001111010100100010010101011000100001001101000101110001100;
			5'h0d: rd_q <= 128'b10110101010110010111001101011101110011101011001111100110010001101010011101110100101111010011010000110101010011011101111110101101;
			5'h0c: rd_q <= 128'b11000100000100101000010110000010101010000110110111110101111101111001001110111001101011100000011110010100010011110001000100100010;
			5'h0b: rd_q <= 128'b10111101110000000101100001001001111110011111111110010101010111110111011001111001000010001111010110111011100010000100110010110101;
			5'h0a: rd_q <= 128'b00000111101101100011100110011111000011011101000100100010000101101010101111100010111001011110010110011111100110111110011010001101;
			5'h09: rd_q <= 128'b11110001101110011100110100000000010000010000001100011000110101011110110011001111010000010111110011111011010011001111111100010101;
			5'h08: rd_q <= 128'b11100110100001010111100011100010110000010111001001101110111001011011001111101011110011100000000101010010110101101111101000001000;
			5'h07: rd_q <= 128'b11011001110001100111001110101010010001101001110000101110000011111101001110000100100100010000100000010100010111000111100011000001;
			5'h06: rd_q <= 128'b11111010100000101110000001000001011110111101011010000111110111001011101110000110111101100110010010001110101110000101000110001001;
			5'h05: rd_q <= 128'b01001001101100100001110110010000011000111110110110001110110110000000000000101101011111001000001010001010011111100110101110000111;
			5'h04: rd_q <= 128'b10100000110010101101001011110010101110101100101000001111010101001011101011000011001111000101101110001011111000101000111100001001;
			5'h03: rd_q <= 128'b10011101100011101100101010000010011111101001101010101101110010000011010111000101110111011100011001001111110111111101000101100001;
			5'h02: rd_q <= 128'b00011011101110011001000000010000110101101111010100110001001000011110111011110011001010101000010100000100111011100000101000010110;
			5'h01: rd_q <= 128'b00101010011111000110001100111001101010010110001011010100001001101011111000110001010111100010111010101000110001101111111010000010;
			5'h00: rd_q <= 128'b01011100010100010000111001000111110001111110010100101010000000000011010111000111000111011010100011010110101110010001110101101100;
		default:rd_q <= 128'b0;
		endcase
	end
end

endmodule
