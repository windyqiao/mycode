#include <linux/interrupt.h>
#include <linux/pci.h>
#include <linux/kthread.h>

#include "utils/xiaofei_debug.h"

#include "pcie.h"
#include "dma_common.h"

#define BASE_AXI_CDMA_LITE 0x8100c000
#define OFFSET_AXI_CDMA_LITE (BASE_AXI_CDMA_LITE - BASE_AXI_PCIe)

//AXI CDMA Register Summary
#define CDMA_CR 0x00 //CDMA Control.
#define CDMA_SR 0x04 //CDMA Status.
#define CDMA_CURDESC_PNTR 0x08 //Current Descriptor Pointer.
//#define Reserved 0x0C //N/A
#define CDMA_TAILDESC_PNTR 0x10 //Tail Descriptor Pointer.
//#define Reserved 0x14 //N/A
#define CDMA_SA 0x18 //Source Address.
//#define Reserved 0x1C //N/A
#define CDMA_DA 0x20 //Destination Address.
//#define Reserved 0x24 //N/A
#define CDMA_BTT 0x28 //Bytes to Transfer.

#define SG_DESCRIPTOR_SIZE 0x40

////Transfer Descriptor Word Summary
//#define DES_NXTDESC_PNTR 0x00 //[31:5]
////#define DES_RESERVED 0x04
//#define DES_SA 0x08
////#define DES_RESERVED 0x0c
//#define DES_DA 0x10
////#define DES_RESERVED 0x14
//#define DES_CONTROL 0x18 //[22:0] size to transfer
//#define DES_STATUS 0x1c //bit31:Cmplt bit30:DMADecErr bit29:DMASlvErr bit28:DMAIntErr

typedef union {
	struct {
		uint32_t NXTDESC_PNTR;
		uint32_t PAD0;
		uint32_t SA;
		uint32_t PAD1;
		uint32_t DA;
		uint32_t PAD2;
		uint32_t CONTROL;
		uint32_t STATUS;
	} des;
	unsigned char des_space[0x40];
} kc705_transfer_descriptor_t;

typedef struct {
	struct list_head sg_item;
	kc705_transfer_descriptor_t des;
} kc705_sg_item_info_t;

struct completion cmp;

static LIST_HEAD(sg_descripter_list);
static uint32_t cdma_tail_des_axi_addr;

#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,19)
irqreturn_t isr(int irq, void *dev_id, struct pt_regs *regs)
#else
irqreturn_t isr(int irq, void *dev_id)
#endif
{
	irqreturn_t status = IRQ_NONE;

	struct pci_dev *pdev = dev_id;
	kc705_pci_dev_t *kc705_pci_dev = pci_get_drvdata(pdev);
	uint8_t *base_vaddr;
	uint8_t *cdma_base_vaddr;
	uint32_t value;

	if(kc705_pci_dev == NULL) {
		mydebug("\n");
		return status;
	}
	base_vaddr = kc705_pci_dev->bar_info[0].base_vaddr;
	cdma_base_vaddr = (uint8_t *)(base_vaddr + OFFSET_AXI_CDMA_LITE); 
	value = readl(cdma_base_vaddr + CDMA_SR);
	if((value & BITMASK(12)/*IOC_Irq*/) != 0) {
		complete(&cmp);
		//mydebug("\n");
		value |= BITMASK(12);
		writel(value, cdma_base_vaddr + CDMA_SR);
		status = IRQ_HANDLED;
	} else if((value & BITMASK(14)/*Err_Irq*/) != 0) {
		complete(&cmp);
		mydebug("\n");
		value |= BITMASK(14);
		writel(value, cdma_base_vaddr + CDMA_SR);
		status = IRQ_HANDLED;
	}
	/* Handle DMA and any user interrupts */
	return status;
}

static int init_dma(kc705_pci_dev_t *kc705_pci_dev) {
	int rtn;
	uint8_t *base_vaddr = kc705_pci_dev->bar_info[0].base_vaddr;
	uint8_t *cdma_base_vaddr = (uint8_t *)(base_vaddr + OFFSET_AXI_CDMA_LITE); 

	//reset cdma
	uint32_t default_value = 0x00010002;//0000_0000_0000_0001(irq threshold)_0000_0000_0000_001(tail ptr enable)0
	uint32_t value;
	
	//reset
	value = default_value | BITMASK(2);//reset bit
	writel(value, cdma_base_vaddr + CDMA_CR);
	rtn = wait_for_iostatus_timeout(0, cdma_base_vaddr + CDMA_CR, BITMASK(2), 0);
	if(rtn != 0) {
		mydebug("time out!\n");
	}

	//enable sg mode
	value = readl(cdma_base_vaddr + CDMA_CR) & (~(BITMASK(3)));//sg mode
	writel(value, cdma_base_vaddr + CDMA_CR);

	value = readl(cdma_base_vaddr + CDMA_CR) | BITMASK(3);//sg mode
	writel(value, cdma_base_vaddr + CDMA_CR);

	//enable interrupt
	value = readl(cdma_base_vaddr + CDMA_CR) | BITMASK(12)/*ioc interrupt*/ | BITMASK(14)/*err interrupt*/;
	writel(value, cdma_base_vaddr + CDMA_CR);

	value = readl(cdma_base_vaddr + CDMA_CR) | (2 << 16)/*IRQThreshold:2*/;
	writel(value, cdma_base_vaddr + CDMA_CR);


	return rtn;
}

static int alloc_sg_des_item(uint32_t SA, uint32_t DA, uint32_t CONTROL, struct list_head *sg_list) {
	int rtn = 0;
	kc705_sg_item_info_t *sg_item = (kc705_sg_item_info_t *)vzalloc(sizeof(kc705_sg_item_info_t));

	if(sg_item == NULL) {
		rtn = -1;
		mydebug("alloc sg_item failed.\n");
		return rtn;
	}

	sg_item->des.des.SA = SA;
	sg_item->des.des.DA = DA;
	sg_item->des.des.CONTROL = CONTROL;
	list_add_tail(&sg_item->sg_item, sg_list);
	return 0;
}

static void free_sg_des_items(struct list_head *sg_list) {
	kc705_sg_item_info_t *sg_item, *sg_item_next;
	list_for_each_entry_safe(sg_item, sg_item_next, sg_list, sg_item) {
		list_del(&sg_item->sg_item);

		vfree(sg_item);
	}
}

static int alloc_sg_list_chain(uint32_t tx_axiaddr, uint32_t rx_axiaddr) {
	int rtn = 0;
	int offset = 0;

	free_sg_des_items(&sg_descripter_list);

	rtn = alloc_sg_des_item(
			BASE_Translation_BRAM + offset,
			BASE_AXI_PCIe_CTL + AXIBAR2PCIEBAR_1U,
			sizeof(uint64_t),
			&sg_descripter_list
		);
	if(rtn != 0) {
		goto failed;
	}

	offset += sizeof(uint64_t);

	rtn = alloc_sg_des_item(tx_axiaddr, BASE_AXI_DDR_ADDR, DM_CHANNEL_TX_SIZE, &sg_descripter_list);
	if(rtn != 0) {
		goto failed;
	}

	rtn = alloc_sg_des_item(
			BASE_Translation_BRAM + offset,
			BASE_AXI_PCIe_CTL + AXIBAR2PCIEBAR_1U,
			sizeof(uint64_t),
			&sg_descripter_list
		);
	if(rtn != 0) {
		goto failed;
	}

	rtn = alloc_sg_des_item(BASE_AXI_DDR_ADDR, rx_axiaddr, DM_CHANNEL_RX_SIZE, &sg_descripter_list);
	if(rtn != 0) {
		goto failed;
	}

	return rtn;

failed:
	rtn = -1;
	free_sg_des_items(&sg_descripter_list);

	return rtn;
}

static int flush_sg_des_items(kc705_transfer_descriptor_t *axi_pcie_sg_port, struct list_head *sg_list) {
	kc705_transfer_descriptor_t *pdes = axi_pcie_sg_port; //buffer for sg, axi address 0x80800000
	kc705_sg_item_info_t *info;
	uint32_t bar_sg_next_addr_offset = BASE_AXI_PCIe_BAR0 + SG_DESCRIPTOR_SIZE;

	list_for_each_entry(info, sg_list, sg_item) {
		//kc705_sg_item_info_t *next_info = list_next_entry(info, sg_item);

		if(info->sg_item.next != sg_list) {
		//if(&(next_info->sg_item) != sg_list) {
			info->des.des.NXTDESC_PNTR = bar_sg_next_addr_offset;
			cdma_tail_des_axi_addr = bar_sg_next_addr_offset;
			bar_sg_next_addr_offset += SG_DESCRIPTOR_SIZE;
		} else {
			info->des.des.NXTDESC_PNTR = BASE_AXI_PCIe_BAR0;
		}


		pdes->des = info->des.des;

		pdes++;

	}

	free_sg_des_items(&sg_descripter_list);

	return 0;
}

static int prepare_bars_map(kc705_pci_dev_t *kc705_pci_dev, uint64_t addr_sg_bar, uint64_t addr_tx_bar, uint64_t addr_rx_bar) {
	uint8_t *base_vaddr = kc705_pci_dev->bar_info[0].base_vaddr;
	uint32_t *bram_vddr_reg = (uint32_t *)base_vaddr;
	uint32_t *bar_vddr_map_ctrl_reg = (uint32_t *)(base_vaddr + OFFSET_AXI_PCIe_CTL + AXIBAR2PCIEBAR_0U);

	//bind sg 
	write_addr_to_reg(bar_vddr_map_ctrl_reg, addr_sg_bar);

	//prepare tx && rx buffer address for dm map ctl register at TR BRAM
	write_addr_to_reg(bram_vddr_reg, addr_tx_bar);
	bram_vddr_reg++;
	bram_vddr_reg++;
	write_addr_to_reg(bram_vddr_reg, addr_rx_bar);

	return 0;
}

static int dma_prepare_transfer(kc705_pci_dev_t *kc705_pci_dev, uint64_t addr_sg_bar, uint64_t addr_tx_bar, uint64_t addr_rx_bar, uint64_t addr_tx, uint64_t addr_rx) {
	int rtn = 0;

	prepare_bars_map(kc705_pci_dev, addr_sg_bar, addr_tx_bar, addr_rx_bar);

	rtn = alloc_sg_list_chain(addr_tx, addr_rx);
	if(rtn != 0) {
		return rtn;
	}

	rtn = flush_sg_des_items(kc705_pci_dev->bar_map_memory[0], &sg_descripter_list);

	return rtn;
}

static int start_cdma(kc705_pci_dev_t *kc705_pci_dev) {
	uint8_t *base_vaddr = kc705_pci_dev->bar_info[0].base_vaddr;
	uint8_t *cdma_base_vaddr = (uint8_t *)(base_vaddr + OFFSET_AXI_CDMA_LITE); 

	init_completion(&cmp);

	//update cdma curdesc pointer
	writel(BASE_AXI_PCIe_BAR0, cdma_base_vaddr + CDMA_CURDESC_PNTR);

	writel(cdma_tail_des_axi_addr, cdma_base_vaddr + CDMA_TAILDESC_PNTR);
	return 0;
}

static int dma_trans_sync(kc705_pci_dev_t *kc705_pci_dev) {
	unsigned long tmo;
	int rtn = 0;

	tmo = msecs_to_jiffies(1000);
	tmo = wait_for_completion_timeout(&cmp, tmo);
	if (0 == tmo) {
		mydebug("transfer timed out!\n");
		rtn = -1;
	}

	return rtn;
}

void inc_dma_op_count(void);
int dma_worker_thread(void *ppara) {
	int rtn = 0;
	kc705_pci_dev_t *kc705_pci_dev = (kc705_pci_dev_t *)ppara;

	init_dma(kc705_pci_dev);

	while(true) {
		if(kthread_should_stop()) {
			return -1;
		}

		set_current_state(TASK_UNINTERRUPTIBLE);  
		//schedule_timeout(1*HZ); 
		init_dma(kc705_pci_dev);
		dma_prepare_transfer(kc705_pci_dev, (uint64_t)kc705_pci_dev->bar_map_addr[0], (uint64_t)kc705_pci_dev->bar_map_addr[1], (uint64_t)kc705_pci_dev->bar_map_addr[2], BASE_AXI_PCIe_BAR1, BASE_AXI_PCIe_BAR1);
		//dump_memory(kc705_pci_dev->bar_map_memory[0], 4 * 0x40);
		prepare_test_data(kc705_pci_dev);
		start_cdma(kc705_pci_dev);
		dma_trans_sync(kc705_pci_dev);
		inc_dma_op_count();
		test_result(kc705_pci_dev);
		//mydebug("\n");
	}

	return rtn;
}
