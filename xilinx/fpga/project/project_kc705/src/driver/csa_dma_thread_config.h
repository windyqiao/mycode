#ifndef _CSA_DMA_THREAD_CONFIG_H
#define _CSA_DMA_THREAD_CONFIG_H

unsigned long long i2s_read_count = 0;

static int csa_dma_receiver_thread(void *ppara) {
	int ret = 0;
	pcie_dma_t *dma = (pcie_dma_t *)ppara;

	while(!kthread_should_stop()) {
		//set_current_state(TASK_UNINTERRUPTIBLE);  
		//schedule_timeout(msecs_to_jiffies(10)); 

		put_pcie_tr(dma, 0, 0, 0, dma->receive_bulk_size, NULL, NULL);

		i2s_read_count++;
	}

	mydebug("\n");

	return ret;
}

dma_thread_info_t csa_dma_threads[] = {
	{
		.t = &csa_dma_receiver_thread,
		.thread_name = "csa_receiver"
	},
};

#define CSA_DMA_THREAD (sizeof(csa_dma_threads) / sizeof(dma_thread_info_t))

#endif//#ifndef _CSA_DMA_THREAD_CONFIG_H
