/**
 *  This is a simple demon of uio driver.
 *  Last modified by 
 09-05-2011   Joseph Yang(Yang Honggang)<ganggexiongqi@gmail.com>
 *
 * Compile:  
 *   Save this file name it simple.c
 *   # echo "obj-m := simple.o" > Makefile
 *   # make -Wall -C /lib/modules/`uname -r`/build M=`pwd` modules
 * Load the module:
 *   #modprobe uio
 *   #insmod simple.ko
 */

#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/slab.h> /* kmalloc, kfree */
#include <linux/i2c.h>
#include <linux/i2c-gpio.h>
#define MY_NAME "kc705_i2c"

#define SDA0 158 //FMC_LPC_LA30_P
#define SCL0 157 //FMC_LPC_LA30_N
#define I2C_BUS_NUM (-1)

static struct i2c_gpio_platform_data i2c_gpio_data = {
	.sda_pin		= SDA0,
	.scl_pin		= SCL0,
	.sda_is_open_drain	= 0,
	.scl_is_open_drain	= 0,
	.udelay			= 10,
	.scl_is_output_only	= 1,
};

void gpio_free(unsigned gpio);
static void release_gpio(struct device *dev) {
	struct i2c_gpio_platform_data *data = dev->platform_data;
	gpio_free(data->sda_pin);
	gpio_free(data->scl_pin);
}

static struct platform_device i2c_gpio_device = {
	.name		= "i2c-gpio",
	.id		= I2C_BUS_NUM,
	.dev		= {
		.platform_data	= &i2c_gpio_data,
		.release = release_gpio,
	},
};

static int __init kc705_i2c_master_init(void)
{
	int ret = 0;
	printk("%s\n", __PRETTY_FUNCTION__);
	ret = platform_device_register(&i2c_gpio_device);

	return ret;
}

static void __exit kc705_i2c_master_exit(void) {
	printk("%s\n", __PRETTY_FUNCTION__);
	platform_device_unregister(&i2c_gpio_device);
}

module_init(kc705_i2c_master_init);
module_exit(kc705_i2c_master_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("xiaofei");
MODULE_DESCRIPTION("kc705 i2c-gpio platform driver");