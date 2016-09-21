# -*- coding: utf-8 -*-
import re

def kc705_pins_key(x):
	#print x
	info = x[3]
	pattern = re.compile(r'([^\d]+)(\d+)')
	g = pattern.match(info)
	r = g.groups()
	return r[0], int(r[1])

def gen_list_kc705_net_group_part_pin():
	content = ''

	with open('kc705_signals.txt') as f:
		content = f.read()
	pattern = re.compile(r'\*SIGNAL\* (.*) \d+ \d+\r\n\s*([^\-\s]+)-([^\.]+)\.([^\s]+)')
	result = pattern.findall(content)
	list_kc705_net_group_part_pin = sorted(result, key = lambda x:(kc705_pins_key(x)))
	list_kc705_net_group_part_pin.append(('FMC_LPC_PRSNT_M2C_B_LS', 'J2', 'E', 'H2'))
	list_kc705_net_group_part_pin.append(('FMC_HPC_PRSNT_M2C_B_LS', 'J22', 'I', 'H2'))
	list_kc705_net_group_part_pin.append(('FMC_HPC_PG_M2C_LS', 'J22', 'F', 'F1'))
	list_kc705_net_group_part_pin.append(('FMC_C2M_PG_LS', 'J22', 'D', 'D1'))#not valid
	print '-' * 100
	print 'list_kc705_net_group_part_pin info'
	print '-' * 100
	for i in list_kc705_net_group_part_pin:
		print i
	print 'total:', len(list_kc705_net_group_part_pin)
	return list_kc705_net_group_part_pin

def fmc_pins_key(x):
	#print x
	info = x[5]
	pattern = re.compile(r'([^\d]+)(\d+)')
	g = pattern.match(info)
	r = g.groups()
	return r[0], int(r[1])

def gen_list_fmc_pin_resistor():
	content = ''

	with open('kc705FMC.txt') as f:
		content = f.read()
	pattern = re.compile(r'\*SIGNAL\* (.*) \d+ \d+\r\n(R[^\.]+)\.(\d+)\s+([^\-\s]+)-([^\.]+)\.([^\s]+)')
	result = pattern.findall(content)
	pattern = re.compile(r'\*SIGNAL\* (.*) \d+ \d+\r\n([^\-\s]+)-([^\.]+)\.([^\s]+)\s+(R[^\.]+)\.(\d+)')
	result.extend([(x[0], x[4], x[5], x[1], x[2], x[3]) for x in pattern.findall(content)])
	fmc_pins = sorted(result, key = lambda x:(fmc_pins_key(x)))
	list_fmc_pin_resistor = []
	for i in fmc_pins:
		list_fmc_pin_resistor.append((i[5], i[1] + '.' + i[2]))
	list_fmc_pin_resistor.append(('F1', 'R113.1'))
	list_fmc_pin_resistor.append(('H2', 'R62.1'))
	print '-' * 100
	print 'list_fmc_pin_resistor info'
	print '-' * 100
	for i in list_fmc_pin_resistor:
		print i
	print 'total:', len(list_fmc_pin_resistor)
	return list_fmc_pin_resistor

def gen_map_kc705_pin_net():
	map_kc705_pin_net = {}
	lines = []
	with open('kc705_package_pin_nets.txt') as f:
		lines = f.read().splitlines()

	for i in lines:
		l = i.split()
		item = {l[0] : l[1]}
		if len(l) == 2:
			map_kc705_pin_net.update(item)

	print '-' * 100
	print 'map_kc705_pin_net info'
	print '-' * 100
	for i in map_kc705_pin_net.items():
		print i
	print 'total:', len(map_kc705_pin_net)

	return map_kc705_pin_net

def gen_map_kc705_pin_iotype():
	map_kc705_pin_iotype = {}
	lines = []
	with open('kc705_io_package_pins.txt') as f:
		lines = f.read().splitlines()

	for i in lines:
		l = i.split()
		item = {l[0] : l[1]}
		if len(l) == 8:
			map_kc705_pin_iotype.update(item)

	print '-' * 100
	print 'map_kc705_pin_iotype info'
	print '-' * 100
	for i in map_kc705_pin_iotype.items():
		print i
	print 'total:', len(map_kc705_pin_iotype)

	return map_kc705_pin_iotype

def remove_unused_pin(map_kc705_pin_net):
	list_unsupport_pin_net = []
	unsupport_pin = [
		'F2',
		'F5',
		'F6',
		'C8',
		'C3',
		'C7',
		'C4',
		'F1',
		'B5',
		'B6',
		'B1',
		'B2',
		'E8',
		'E4',
		'E7',
		'E3',
		'N8',
		'N7',
		'A3',
		'A4',
		'A7',
		'A8',
		'D6',
		'D5',
		'D2',
		'D1',
	]
	
	for i in unsupport_pin:
		if i in map_kc705_pin_net.keys():
			net = map_kc705_pin_net.pop(i)
			item = (i, net)
			list_unsupport_pin_net.append(item)
	print '-' * 100
	print 'list_unsupport_pin_net info'
	print '-' * 100
	for i in list_unsupport_pin_net:
		print i
	print 'total:', len(list_unsupport_pin_net)


#cat log | sed 's/:\|(\|)/ /g' | awk '{print $1":"$5":"$3":"$6}' | sed 's/\([^:]\+\):\([^:]\+\):\([^:]\+\):\([^:]\+\)/\1 : \"\2\",\n\3 : \"\4\",/g' | sed -e "s/\"/'/g"
def get_newboard_map_slot_map_portnum_pin():
	map_slot_map_portnum_pin = {
		'J102' : {
			5 : 'Y30',
			6 : 'AA30',
			7 : 'AB29',
			8 : 'AB30',
			9 : 'AC29',
			10 : 'AC30',
			11 : 'AB27',
			12 : 'AC27',
			13 : 'AD29',
			14 : 'AE29',
			17 : 'AE30',
			18 : 'AF30',
			19 : 'AE28',
			20 : 'AF28',
			21 : 'AG30',
			22 : 'AH30',
			23 : 'AK29',
			24 : 'AK30',
			25 : 'AJ28',
			26 : 'AJ29',
			29 : 'AG27',
			30 : 'AG28',
			31 : 'AH26',
			32 : 'AH27',
			33 : 'AJ27',
			34 : 'AK28',
			35 : 'AJ26',
			36 : 'AK26',
			37 : 'AF26',
			38 : 'AF27',
		},
		'J101' : {
			5 : 'AC26',
			6 : 'AD26',
			7 : 'AE25',
			8 : 'AF25',
			9 : 'AC24',
			10 : 'AD24',
			11 : 'AJ24',
			12 : 'AK25',
			13 : 'AJ22',
			14 : 'AJ23',
			17 : 'AG22',
			18 : 'AH22',
			19 : 'AD23',
			20 : 'AE24',
			21 : 'AC22',
			22 : 'AD22',
			23 : 'AF20',
			24 : 'AF21',
			25 : 'AG20',
			26 : 'AH20',
			29 : 'AK20',
			30 : 'AK21',
			31 : 'AE23',
			32 : 'AF23',
			33 : 'AB24',
			34 : 'AC25',
			35 : 'AK23',
			36 : 'AK24',
			37 : 'AD21',
			38 : 'AE21',
		},
		'J96' : {
			5 : 'D17',
			6 : 'D27',
			7 : 'D18',
			8 : 'C27',
			9 : 'C25',
			10 : 'D26',
			11 : 'B25',
			12 : 'C26',
			13 : 'H24',
			14 : 'H26',
			17 : 'H25',
			18 : 'H27',
			19 : 'G28',
			20 : 'G29',
			21 : 'F28',
			22 : 'F30',
			23 : 'H30',
			24 : 'E28',
			25 : 'G30',
			26 : 'D28',
			29 : 'E29',
			30 : 'B30',
			31 : 'E30',
			32 : 'A30',
			33 : 'D29',
			34 : 'G27',
			35 : 'C30',
			36 : 'F27',
			37 : 'C29',
			38 : 'B29',
		},
		'J86' : {
			5 : 'D21',
			6 : 'C21',
			7 : 'D16',
			8 : 'E18',
			9 : 'C16',
			10 : 'F16',
			11 : 'K18',
			12 : 'J18',
			13 : 'H20',
			14 : 'G20',
			17 : 'J17',
			18 : 'H17',
			19 : 'B23',
			20 : 'A23',
			21 : 'E23',
			22 : 'D23',
			23 : 'F25',
			24 : 'E25',
			25 : 'E24',
			26 : 'D24',
			29 : 'F26',
			30 : 'E26',
			31 : 'G23',
			32 : 'G24',
			33 : 'J19',
			34 : 'H19',
			35 : 'L17',
			36 : 'L18',
			37 : 'K19',
			38 : 'K20',
		},
		'J97' : {
			5 : 'A25',
			6 : 'B28',
			7 : 'A26',
			8 : 'A28',
			9 : 'C24',
			10 : 'B27',
			11 : 'B24',
			12 : 'A27',
			13 : 'F20',
			14 : 'F21',
			17 : 'E20',
			18 : 'E21',
			19 : 'G18',
			20 : 'E19',
			21 : 'F18',
			22 : 'D19',
			23 : 'A20',
			24 : 'C20',
			25 : 'A21',
			26 : 'B20',
			29 : 'B22',
			30 : 'A16',
			31 : 'A22',
			32 : 'A17',
			33 : 'G17',
			34 : 'B18',
			35 : 'F17',
			36 : 'A18',
			37 : 'C19',
			38 : 'B19',
		},
		'J95' : {
			5 : 'H15',
			6 : 'L15',
			7 : 'G15',
			8 : 'K15',
			9 : 'G13',
			10 : 'K14',
			11 : 'F13',
			12 : 'J14',
			13 : 'H11',
			14 : 'K13',
			17 : 'H12',
			18 : 'J13',
			19 : 'J11',
			20 : 'L11',
			21 : 'J12',
			22 : 'K11',
			23 : 'L12',
			25 : 'L13',
			26 : 'G19',
			29 : 'C17',
			30 : 'D22',
			31 : 'B17',
			32 : 'C22',
			33 : 'G22',
			35 : 'F22',
			37 : 'H21',
			38 : 'H22',
		},
		'J94' : {
			5 : 'D12',
			6 : 'H14',
			7 : 'D13',
			8 : 'G14',
			9 : 'D11',
			10 : 'C12',
			11 : 'C11',
			12 : 'B12',
			13 : 'F11',
			14 : 'F15',
			17 : 'E11',
			18 : 'E16',
			19 : 'D14',
			20 : 'B14',
			21 : 'C14',
			22 : 'A15',
			23 : 'E14',
			24 : 'F12',
			25 : 'E15',
			26 : 'E13',
			29 : 'A11',
			30 : 'B13',
			31 : 'A12',
			32 : 'A13',
			33 : 'C15',
			34 : 'L16',
			35 : 'B15',
			36 : 'K16',
			37 : 'J16',
			38 : 'H16',
		},
		'J82' : {
			3 : 'N30',
			5 : 'U30',
			6 : 'L20',
			7 : 'T25',
			8 : 'U25',
			9 : 'R19',
			10 : 'U28',
			11 : 'T26',
			12 : 'T27',
			13 : 'R28',
			14 : 'T28',
			17 : 'V26',
			18 : 'U27',
			19 : 'R30',
			20 : 'W19',
			21 : 'J21',
			22 : 'R23',
			23 : 'K30',
			24 : 'M27',
			25 : 'N29',
			26 : 'M28',
			29 : 'N25',
			30 : 'N27',
			31 : 'L28',
			32 : 'M29',
			33 : 'K26',
			34 : 'J26',
			35 : 'J28',
			36 : 'L30',
			37 : 'J29',
		},
		'J98' : {
			5 : 'L25',
			6 : 'AA26',
			7 : 'K25',
			8 : 'Y26',
			9 : 'M20',
			10 : 'Y25',
			11 : 'P19',
			12 : 'NIL',
			13 : 'NIL',
			14 : 'NIL',
			17 : 'AVP',
			18 : 'J23',
			19 : 'AVN',
			20 : 'J24',
			21 : 'L22',
			22 : 'THD',
			23 : 'L23',
			24 : 'THD',
			25 : 'AB25',
			26 : 'AA25',
			29 : 'AB28',
			30 : 'AA27',
			31 : 'AH24',
			32 : 'Y14',
			33 : 'Y20',
			34 : 'AB14',
			35 : 'NIL',
			36 : 'AG17',
			37 : 'NIL',
			38 : 'NIL',
		},
		'J87' : {
			3 : 'G7',
			4 : 'B1',
			5 : 'G8',
			6 : 'B2',
			7 : 'A8',
			8 : 'B5',
			9 : 'A4',
			10 : 'B6',
			13 : 'A3',
			14 : 'A7',
			15 : 'C8',
			16 : 'E8',
			17 : 'C7',
			18 : 'E7',
		},
	}

	return map_slot_map_portnum_pin


def map_port_property_iic_slave():
	map_port_property = {
		'iic_scl': ['CLOCK_DEDICATED_ROUTE FALSE'],
	}

	return map_port_property

def list_net_port_iic_slave():
	list_net_port = [
		('FMC_HPC_LA28_P', 'iic_scl'),
		('FMC_HPC_LA21_P', 'iic_sda'),
	]

	return list_net_port

def map_port_property_new_i2s_board():
	map_port_property = {
		'bclk[0]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[0]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[0]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[1]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[1]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[1]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[2]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[2]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[2]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[3]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[3]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[3]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[4]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[4]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[4]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[5]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[5]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[5]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[6]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[6]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[6]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[7]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[7]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[7]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[8]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[8]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[8]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[9]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[9]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[9]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[10]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[10]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[10]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[11]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[11]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[11]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[12]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[12]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[12]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[13]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[13]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[13]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[14]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[14]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[14]': ['CLOCK_DEDICATED_ROUTE FALSE'],

		'bclk[15]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'lrclk[15]': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'sdata[15]': ['CLOCK_DEDICATED_ROUTE FALSE'],
	}

	return map_port_property

def list_pin_port_new_i2s_board():
	list_pin_port = [
		('AG22', 'bclk[0]'),
		('AH22', 'lrclk[0]'),
		('AD23', 'sdata[0]'),
		('AE24', 'bclk[1]'),
		('AC22', 'lrclk[1]'),
		('AD22', 'sdata[1]'),
		('AF20', 'bclk[2]'),
		('AF21', 'lrclk[2]'),
		('AG20', 'sdata[2]'),
		('AH20', 'bclk[3]'),
		('AK20', 'lrclk[3]'),
		('AK21', 'sdata[3]'),
		('AE23', 'bclk[4]'),
		('AF23', 'lrclk[4]'),
		('AB24', 'sdata[4]'),
		('AC25', 'bclk[5]'),
		('AK23', 'lrclk[5]'),
		('AK24', 'sdata[5]'),
		('Y30', 'bclk[6]'),
		('AA30', 'lrclk[6]'),
		('AB29', 'sdata[6]'),
		('AB30', 'bclk[7]'),
		('AC29', 'lrclk[7]'),
		('AC30', 'sdata[7]'),
		('AB27', 'bclk[8]'),
		('AC27', 'lrclk[8]'),
		('AD29', 'sdata[8]'),
		('AE29', 'bclk[9]'),
		('AE30', 'lrclk[9]'),
		('AF30', 'sdata[9]'),
		('AE28', 'bclk[10]'),
		('AF28', 'lrclk[10]'),
		('AG30', 'sdata[10]'),
		('AH30', 'bclk[11]'),
		('AK29', 'lrclk[11]'),
		('AK30', 'sdata[11]'),
		('AJ28', 'bclk[12]'),
		('AJ29', 'lrclk[12]'),
		('AG27', 'sdata[12]'),
		('AG28', 'bclk[13]'),
		('AH26', 'lrclk[13]'),
		('AH27', 'sdata[13]'),
		('AJ27', 'bclk[14]'),
		('AK28', 'lrclk[14]'),
		('AJ26', 'sdata[14]'),
		('AK26', 'bclk[15]'),
		('AF26', 'lrclk[15]'),
		('AF27', 'sdata[15]'),
	]

	return list_net_port

def map_port_property_new_tsp_board_j94():
	map_port_property = {
		'mpeg_clk': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'fs_0p5_en': ['CLOCK_DEDICATED_ROUTE FALSE'],
	}

	return map_port_property

def list_pin_port_new_tsp_board_j94():
	list_pin_port = [
		('D12', 'mpeg_clk'),
		('H14', 'mpeg_sync'),
		('E16', 'mpeg_valid'),
		('D13', 'mpeg_data[0]'),
		('G14', 'mpeg_data[1]'),
		('D11', 'mpeg_data[2]'),
		('F11', 'mpeg_data[3]'),
		('B12', 'mpeg_data[4]'),
		('E11', 'mpeg_data[5]'),
		('F15', 'mpeg_data[6]'),
		('D14', 'mpeg_data[7]'),

		('A11', 'asi_out_p'),
		('A12', 'asi_out_n'),

		#('C29', 'fs_0p5_en'),#???G23

		#('H25', 'symbol_2x_oe'),
	      
		#('H24', 'symbol_2x_re_out[0]'),
		#('H26', 'symbol_2x_re_out[1]'),
		#('B25', 'symbol_2x_re_out[2]'),
		#('C26', 'symbol_2x_re_out[3]'),
		#('C25', 'symbol_2x_re_out[4]'),
		#('D26', 'symbol_2x_re_out[5]'),
		#('D18', 'symbol_2x_re_out[6]'),
		#('C27', 'symbol_2x_re_out[7]'),
		#('D17', 'symbol_2x_re_out[8]'),
		#('D27', 'symbol_2x_re_out[9]'),
		#('K19', 'symbol_2x_re_out[10]'),
		#('K20', 'symbol_2x_re_out[11]'),
		#('L17', 'symbol_2x_re_out[12]'),
		#('L18', 'symbol_2x_re_out[13]'),
		#('J19', 'symbol_2x_re_out[14]'),
		#('H19', 'symbol_2x_re_out[15]'),

		#('C30', 'symbol_2x_im_out[0]'),
		#('F27', 'symbol_2x_im_out[1]'),
		#('D29', 'symbol_2x_im_out[2]'),
		#('G27', 'symbol_2x_im_out[3]'),
		#('E30', 'symbol_2x_im_out[4]'),
		#('A30', 'symbol_2x_im_out[5]'),
		#('E29', 'symbol_2x_im_out[6]'),
		#('B30', 'symbol_2x_im_out[7]'),
		#('G30', 'symbol_2x_im_out[8]'),
		#('D28', 'symbol_2x_im_out[9]'),
		#('H30', 'symbol_2x_im_out[10]'),
		#('E28', 'symbol_2x_im_out[11]'),
		#('F28', 'symbol_2x_im_out[12]'),
		#('F30', 'symbol_2x_im_out[13]'),
		#('G28', 'symbol_2x_im_out[14]'),
		#('G29', 'symbol_2x_im_out[15]'),
	]

	return list_pin_port

def list_net_port_new_tsp_board_j94():
	list_net_port = [
		('FMC_HPC_HA00_CC_P', 'mpeg_clk'),
		('FMC_HPC_HA01_CC_P', 'mpeg_sync'),
		('FMC_HPC_HA05_N', 'mpeg_valid'),
		('FMC_HPC_HA00_CC_N', 'mpeg_data[0]'),
		('FMC_HPC_HA01_CC_N', 'mpeg_data[1]'),
		('FMC_HPC_HA02_P', 'mpeg_data[2]'),
		('FMC_HPC_HA04_P', 'mpeg_data[3]'),
		('FMC_HPC_HA03_N', 'mpeg_data[4]'),
		('FMC_HPC_HA04_N', 'mpeg_data[5]'),
		('FMC_HPC_HA05_P', 'mpeg_data[6]'),
		('FMC_HPC_HA06_P', 'mpeg_data[7]'),

		('FMC_HPC_HA10_P', 'asi_out_p'),
		('FMC_HPC_HA10_N', 'asi_out_n'),

		#('FMC_LPC_CLK0_M2C_P', 'fs_0p5_en'),

		#('FMC_LPC_LA10_P', 'symbol_2x_oe'),
	      
		#('FMC_LPC_LA00_CC_P', 'symbol_2x_re_out[0]'),
		#('FMC_LPC_LA02_P', 'symbol_2x_re_out[1]'),
		#('FMC_LPC_LA00_CC_N', 'symbol_2x_re_out[2]'),
		#('FMC_LPC_LA02_N', 'symbol_2x_re_out[3]'),
		#('FMC_LPC_LA03_P', 'symbol_2x_re_out[4]'),
		#('FMC_LPC_LA04_P', 'symbol_2x_re_out[5]'),
		#('FMC_LPC_LA03_N', 'symbol_2x_re_out[6]'),
		#('FMC_LPC_LA04_N', 'symbol_2x_re_out[7]'),
		#('FMC_LPC_LA07_P', 'symbol_2x_re_out[8]'),
		#('FMC_LPC_LA08_P', 'symbol_2x_re_out[9]'),
		#('FMC_LPC_LA01_CC_P', 'symbol_2x_re_out[10]'),
		#('FMC_LPC_LA01_CC_N', 'symbol_2x_re_out[11]'),
		#('FMC_LPC_LA06_P', 'symbol_2x_re_out[12]'),
		#('FMC_LPC_LA06_N', 'symbol_2x_re_out[13]'),
		#('FMC_LPC_LA05_P', 'symbol_2x_re_out[14]'),
		#('FMC_LPC_LA05_N', 'symbol_2x_re_out[15]'),

		#('FMC_LPC_LA10_N', 'symbol_2x_im_out[0]'),
		#('FMC_LPC_LA09_P', 'symbol_2x_im_out[1]'),
		#('FMC_LPC_LA09_N', 'symbol_2x_im_out[2]'),
		#('FMC_LPC_LA13_P', 'symbol_2x_im_out[3]'),
		#('FMC_LPC_LA14_P', 'symbol_2x_im_out[4]'),
		#('FMC_LPC_LA13_N', 'symbol_2x_im_out[5]'),
		#('FMC_LPC_LA14_N', 'symbol_2x_im_out[6]'),
		#('FMC_LPC_LA07_N', 'symbol_2x_im_out[7]'),
		#('FMC_LPC_LA08_N', 'symbol_2x_im_out[8]'),
		#('FMC_LPC_LA12_P', 'symbol_2x_im_out[9]'),
		#('FMC_LPC_LA11_P', 'symbol_2x_im_out[10]'),
		#('FMC_LPC_LA12_N', 'symbol_2x_im_out[11]'),
		#('FMC_LPC_LA11_N', 'symbol_2x_im_out[12]'),
		#('FMC_LPC_LA16_P', 'symbol_2x_im_out[13]'),
		#('FMC_LPC_LA16_N', 'symbol_2x_im_out[14]'),
		#('FMC_LPC_LA15_P', 'symbol_2x_im_out[15]'),
	]

	return list_net_port

def map_port_property_new_tsp_board_j97():
	map_port_property = {
		'mpeg_clk': ['CLOCK_DEDICATED_ROUTE FALSE'],
	}

	return map_port_property

def list_net_port_new_tsp_board_j97():
	list_net_port = [
		('FMC_HPC_LA13_P', 'mpeg_clk'),
		('FMC_HPC_LA14_P', 'mpeg_sync'),
		('FMC_HPC_LA18_CC_N', 'mpeg_valid'),
		('FMC_HPC_LA13_N', 'mpeg_data[0]'),
		('FMC_HPC_LA14_N', 'mpeg_data[1]'),
		('FMC_HPC_LA15_P', 'mpeg_data[2]'),
		('FMC_HPC_LA17_CC_P', 'mpeg_data[3]'),
		('FMC_HPC_LA16_N', 'mpeg_data[4]'),
		('FMC_HPC_LA17_CC_N', 'mpeg_data[5]'),
		('FMC_HPC_LA18_CC_P', 'mpeg_data[6]'),
		('FMC_HPC_LA19_P', 'mpeg_data[7]'),

		('FMC_HPC_LA23_P', 'asi_out_p'),
		('FMC_HPC_LA23_N', 'asi_out_n'),
	]

	return list_net_port

def map_port_property_old_tsp_board_2ab42e394123204b24255388e7e131aab67b6328():
	map_port_property = {
		'mpeg_clk': ['CLOCK_DEDICATED_ROUTE FALSE'],
		#'fs_0p5_en': ['CLOCK_DEDICATED_ROUTE FALSE'],

		#'symbol_2x_oe' : ['slew FAST'],

		#'symbol_2x_re_out[0]' : ['slew FAST'],
		#'symbol_2x_re_out[1]' : ['slew FAST'],
		#'symbol_2x_re_out[2]' : ['slew FAST'],
		#'symbol_2x_re_out[3]' : ['slew FAST'],
		#'symbol_2x_re_out[4]' : ['slew FAST'],
		#'symbol_2x_re_out[5]' : ['slew FAST'],
		#'symbol_2x_re_out[6]' : ['slew FAST'],
		#'symbol_2x_re_out[7]' : ['slew FAST'],
		#'symbol_2x_re_out[8]' : ['slew FAST'],
		#'symbol_2x_re_out[9]' : ['slew FAST'],
		#'symbol_2x_re_out[10]' : ['slew FAST'],
		#'symbol_2x_re_out[11]' : ['slew FAST'],
		#'symbol_2x_re_out[12]' : ['slew FAST'],
		#'symbol_2x_re_out[13]' : ['slew FAST'],
		#'symbol_2x_re_out[14]' : ['slew FAST'],
		#'symbol_2x_re_out[15]' : ['slew FAST'],

		#'symbol_2x_im_out[0]' : ['slew FAST'],
		#'symbol_2x_im_out[1]' : ['slew FAST'],
		#'symbol_2x_im_out[2]' : ['slew FAST'],
		#'symbol_2x_im_out[3]' : ['slew FAST'],
		#'symbol_2x_im_out[4]' : ['slew FAST'],
		#'symbol_2x_im_out[5]' : ['slew FAST'],
		#'symbol_2x_im_out[6]' : ['slew FAST'],
		#'symbol_2x_im_out[7]' : ['slew FAST'],
		#'symbol_2x_im_out[8]' : ['slew FAST'],
		#'symbol_2x_im_out[9]' : ['slew FAST'],
		#'symbol_2x_im_out[10]' : ['slew FAST'],
		#'symbol_2x_im_out[11]' : ['slew FAST'],
		#'symbol_2x_im_out[12]' : ['slew FAST'],
		#'symbol_2x_im_out[13]' : ['slew FAST'],
		#'symbol_2x_im_out[14]' : ['slew FAST'],
		#'symbol_2x_im_out[15]' : ['slew FAST'],
	}

	return map_port_property

def list_net_port_old_tsp_board_2ab42e394123204b24255388e7e131aab67b6328():
	list_net_port = [
		('FMC_LPC_LA25_P', 'mpeg_clk'),
		('FMC_LPC_LA29_P', 'mpeg_valid'),
		('FMC_LPC_LA24_P', 'mpeg_data[0]'),
		('FMC_LPC_LA24_N', 'mpeg_data[1]'),
		('FMC_LPC_LA26_P', 'mpeg_data[2]'),
		('FMC_LPC_LA31_P', 'mpeg_data[3]'),
		('FMC_LPC_LA31_N', 'mpeg_data[4]'),
		('FMC_LPC_LA28_P', 'mpeg_data[5]'),
		('FMC_LPC_LA28_N', 'mpeg_data[6]'),
		('FMC_LPC_LA29_N', 'mpeg_data[7]'),
		('FMC_LPC_LA25_N', 'mpeg_sync'),

		#('FMC_HPC_HA23_N', 'ts_out_sync'),
		#('FMC_HPC_HA23_P', 'slot0_out_dump_flag'),

		#('FMC_LPC_LA10_P', 'symbol_2x_oe'),
		#	
		#('FMC_LPC_LA00_CC_P', 'symbol_2x_re_out[0]'),
		#('FMC_LPC_LA02_P', 'symbol_2x_re_out[1]'),
		#('FMC_LPC_LA00_CC_N', 'symbol_2x_re_out[2]'),
		#('FMC_LPC_LA02_N', 'symbol_2x_re_out[3]'),
		#('FMC_LPC_LA03_P', 'symbol_2x_re_out[4]'),
		#('FMC_LPC_LA04_P', 'symbol_2x_re_out[5]'),
		#('FMC_LPC_LA03_N', 'symbol_2x_re_out[6]'),
		#('FMC_LPC_LA04_N', 'symbol_2x_re_out[7]'),
		#('FMC_LPC_LA07_P', 'symbol_2x_re_out[8]'),
		#('FMC_LPC_LA08_P', 'symbol_2x_re_out[9]'),
		#('FMC_LPC_LA01_CC_P', 'symbol_2x_re_out[10]'),
		#('FMC_LPC_LA01_CC_N', 'symbol_2x_re_out[11]'),
		#('FMC_LPC_LA06_P', 'symbol_2x_re_out[12]'),
		#('FMC_LPC_LA06_N', 'symbol_2x_re_out[13]'),
		#('FMC_LPC_LA05_P', 'symbol_2x_re_out[14]'),
		#('FMC_LPC_LA05_N', 'symbol_2x_re_out[15]'),

		#('FMC_LPC_LA10_N', 'symbol_2x_im_out[0]'),
		#('FMC_LPC_LA09_P', 'symbol_2x_im_out[1]'),
		#('FMC_LPC_LA09_N', 'symbol_2x_im_out[2]'),
		#('FMC_LPC_LA13_P', 'symbol_2x_im_out[3]'),
		#('FMC_LPC_LA14_P', 'symbol_2x_im_out[4]'),
		#('FMC_LPC_LA13_N', 'symbol_2x_im_out[5]'),
		#('FMC_LPC_LA14_N', 'symbol_2x_im_out[6]'),
		#('FMC_LPC_LA07_N', 'symbol_2x_im_out[7]'),
		#('FMC_LPC_LA08_N', 'symbol_2x_im_out[8]'),
		#('FMC_LPC_LA12_P', 'symbol_2x_im_out[9]'),
		#('FMC_LPC_LA11_P', 'symbol_2x_im_out[10]'),
		#('FMC_LPC_LA12_N', 'symbol_2x_im_out[11]'),
		#('FMC_LPC_LA11_N', 'symbol_2x_im_out[12]'),
		#('FMC_LPC_LA16_P', 'symbol_2x_im_out[13]'),
		#('FMC_LPC_LA16_N', 'symbol_2x_im_out[14]'),
		#('FMC_LPC_LA15_P', 'symbol_2x_im_out[15]'),

		#('FMC_LPC_LA22_N', 'clk_out2'),
		#('FMC_LPC_LA21_P', 'clk_out3'),

		#('FMC_LPC_LA20_P', 'clk_out4'),

		('FMC_LPC_LA32_N', 'asi_out_p'),
		('FMC_LPC_LA33_N', 'asi_out_n'),

		#('FMC_LPC_CLK0_M2C_P', 'fs_0p5_en'),

		##('XADC_GPIO_0', 'clk_out1'),
		##('USER_SMA_GPIO_P', 'asi_out'),
		##('LCD_DB4_LS', 'asi_out'),
		##('GPIO_SW_E', 'asi_out'),
		#('LCD_E_LS', 'lcm_din'),
		#('LCD_RS_LS', 'lcm_lp'),
		#('LCD_RW_LS', 'lcm_xscl'),
		#('XADC_GPIO_0', 'lcm_data[0]'),
		#('XADC_GPIO_1', 'lcm_data[1]'),
		#('XADC_GPIO_2', 'lcm_data[2]'),
		#('XADC_GPIO_3', 'lcm_data[3]'),
		#('LCD_DB4_LS', 'lcm_data[4]'),
		#('LCD_DB5_LS', 'lcm_data[5]'),
		#('LCD_DB6_LS', 'lcm_data[6]'),
		#('LCD_DB7_LS', 'lcm_data[7]'),
	]

	return list_net_port

def map_port_property_multi_tsp():
	map_port_property = {
		'mpeg_clk': ['CLOCK_DEDICATED_ROUTE FALSE'],
		'mpeg_clk_1': ['CLOCK_DEDICATED_ROUTE FALSE'],
		'mpeg_clk_2': ['CLOCK_DEDICATED_ROUTE FALSE'],
		'mpeg_clk_3': ['CLOCK_DEDICATED_ROUTE FALSE'],
	}

	return map_port_property

def list_net_port_multi_tsp():
	list_net_port = [
		#j94
		('FMC_HPC_HA00_CC_P', 'mpeg_clk'),#5
		('FMC_HPC_HA01_CC_P', 'mpeg_sync'),#6
		('FMC_HPC_HA05_N', 'mpeg_valid'),#18
		('FMC_HPC_HA00_CC_N', 'mpeg_data[0]'),#7
		('FMC_HPC_HA01_CC_N', 'mpeg_data[1]'),#8
		('FMC_HPC_HA02_P', 'mpeg_data[2]'),#9
		('FMC_HPC_HA04_P', 'mpeg_data[3]'),#13
		('FMC_HPC_HA03_N', 'mpeg_data[4]'),#12
		('FMC_HPC_HA04_N', 'mpeg_data[5]'),#17
		('FMC_HPC_HA05_P', 'mpeg_data[6]'),#14
		('FMC_HPC_HA06_P', 'mpeg_data[7]'),#19

		('FMC_HPC_HA10_P', 'asi_out_p'),#29
		('FMC_HPC_HA10_N', 'asi_out_n'),#31
		
		#j95
		('FMC_HPC_HA15_P', 'mpeg_clk_1'),#5
		('FMC_HPC_HA16_P', 'mpeg_sync_1'),#6
		('FMC_HPC_HA20_N', 'mpeg_valid_1'),#18
		('FMC_HPC_HA15_N', 'mpeg_data_1[0]'),#7
		('FMC_HPC_HA16_N', 'mpeg_data_1[1]'),#8
		('FMC_HPC_HA17_CC_P', 'mpeg_data_1[2]'),#9
		('FMC_HPC_HA19_P', 'mpeg_data_1[3]'),#13
		('FMC_HPC_HA18_N', 'mpeg_data_1[4]'),#12
		('FMC_HPC_HA19_N', 'mpeg_data_1[5]'),#17
		('FMC_HPC_HA20_P', 'mpeg_data_1[6]'),#14
		('FMC_HPC_HA21_P', 'mpeg_data_1[7]'),#19

		('FMC_HPC_LA29_P', 'asi_out_p_1'),#29
		('FMC_HPC_LA29_N', 'asi_out_n_1'),#31

		#j96
		('FMC_HPC_CLK1_M2C_P', 'mpeg_clk_2'),#5
		('FMC_HPC_CLK0_M2C_P', 'mpeg_sync_2'),#6
		('FMC_HPC_LA03_N', 'mpeg_valid_2'),#18
		('FMC_HPC_CLK1_M2C_N', 'mpeg_data_2[0]'),#7
		('FMC_HPC_CLK0_M2C_N', 'mpeg_data_2[1]'),#8
		('FMC_HPC_LA00_CC_P', 'mpeg_data_2[2]'),#9
		('FMC_HPC_LA02_P', 'mpeg_data_2[3]'),#13
		('FMC_HPC_LA01_CC_N', 'mpeg_data_2[4]'),#12
		('FMC_HPC_LA02_N', 'mpeg_data_2[5]'),#17
		('FMC_HPC_LA03_P', 'mpeg_data_2[6]'),#14
		('FMC_HPC_LA04_P', 'mpeg_data_2[7]'),#19

		('FMC_HPC_LA08_P', 'asi_out_p_2'),#29
		('FMC_HPC_LA08_N', 'asi_out_n_2'),#31
		
		#j97
		('FMC_HPC_LA13_P', 'mpeg_clk_3'),#5
		('FMC_HPC_LA14_P', 'mpeg_sync_3'),#6
		('FMC_HPC_LA18_CC_N', 'mpeg_valid_3'),#18
		('FMC_HPC_LA13_N', 'mpeg_data_3[0]'),#7
		('FMC_HPC_LA14_N', 'mpeg_data_3[1]'),#8
		('FMC_HPC_LA15_P', 'mpeg_data_3[2]'),#9
		('FMC_HPC_LA17_CC_P', 'mpeg_data_3[3]'),#13
		('FMC_HPC_LA16_N', 'mpeg_data_3[4]'),#12
		('FMC_HPC_LA17_CC_N', 'mpeg_data_3[5]'),#17
		('FMC_HPC_LA18_CC_P', 'mpeg_data_3[6]'),#14
		('FMC_HPC_LA19_P', 'mpeg_data_3[7]'),#19

		('FMC_HPC_LA23_P', 'asi_out_p_3'),#29
		('FMC_HPC_LA23_N', 'asi_out_n_3'),#31
	]

	return list_net_port

#s:('.*', \('.*'\)),\#\(.*\):\2 \: \1,:gc
def list_pin_port_multi_tsp():
	list_pin_port = []

	list_slot_list_portnum_port = [
		(
			'J94',
			[
				(5, 'mpeg_clk'),
				(6, 'mpeg_sync'),
				(18, 'mpeg_valid'),
				(7, 'mpeg_data[0]'),
				(8, 'mpeg_data[1]'),
				(9, 'mpeg_data[2]'),
				(13, 'mpeg_data[3]'),
				(12, 'mpeg_data[4]'),
				(17, 'mpeg_data[5]'),
				(14, 'mpeg_data[6]'),
				(19, 'mpeg_data[7]'),

				(29, 'asi_out_p'),
				(31, 'asi_out_n'),
			]
		),
		(
			'J95',
			[
				(5, 'mpeg_clk_1'),
				(6, 'mpeg_sync_1'),
				(18, 'mpeg_valid_1'),
				(7, 'mpeg_data_1[0]'),
				(8, 'mpeg_data_1[1]'),
				(9, 'mpeg_data_1[2]'),
				(13, 'mpeg_data_1[3]'),
				(12, 'mpeg_data_1[4]'),
				(17, 'mpeg_data_1[5]'),
				(14, 'mpeg_data_1[6]'),
				(19, 'mpeg_data_1[7]'),

				(29, 'asi_out_p_1'),
				(31, 'asi_out_n_1'),
			]
			),
		(
		'J96',
			[
				(5, 'mpeg_clk_2'),
				(6, 'mpeg_sync_2'),
				(18, 'mpeg_valid_2'),
				(7, 'mpeg_data_2[0]'),
				(8, 'mpeg_data_2[1]'),
				(9, 'mpeg_data_2[2]'),
				(13, 'mpeg_data_2[3]'),
				(12, 'mpeg_data_2[4]'),
				(17, 'mpeg_data_2[5]'),
				(14, 'mpeg_data_2[6]'),
				(19, 'mpeg_data_2[7]'),

				(29, 'asi_out_p_2'),
				(31, 'asi_out_n_2'),
			]
		),
		(
			'J97',
			[
				(5, 'mpeg_clk_3'),
				(6, 'mpeg_sync_3'),
				(18, 'mpeg_valid_3'),
				(7, 'mpeg_data_3[0]'),
				(8, 'mpeg_data_3[1]'),
				(9, 'mpeg_data_3[2]'),
				(13, 'mpeg_data_3[3]'),
				(12, 'mpeg_data_3[4]'),
				(17, 'mpeg_data_3[5]'),
				(14, 'mpeg_data_3[6]'),
				(19, 'mpeg_data_3[7]'),

				(29, 'asi_out_p_3'),
				(31, 'asi_out_n_3'),
			]
		),
	]

	map_slot_map_portnum_pin = get_newboard_map_slot_map_portnum_pin()

	for slot, list_portnum_port in list_slot_list_portnum_port:
		map_portnum_pin = map_slot_map_portnum_pin.get(slot, None)
		if not map_portnum_pin:
			continue
		for portnum, port in list_portnum_port:
			pin = map_portnum_pin.get(portnum, None)
			if not pin:
				continue
			item = (pin, port)
			list_pin_port.append(item)
	
	return list_pin_port
	

def get_list_ip_net_pin_port_des(map_kc705_pin_net):
	list_ip_net_pin_port_des = []

	map_port_property = {}
	list_net_port = []
	map_net_property = {}
	list_pin_port = []

	#map_port_property = map_port_property_new_tsp_board_j94()
	#list_net_port = list_net_port_new_tsp_board_j94()

	#map_port_property = map_port_property_old_tsp_board_2ab42e394123204b24255388e7e131aab67b6328()
	#list_net_port = list_net_port_old_tsp_board_2ab42e394123204b24255388e7e131aab67b6328()

	map_port_property = map_port_property_multi_tsp()
	list_pin_port = list_pin_port_multi_tsp()
	#list_net_port = list_net_port_multi_tsp()

	for pin, port in list_pin_port:
		list_extra_des = []
		list_property = map_port_property.get(port, None)
		if list_property:
			for i in list_property:
				list_extra_des.append('set_property %s [get_nets {%s}]' %(i, port))

		net = map_kc705_pin_net.pop(pin, None)
		if net:
			item = (net, pin, port, list_extra_des)
			list_ip_net_pin_port_des.append(item)
		else:
			print '(%s, %s) is not in map_kc705_pin_net!' %(pin, port)
	
	for net, port in list_net_port:
		list_extra_des = []

		list_property = map_port_property.get(port)
		if list_property:
			for i in list_property:
				list_extra_des.append('set_property %s [get_nets {%s}]' %(i, port))

		for i, j in map_kc705_pin_net.items():
			if j == net:
				pin = i
				map_kc705_pin_net.pop(pin, None)

				item = (net, pin, port, list_extra_des)
				list_ip_net_pin_port_des.append(item)

	print '-' * 100
	print 'list_ip_net_pin_port_des info'
	print '-' * 100
	for i in list_ip_net_pin_port_des:
		print i
	print 'total:', len(list_ip_net_pin_port_des)

	return list_ip_net_pin_port_des

def list_pin_des_new_i2s_board():
	list_pin_des = [
		('AD26', 'SOMI'),
		('AC26', 'MOSI'),
		('AE25', 'SCLK'),
		('AF25', '74138GA(CS)'),
		('AD21', '74138GB'),
		('AD24', '74138GC'),
		('AJ24', 'SPI_S0'),
		('AK25', 'SPI_S1'),
		('AJ22', 'SPI_S2'),
		('AJ23', 'SPI_S3'),
	]

	return list_pin_des

def list_pin_des_new_tsp_board_j94():
	list_pin_des = [
		('C12', 'i2c_sck'),
		('C11', 'i2c_sda'),

		#('A23', 'spi_clk'),
		#('D23', 'spi_mosi'),
		#('E25', 'spi_miso'),

		#('F26', '74138G2A'),
		#('E23', 'spi_s0'),
		#('F25', 'spi_s1'),
		#('E24', 'spi_s2'),

		('C14', 'lnb1_on_off'),
		('E14', 'TUNB_3.3V_ON'),
		#('AF27', 'AD9125_INTB'),
		#('AH29', 'AD5375_DSOP'),

		('E15', 'undefined'),
		('C15', 'undefined'),
		('B15', 'undefined'),
		('J16', 'undefined'),
		('B14', 'undefined'),
		('A15', 'undefined'),
		('F12', 'undefined'),
		('E13', 'undefined'),
		('B13', 'undefined'),
		('A13', 'undefined'),
		('L16', 'undefined'),
		('K16', 'undefined'),
		('H16', 'undefined'),
	]

	return list_pin_des

def list_net_des_new_tsp_board_j94():
	list_net_des = [
		('FMC_HPC_HA03_P', 'i2c_sck'),
		('FMC_HPC_HA02_N', 'i2c_sda'),

		#('FMC_LPC_LA21_N', 'spi_clk'),
		#('FMC_LPC_LA19_P', 'spi_mosi'),
		#('FMC_LPC_LA19_N', 'spi_miso'),

		#('FMC_LPC_LA22_P', '74138G2A'),
		#('FMC_LPC_LA15_N', 'spi_s0'),
		#('FMC_LPC_CLK0_M2C_N', 'spi_s1'),
		#('FMC_LPC_PRSNT_M2C_B_LS', 'spi_s2'),

		#('FMC_HPC_HA06_N', 'lnb1_on_off'),
		#('FMC_HPC_HA08_P', 'TUNB_3.3V_ON'),
		#('FMC_LPC_LA20_N', 'AD9125_INTB'),
		#('FMC_LPC_CLK1_M2C_N', 'AD5375_DSOP'),

		#('FMC_HPC_HA08_N', 'undefined'),
		#('FMC_HPC_HA12_P', 'undefined'),
		#('FMC_HPC_HA12_N', 'undefined'),
		#('FMC_HPC_HA14_P', 'undefined'),
		#('FMC_HPC_HA07_P', 'undefined'),
		#('FMC_HPC_HA07_N', 'undefined'),
		#('FMC_HPC_HA09_P', 'undefined'),
		#('FMC_HPC_HA09_N', 'undefined'),
		#('FMC_HPC_HA11_P', 'undefined'),
		#('FMC_HPC_HA11_N', 'undefined'),
		#('FMC_HPC_HA13_P', 'undefined'),
		#('FMC_HPC_HA13_N', 'undefined'),
		#('FMC_HPC_HA14_N', 'undefined'),
	]
	
	return list_net_des

def list_net_des_new_tsp_board_j97():
	list_net_des = [
		('FMC_HPC_LA16_P', 'i2c_sck'),
		('FMC_HPC_LA15_N', 'i2c_sda'),

		#('FMC_HPC_LA19_N', 'lnb1_on_off'),
		#('FMC_HPC_LA21_P', 'TUNB_3.3V_ON'),

		#('FMC_HPC_LA21_N', 'undefined'),
		#('FMC_HPC_LA25_P', 'undefined'),
		#('FMC_HPC_LA25_N', 'undefined'),
		#('FMC_HPC_LA27_P', 'undefined'),
		#('FMC_HPC_LA20_P', 'undefined'),
		#('FMC_HPC_LA20_N', 'undefined'),
		#('FMC_HPC_LA22_P', 'undefined'),
		#('FMC_HPC_LA22_N', 'undefined'),
		#('FMC_HPC_LA24_P', 'undefined'),
		#('FMC_HPC_LA24_N', 'undefined'),
		#('FMC_HPC_LA26_P', 'undefined'),
		#('FMC_HPC_LA26_N', 'undefined'),
		#('FMC_HPC_LA27_N', 'undefined'),
	]

	return list_net_des

def list_net_des_iic_slave():
	list_net_des = [
		('FMC_HPC_LA30_P', 'master_scl'),
		('FMC_HPC_LA24_P', 'master_sda'),
	]

	return list_net_des

def list_net_des_old_tsp_board_2ab42e394123204b24255388e7e131aab67b6328():
	list_net_des = [
		('FMC_LPC_LA30_N', 'i2c_sck'),
		('FMC_LPC_LA30_P', 'i2c_sda'),
		#('FMC_LPC_LA23_P', 'spi_clk'),
		#('FMC_LPC_LA23_N', 'spi_mosi'),
		#('FMC_LPC_LA20_N', 'spi_miso'),
		#('FMC_LPC_LA32_P', 'spi_cs'),
	]

	return list_net_des

def list_net_des_multi_tsp():
	list_net_des = [
		#j94
		('FMC_HPC_HA03_P', 'i2c_sck'),#10
		('FMC_HPC_HA02_N', 'i2c_sda'),#11
		#j95
		('FMC_HPC_HA18_P', 'i2c_sck_1'),#10
		('FMC_HPC_HA17_CC_N', 'i2c_sda_1'),#11
		#j96
		('FMC_HPC_LA01_CC_P', 'i2c_sck_2'),#10
		('FMC_HPC_LA00_CC_N', 'i2c_sda_2'),#11
		#j97
		('FMC_HPC_LA16_P', 'i2c_sck_3'),#10
		('FMC_HPC_LA15_N', 'i2c_sda_3'),#11
	]

	return list_net_des

def get_map_gpio_if_list_net_pin_des_resistor(map_kc705_pin_net, list_kc705_net_group_part_pin, list_fmc_pin_resistor):
	map_gpio_if_list_net_pin_des_resistor = {}
	map_gpio_if_list_net_pin_des_resistor.update({'HPC': []})
	map_gpio_if_list_net_pin_des_resistor.update({'LPC': []})
	map_gpio_if_list_net_pin_des_resistor.update({'OTHER': []})

	list_pin_des = []
	list_net_des = []
	
	#list_net_des = list_net_des_new_tsp_board_j94()
	#list_net_des = list_net_des_old_tsp_board_2ab42e394123204b24255388e7e131aab67b6328()
	list_net_des = list_net_des_multi_tsp()

	for pin, des in list_pin_des:
		net = map_kc705_pin_net.pop(pin, None)
		if net:
			resistor = 'undefined'
			for i, group, part, j in list_kc705_net_group_part_pin:
				if net == i:
					if group in ['J2', 'J22']:
						for k, l in list_fmc_pin_resistor:
							if j == k:
								resistor = l
			v = (net, pin, des, resistor)
			if net.startswith('FMC_HPC'):
				map_gpio_if_list_net_pin_des_resistor.get('HPC').append(v)
			elif net.startswith('FMC_LPC'):
				map_gpio_if_list_net_pin_des_resistor.get('LPC').append(v)
			else:
				map_gpio_if_list_net_pin_des_resistor.get('OTHER').append(v)


	for net, des in list_net_des:
		for i, j in map_kc705_pin_net.items():
			if j == net:
				map_kc705_pin_net.pop(i, None)
				resistor = 'undefined'
				pin = i
				for k, group, part, l in list_kc705_net_group_part_pin:
					if net == k:
						if group in ['J2', 'J22']:
							for m, n in list_fmc_pin_resistor:
								if l == m:
									resistor = n
				v = (net, pin, des, resistor)
				if net.startswith('FMC_HPC'):
					map_gpio_if_list_net_pin_des_resistor.get('HPC').append(v)
				elif net.startswith('FMC_LPC'):
					map_gpio_if_list_net_pin_des_resistor.get('LPC').append(v)
				else:
					map_gpio_if_list_net_pin_des_resistor.get('OTHER').append(v)

	#for pin, net in map_kc705_pin_net.items():
	#	des = 'undefined'
	#	net = map_kc705_pin_net.pop(pin, None)
	#	if net:
	#		resistor = 'undefined'
	#		for i, group, part, j in list_kc705_net_group_part_pin:
	#			if net == i:
	#				if group in ['J2', 'J22']:
	#					for k, l in list_fmc_pin_resistor:
	#						if j == k:
	#							resistor = l
	#		v = (net, pin, des, resistor)
	#		if net.startswith('FMC_HPC'):
	#			map_gpio_if_list_net_pin_des_resistor.get('HPC').append(v)
	#		elif net.startswith('FMC_LPC'):
	#			map_gpio_if_list_net_pin_des_resistor.get('LPC').append(v)
	#		else:
	#			map_gpio_if_list_net_pin_des_resistor.get('OTHER').append(v)

	for i in map_gpio_if_list_net_pin_des_resistor.items():
		print '-' * 100
		print 'map_gpio_if_list_net_pin_des_resistor %s info' %(i[0])
		print '-' * 100
		for j in i[1]:
			print j
		print 'total:', len(i[1])

	#map_gpio_if_list_net_pin_des_resistor.pop('OTHER', None)

	return map_gpio_if_list_net_pin_des_resistor

def gen_default_contrain():
	txt = """
# Sys Clock Pins
#set_property PACKAGE_PIN AD11 [get_ports MIG_SYS_CLK_clk_n]
#set_property IOSTANDARD DIFF_SSTL15 [get_ports MIG_SYS_CLK_clk_n]

#set_property PACKAGE_PIN AD12 [get_ports MIG_SYS_CLK_clk_p]
#set_property IOSTANDARD DIFF_SSTL15 [get_ports MIG_SYS_CLK_clk_p]

# Sys Reset Pins
set_property PACKAGE_PIN AB7 [get_ports reset]
set_property IOSTANDARD LVCMOS15 [get_ports reset]

# PCIe Refclk Pins
set_property PACKAGE_PIN U8 [get_ports EXT_PCIE_REFCLK_P]
set_property PACKAGE_PIN U7 [get_ports EXT_PCIE_REFCLK_N]

# PCIe TX RX Pins
#set_property PACKAGE_PIN M6 [get_ports {EXT_PCIE_rxp[0]}]
#set_property PACKAGE_PIN M5 [get_ports {EXT_PCIE_rxn[0]}]
#set_property PACKAGE_PIN P6 [get_ports {EXT_PCIE_rxp[1]}]
#set_property PACKAGE_PIN P5 [get_ports {EXT_PCIE_rxn[1]}]
#set_property PACKAGE_PIN R4 [get_ports {EXT_PCIE_rxp[2]}]
#set_property PACKAGE_PIN R3 [get_ports {EXT_PCIE_rxn[2]}]
#set_property PACKAGE_PIN T6 [get_ports {EXT_PCIE_rxp[3]}]
#set_property PACKAGE_PIN T5 [get_ports {EXT_PCIE_rxn[3]}]
#set_property PACKAGE_PIN L4 [get_ports {EXT_PCIE_txp[0]}]
#set_property PACKAGE_PIN L3 [get_ports {EXT_PCIE_txn[0]}]
#set_property PACKAGE_PIN M2 [get_ports {EXT_PCIE_txp[1]}]
#set_property PACKAGE_PIN M1 [get_ports {EXT_PCIE_txn[1]}]
#set_property PACKAGE_PIN N4 [get_ports {EXT_PCIE_txp[2]}]
#set_property PACKAGE_PIN N3 [get_ports {EXT_PCIE_txn[2]}]
#set_property PACKAGE_PIN P2 [get_ports {EXT_PCIE_txp[3]}]
#set_property PACKAGE_PIN P1 [get_ports {EXT_PCIE_txn[3]}]

# LED Pins
set_property PACKAGE_PIN AB8 [get_ports {EXT_LEDS[0]}]
set_property IOSTANDARD LVCMOS15 [get_ports {EXT_LEDS[0]}]

set_property PACKAGE_PIN AA8 [get_ports {EXT_LEDS[1]}]
set_property IOSTANDARD LVCMOS15 [get_ports {EXT_LEDS[1]}]

set_property PACKAGE_PIN AC9 [get_ports {EXT_LEDS[2]}]
set_property IOSTANDARD LVCMOS15 [get_ports {EXT_LEDS[2]}]

set_property PACKAGE_PIN AB9 [get_ports {EXT_LEDS[3]}]
set_property IOSTANDARD LVCMOS15 [get_ports {EXT_LEDS[3]}]

set_property PACKAGE_PIN AE26 [get_ports {EXT_LEDS[4]}]
set_property IOSTANDARD LVCMOS25 [get_ports {EXT_LEDS[4]}]

set_property PACKAGE_PIN G19 [get_ports {EXT_LEDS[5]}]
set_property IOSTANDARD LVCMOS25 [get_ports {EXT_LEDS[5]}]

set_property PACKAGE_PIN E18 [get_ports {EXT_LEDS[6]}]
set_property IOSTANDARD LVCMOS25 [get_ports {EXT_LEDS[6]}]

set_property PACKAGE_PIN F16 [get_ports {EXT_LEDS[7]}]
set_property IOSTANDARD LVCMOS25 [get_ports {EXT_LEDS[7]}]
	"""

	print '#', '-' * 100
	print '#', 'kc705 default constrain'
	print '#', '-' * 100
	print txt

def gen_ip_constrain(list_ip_net_pin_port_des):
	print '#', '-' * 100
	print '#', 'ip constrain'
	print '#', '-' * 100

	for net, pin, port, des in list_ip_net_pin_port_des:
		print '\n#%s\nset_property PACKAGE_PIN %s [get_ports {%s}]' %(net, pin, port)
		print 'set_property IOSTANDARD LVCMOS25 [get_ports {%s}]' %(port)
		if des:
			for i in des:
				print i

def gen_gpio_constrain(map_gpio_if_list_net_pin_des_resistor):
	list_net_pin_des_resistor_gpio_gpio_no = []
	start = 0
	top_pin_no = 256
	#top_pin_no = 180
	gpio_no = 0

	list_gpio_groups = [
		'gpio_tri_io',
		'gpio2_tri_io',
		'gpio_1_tri_io',
		'gpio2_1_tri_io',
		'gpio_2_tri_io',
		'gpio2_2_tri_io',
		'gpio_3_tri_io',
		'gpio2_3_tri_io',
		'gpio_4_tri_io',
		'gpio2_4_tri_io',
	]

	list_gpio_ports = []
	for i in list_gpio_groups:
		for j in range(32):
			list_gpio_ports.append(i + '[' + str(j) + ']')

	print '#', '-' * 100
	print '#', 'gpio constrain'
	print '#', '-' * 100

	common_list_net_pin_des_resistor = []
	for i, j in map_gpio_if_list_net_pin_des_resistor.items():
		common_list_net_pin_des_resistor.extend(j)
	map_common_list_net_pin_des_resistor = {}
	map_common_list_net_pin_des_resistor.update({'common gpio' : common_list_net_pin_des_resistor})

	#for i, j in map_gpio_if_list_net_pin_des_resistor.items():
	for i, j in map_common_list_net_pin_des_resistor.items():
		list_len = len(j)

		if list_len == 0:
			continue

		list_if_gpio_ports = list_gpio_ports[start : ]

		if len(list_if_gpio_ports) < list_len:
			#print , "gpio bank is not enough!"
			continue

		#print '#', '-' * 100
		#print '#', 'gpio constrain for %s' %(i)
		#print '#', '-' * 100

		base_pin_no = 0

		for k in range(list_len):
			bank = k / 32
			bank_gpio_num = 32 if (list_len - bank * 32 >= 32) else list_len - bank * 32
			base_pin_no = top_pin_no - bank * 32 - bank_gpio_num
			gpio_no = base_pin_no + k % 32
			net, pin, des, resistor = j[k]
			gpio = list_if_gpio_ports[k]
			item = (net, pin, des, resistor, gpio, gpio_no)
			list_net_pin_des_resistor_gpio_gpio_no.append(item)
			print '\n#%s, %s, %s, %d\nset_property PACKAGE_PIN %s [get_ports {%s}]' %(net, des, resistor, gpio_no, pin, gpio)
			print 'set_property IOSTANDARD LVCMOS25 [get_ports {%s}]' %(gpio)

		top_pin_no = base_pin_no

		start += list_len
		#if (start % 32) != 0:
		#	start = 32 * ((start / 32) + 1)

	return list_net_pin_des_resistor_gpio_gpio_no

def gen_bitstream_constrain():
	txt = """
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 40 [current_design]
set_property BITSTREAM.CONFIG.SPI_FALL_EDGE YES [current_design]

##Encryption Settings
#set_property BITSTREAM.ENCRYPTION.ENCRYPT YES [current_design]
#set_property BITSTREAM.ENCRYPTION.ENCRYPTKEYSELECT BBRAM [current_design]
##set_property BITSTREAM.ENCRYPTION.ENCRYPTKEYSELECT eFUSE [current_design]
#set_property BITSTREAM.ENCRYPTION.KEY0 256'h12345678ABCDDCBA1234578ABCDDCBA1234578ABCDDCBA1234578ABCDDCBA [current_design]
	"""

	print '#', '-' * 100
	print '#', 'bitstream constrain'
	print '#', '-' * 100
	print txt

def gen_gpio_test_list(list_net_pin_des_resistor_gpio_gpio_no):
	fmc_board_pins = '''
	149 148 147 146 145 144 143 142 141 140 139 138
	84 83 137 136 135 134 133 132 131 130 129 128 127 126
	61 59 82 81 80 79 78 77 75 73 71 69 67 65 63
	86 53 58 57 56 55 54 76 74 72 70 68 66 64 62
	52 51 49 50 47 48 46 45 44 43 42 41 40 39 38
	85 60 125 124 123 122 121 120 119 118 117 116 115 114 113
	112 111 110 109 108 107 106 105 104 103 102 101 3 19 18 4
	37 36 35 34 33 32 31 30 29 28 27 26 25 24 5
	16 15 14 13 12 11 10 9 8 7 23 22 21 20 6 17
	98 97 96 95 94 93 99 100 92 91 90 89 88 87 1 2
	'''
	list_resistor_no = []
	l = fmc_board_pins.strip().splitlines()
	for i in l:
		for j in i.split():
			list_resistor_no.append(j)
	

	print '#', '-' * 100
	print '#', 'test fmc data'
	print '#', '-' * 100

	list_test_gpio_resistor_net = []

	for no in list_resistor_no:
		for net, pin, des, resistor, gpio, gpio_no in list_net_pin_des_resistor_gpio_gpio_no:
			if net.startswith('FMC_HPC'):
				pattern = re.compile(r'([^\d]+)(\d+)')
				g = pattern.match(resistor)
				if g:
					r, i = g.groups()
					if no == i:
						item = (gpio_no, resistor, net)
						list_test_gpio_resistor_net.append(item)

	for no in list_resistor_no:
		for net, pin, des, resistor, gpio, gpio_no in list_net_pin_des_resistor_gpio_gpio_no:
			if net.startswith('FMC_LPC'):
				pattern = re.compile(r'([^\d]+)(\d+)')
				g = pattern.match(resistor)
				if g:
					r, i = g.groups()
					if no == i:
						item = (gpio_no, resistor, net)
						list_test_gpio_resistor_net.append(item)

	for gpio_no, resistor, net in list_test_gpio_resistor_net:
		print "%s\t%s\t%s" %(gpio_no, resistor, net)

def gen_kc705_constrain():
	list_kc705_net_group_part_pin = gen_list_kc705_net_group_part_pin()

	list_fmc_pin_resistor = gen_list_fmc_pin_resistor()

	map_kc705_pin_net = gen_map_kc705_pin_net()

	map_kc705_pin_iotype = gen_map_kc705_pin_iotype()

	remove_unused_pin(map_kc705_pin_net)

	list_ip_net_pin_port_des = get_list_ip_net_pin_port_des(map_kc705_pin_net)

	map_gpio_if_list_net_pin_des_resistor = get_map_gpio_if_list_net_pin_des_resistor(map_kc705_pin_net, list_kc705_net_group_part_pin, list_fmc_pin_resistor)
	gen_default_contrain()

	gen_ip_constrain(list_ip_net_pin_port_des)

	list_net_pin_des_resistor_gpio_gpio_no = gen_gpio_constrain(map_gpio_if_list_net_pin_des_resistor)

	gen_bitstream_constrain()

	gen_gpio_test_list(list_net_pin_des_resistor_gpio_gpio_no)

if __name__ == "__main__":
	gen_kc705_constrain()
