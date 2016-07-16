#ifndef _IIC_SLAVE_PCIE_CONFIG_H
#define _IIC_SLAVE_PCIE_CONFIG_H

//Base Address
//regs
#define BASE_AXI_PCIe_CTL 0x81000000
#define BASE_AXI_IIC_SLAVE_LITE_0 0x81001000
#define BASE_AXI_GPIO_LITE_0 0x81002000
#define BASE_Translation_BRAM 0x81009000

//PCIe:BAR0 Address Offset for the accessible Interfaces
#define OFFSET_AXI_PCIe_CTL (BASE_AXI_PCIe_CTL - BASE_AXI_PCIe)
#define OFFSET_AXI_IIC_SLAVE_LITE_0 (BASE_AXI_IIC_SLAVE_LITE_0 - BASE_AXI_PCIe)
#define OFFSET_AXI_GPIO_LITE_0 (BASE_AXI_GPIO_LITE_0 - BASE_AXI_PCIe)
#define OFFSET_Translation_BRAM (BASE_Translation_BRAM - BASE_AXI_PCIe)

#endif//#ifndef _IIC_SLAVE_PCIE_CONFIG_H

