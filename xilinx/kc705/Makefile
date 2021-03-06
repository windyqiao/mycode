export BUILD_KO=$(shell pwd)/driver/build_kernel_modules.mk

#export SUBJECT := DVBS2
#export SUBJECT := KC705_CSA
#export SUBJECT := KC705_CSA_DEBUG
#export SUBJECT := KC705_FMC_GPIO
#export SUBJECT := KC705_I2S_RECEIVER
#export SUBJECT := KC705_IIC_SLAVE
#export SUBJECT := KC705_DVBS2
#export SUBJECT := KC705_TSP


ifeq ($(SUBJECT), DVBS2)
	NEED_I2C := YES
	NEED_SPI := YES
else ifeq ($(SUBJECT), KC705_I2S_RECEIVER)
	NEED_SPI := YES
else ifeq ($(SUBJECT), KC705_IIC_SLAVE)
	NEED_I2C := YES
else ifeq ($(SUBJECT), KC705_DVBS2)
	NEED_I2C := YES
	NEED_SPI := YES
else ifeq ($(SUBJECT), KC705_TSP)
	NEED_I2C := YES
endif

app_target := app/kc705_device \
		app/tsp_dma \
		app/asi_dma \
		app/i2s_dma \
		app/i2s_spi_dev \
		app/tsp_regs \
		app/dvbs2_regs \
		app/iic_slave \
		app/csa_dma \
		app/csa_reg \
		app/csa_debug_dma \
		app/csa_debug_reg

all : $(app_target)
	make -C driver

% : %.c app/utils.c
	gcc -Idriver -o $@ $^ -pthread

clean : clean-app clean-driver

clean-app :
	-rm $(app_target)

clean-driver :
	make -C driver clean

install:
	sudo insmod driver/kc705-module.ko

ifeq ($(NEED_I2C), YES)
	sudo insmod driver/i2c-gpio.ko
	sudo insmod driver/kc705_i2c_master.ko
	sudo insmod driver/i2c-dev.ko
endif

ifeq ($(NEED_SPI), YES)
	sudo insmod driver/spi-gpio-all.ko
	sudo insmod driver/kc705_spi_master.ko
	sudo insmod driver/spidev.ko
	sudo insmod driver/kc705_spi_device.ko
endif

	dmesg

uninstall:
#	make start_dma

ifeq ($(NEED_SPI), YES)
	-sudo rmmod kc705_spi_device
	-sudo rmmod spidev
	-sudo rmmod spi_bitbang
	-sudo rmmod kc705_spi_master
	-sudo rmmod spi_gpio_all
endif

ifeq ($(NEED_I2C), YES)
	-sudo rmmod i2c-dev
	-sudo rmmod kc705_i2c_master
	-sudo rmmod i2c_gpio
endif

	-sudo rmmod kc705-module

	sudo dmesg -c

start_dma:
	sudo dmesg -c
	sudo ./app/kc705_device /dev/kc705_pcie start 

stop_dma:
	sudo dmesg -c
	sudo ./app/kc705_device /dev/kc705_pcie stop

test:
	while true;do make start_dma; sleep 3; make stop_dma; sleep 3;done
