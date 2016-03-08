
`timescale 1ns / 1ps
module F_normal_t10_next_Rom0(
input	          							clk_1x,
input	          							rst_n,
//////////////////////////////////////////////////////////////
input										rd_en,
input				[4:0]				rdaddr,
output		reg			[159:0]				rd_q
);

always @(posedge clk_1x)begin
	if(~rst_n)begin
		rd_q <= 160'b0;
	end
	else if(rd_en == 1'b1)begin
		case(rdaddr)
			5'h13: rd_q <= 160'b1000100110100110110111010001110110000000110001001000101111110111110000001110101000011110010101101111100011001100010101000011111110110111001100001010100000000110;
			5'h12: rd_q <= 160'b0100101010101011000010000001111010011111111010111111111110111111000010101011111110111100010110111010100100110111011100001111100100011100001110010010100111001011;
			5'h11: rd_q <= 160'b1000011000001110111110111110001011100111010100111001011111010000100011010110101100101100101110001000110100111101011011010101010111001001010101001011110100011111;
			5'h10: rd_q <= 160'b1110010000110101101100010011000001010111011111100110110011100001010011001010010000100000011001000001101110001010001110101111100110101110011011000010101111001001;
			5'h0f: rd_q <= 160'b1011111101000001111111110001101010110111101111011110101101010000011110000000011111111010111001111110011111001010101110111000010011010111011000110001111100111100;
			5'h0e: rd_q <= 160'b1110001101110100000111100001001000001110001010100011110111111010010000101101010001100000000001010000010100110100000001100111011000000011011110010011101011011011;
			5'h0d: rd_q <= 160'b0101101011100110010011001100010000011011011111000000100101100000000100001010000100010101110100111000100000100010100110101000010011011100000001010001010000001001;
			5'h0c: rd_q <= 160'b0111001010001010100111110111010000000011010101110010011100111001110110011100010011101110101011111101010011110011011011010000010011000110101110011000101000000110;
			5'h0b: rd_q <= 160'b0100101001010000001001000101110011110110011010000110110000010011110001001010011010010010101010110101000000011011010011111100000000100111010010001010000011101001;
			5'h0a: rd_q <= 160'b0001010000100000111100001101010100111011111010010101010001011010101110100101111101100001100101100110111001111110011010111100000110110100000101101011100110110000;
			5'h09: rd_q <= 160'b1111111000111100111111111000011101000101101101001001010011011011011100100000001010001010010000110111001111101110100111111100001110110110001101101101010110111101;
			5'h08: rd_q <= 160'b1111111111000101101011100011001000101100110010110100000000001100000111000100101100000011100101000000101100000010100101111001111111001011010110101001010010000001;
			5'h07: rd_q <= 160'b0001110000001111000010001000111010001101001111111011111111001001110110011000100100101101111000100011111010101001101101110101101000010000100010011010000100000100;
			5'h06: rd_q <= 160'b0111001111011111001110111000101001110010110000001110110110011000100111111000110000010010101010110100100010110100011111101000000101100111000110110110011111100011;
			5'h05: rd_q <= 160'b1100101001111110100011001000111001101011110100001011000110000110001101101000010110110001110110000110111000110110000000010000011110010001110001001100000111010010;
			5'h04: rd_q <= 160'b0010100000011111001111110110111001000000010101011010100011011100110101010000000100001011101110000101001000110010110101110001110111101111111100100010011011100000;
			5'h03: rd_q <= 160'b0110011010010010110001101111011011001110000100110011001010101110110011001001101010001001101101010111101000000111000011011100011100101011101110111000110000100100;
			5'h02: rd_q <= 160'b1101100001101010110011000001111011101010011101100110100000011111110010000100100110011000110011000101100100001111100100010000101110100000110111001101011111001001;
			5'h01: rd_q <= 160'b1011111101111101101000000110011110011001000000001110001101010100100001101000001100010111010111110100111110001000001111100010111100100101011011011010111111000000;
			5'h00: rd_q <= 160'b1100110111001010110011100011001100100111001111111100111011101111011101000001100110010010011010101101101111100101111101100001111001000011100011011001000110101010;
		default:rd_q <= 160'b0;
		endcase
	end
end

endmodule
