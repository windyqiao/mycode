
`timescale 1ns / 1ps
module F_normal_t10_next_Rom6(
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
			5'h13: rd_q <= 160'b0011100111100001100110100100000101111110001001101110100100010011101010110010101011001101110000110101010101000101011010111001101100011110100001011111011100100001;
			5'h12: rd_q <= 160'b0011111010100000100110111111110110011110010111000111000010011101001101100000010011001011101110011101011111000100111001011010100111111001100100000101010001100110;
			5'h11: rd_q <= 160'b1010010100000000000010101000110001011111011000101000101110110101101100001110110011000100011001100111110010000001000100110110011100001011000100110101111100110011;
			5'h10: rd_q <= 160'b1101101110011100100010000001110011011101111001011000001010011110111000111011011110010010110001000111110000011011101111101110110110000001010011101101110011101010;
			5'h0f: rd_q <= 160'b1011100000000110101101100000010100111010001100111100111111011001100010010010110111000101111000100000011001111001111000010101100110111111010001110001101101111011;
			5'h0e: rd_q <= 160'b0111100011010100100010010010101101101100011110010011001001101111110000110101000001101011111000111101000100010010110000100110110000011110011101010000000000101001;
			5'h0d: rd_q <= 160'b1101100101100111110001111110101100001100110101011000101100001000111001101100011110000110000100101010001001010101000111000110110001110100100001110111100000010101;
			5'h0c: rd_q <= 160'b0011101000001101001010110100100011011000001010001010011110100000100100110100111001110110000000001011000111110101100101110111111111110011010000111101001110101001;
			5'h0b: rd_q <= 160'b0101000010000011110000110101010011101111101001010101000101101010111010010111110110000110010110011011100111111001101011110000011011010000010110101110011011000000;
			5'h0a: rd_q <= 160'b1100110100100101001100000101000000010100010010010110101101011101010010100111011001101100111110111101110100010011100001111000111101101010011110001010011011100011;
			5'h09: rd_q <= 160'b1100101011000000011101101000010110110001101101100011100000000000111100110101000001001011101001100011111010100011101001101111111010011111110010011010001000010011;
			5'h08: rd_q <= 160'b0111000000111100001000100011101000110100111111101111111100100111011001100010010010110111100010001111101010100110110111010110100001000010001001101000010000010000;
			5'h07: rd_q <= 160'b1101110000110001010101000001001011001010100010101010000110001101111111111110010001110110000000001101001101001001010100100111101011110010000011001100111110000001;
			5'h06: rd_q <= 160'b0001110000101100111111000111010010101101110110011111111000101000010110000110101010000010100101111010101001110001111111001001111111110101101100001111011101011111;
			5'h05: rd_q <= 160'b1010000001111100111111011011100100000001010101101010001101110011010101000000010000101110111000010100100011001011010111000111011110111111110010001001101110000000;
			5'h04: rd_q <= 160'b1000100100000110101000011110000000111001110001011101110101010100101100111011111000011010011110000001100110000100100111110110001111000000100011110110000010011101;
			5'h03: rd_q <= 160'b0101010001111101111111100011011010101011010000101001100001001111101000110101101000100110110001110111011010010111101111001010111100110001110100001010111100110011;
			5'h02: rd_q <= 160'b1101101101101101111101011110100001100111000100011010001010001101000110011010010000100100001001101101110100010001101010000100001001001001011101000001111100011010;
			5'h01: rd_q <= 160'b0000001011111101111101101000000110011110011001000000001110001101010100100001101000001100010111010111110100111110001000001111100010111100100101011011011010111111;
			5'h00: rd_q <= 160'b1100011011011000111101010111101001010100001101100111100110001000111000010100000111010110110100010100000001001001001011001011101111101110110101011100000011000011;
		default:rd_q <= 160'b0;
		endcase
	end
end

endmodule
