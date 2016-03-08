
`timescale 1ns / 1ps
module F_short_t12_next_Rom3(
input	          							clk_1x,
input	          							rst_n,
//////////////////////////////////////////////////////////////
input										rd_en,
input				[4:0]				rdaddr,
output		reg			[167:0]				rd_q
);

always @(posedge clk_1x)begin
	if(~rst_n)begin
		rd_q <= 168'b0;
	end
	else if(rd_en == 1'b1)begin
		case(rdaddr)
			5'h14: rd_q <= 168'b010001100110010001011111010101001000100010001111000001101000110000011001110001011101101001011010110011111100101111101111011110011100111110000001000101101100101111000001;
			5'h13: rd_q <= 168'b101101010011010010101010001100001000101010011011011100000000110110001001010011010110010100000011110100110001110111110001001111000011111101001010101100000101010010110101;
			5'h12: rd_q <= 168'b011011101111001000001100111011010101010100101011101011100100110000100100111000101111010111000101011010011010111111101101011101100101100111011001000001010001110010011001;
			5'h11: rd_q <= 168'b001001110011101010011000010100111110000110011010010110001000000010000001010110100101001001111101000011100111000011100110101001100000110101100001010000110000110001000000;
			5'h10: rd_q <= 168'b010100101111011101110110110111011010011000010010011000101111110111001011100001011011100010110000001001001010110101010110001011011010101010100110100011001110000000001101;
			5'h0f: rd_q <= 168'b100001111000101100000001011001100110010111010001101011111000110011110010000011001011111011011010111011011110000110011011111001111111111100001111010110010001100110001110;
			5'h0e: rd_q <= 168'b111001001111100011001010011110000111010111111101100001100010011001111101110101100111101000011001100100010011011101101000001011101101100110000110001000110110001111110010;
			5'h0d: rd_q <= 168'b101110010011110011111000101110100111111111111111000100100011010001100001100011011001000001001101011001010100011011001110101000111100110101010100100001001101010011011001;
			5'h0c: rd_q <= 168'b011101010011110100011010111000100100001101000011011101001001100110110010000110111101111111111010110111111101111100101001010011101101010001011110001000110010111010001001;
			5'h0b: rd_q <= 168'b011000010100010100001000000100010110011000000011001101101101011001001101000010010111000100001101111111100000110101111001000110111111101001101101110100101110000110110011;
			5'h0a: rd_q <= 168'b101010010110101100010011100111000010001100011000111000101100010100000010111000000010101001011011010010111011110110000011111101111010011110100101100001010010000100100111;
			5'h09: rd_q <= 168'b000010010010111010100001110010000001101011100101001101111101000111010011000101100100100011101010100010111101010001001100111101111110001001100101001010001110101011010101;
			5'h08: rd_q <= 168'b101100000101011011100100000010100100100101010110001001011011011010000000001101111111100010111111010001101100001111011100111100110000000110101101111010101011000010100100;
			5'h07: rd_q <= 168'b011010101001000100101011010101100010011101100000100100110111000101011110011101111101001011111101011110011100011010001101101011000000101000011111111100110010101011000001;
			5'h06: rd_q <= 168'b101101010001100001011111010001001000100000110100100111111001100001110100000010101101011100001011011101001010101111111100010111101110101010001111001011101011000101010100;
			5'h05: rd_q <= 168'b010101110100100001010000110111101110111000100100111100111011000010000111110000001010011000011011011101110100110110111111010110111110001010001011110111000101011110000000;
			5'h04: rd_q <= 168'b101001011111011111010000110110110011010100001001110101011011100100100110100011100000010101100010101010000011000100000000001010010100001010110101010100001001101001010101;
			5'h03: rd_q <= 168'b000101010101101010100101111100001011000110011110001110000001111001111110110010111010010100110110011111011010011001110100001010011100011001011010111000011000111011010110;
			5'h02: rd_q <= 168'b011101100100110010111111111011000011000111110101010001011001010000100111011100001010110101010011001111110110110001011100010110010010101000000010110111011001000001000111;
			5'h01: rd_q <= 168'b110101111110100101110100100010001000111000011010001011111100101111111010101111001000111000111010010001011001010001100101000100001101111101000001010011111000011011100111;
			5'h00: rd_q <= 168'b111111100010000011110111011000010001000001011100001111001111001100000000111000110011001101101000000000000011111100001110010011000001000011100001111110101100010101110001;
		default:rd_q <= 168'b0;
		endcase
	end
end

endmodule
