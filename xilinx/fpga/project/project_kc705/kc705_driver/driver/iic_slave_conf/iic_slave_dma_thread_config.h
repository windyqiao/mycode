#ifndef _IIC_SLAVE_DMA_THREAD_CONFIG_H
#define _IIC_SLAVE_DMA_THREAD_CONFIG_H

static int iic_slave_dma_receiver_thread(void *ppara) {
	int ret = 0;
	pcie_dma_t *dma = (pcie_dma_t *)ppara;
	//kc705_pci_dev_t *kc705_pci_dev = (kc705_pci_dev_t *)dma->kc705_pci_dev;

	while(!kthread_should_stop()) {
		//set_current_state(TASK_UNINTERRUPTIBLE);  
		//schedule_timeout(msecs_to_jiffies(10)); 
		
		//put_pcie_tr(dma, 0, 0, 0, dma->receive_bulk_size, NULL, NULL);
	}

	mydebug("\n");

	return ret;
}

dma_thread_info_t iic_slave_dma_threads[] = {
	{
		.t = &iic_slave_dma_receiver_thread,
		.thread_name = "iic_slave_receiver"
	},
};

#define IIC_SLAVE_DMA_THREAD (sizeof(iic_slave_dma_threads) / sizeof(dma_thread_info_t))

#endif//#ifndef _IIC_SLAVE_DMA_THREAD_CONFIG_H
