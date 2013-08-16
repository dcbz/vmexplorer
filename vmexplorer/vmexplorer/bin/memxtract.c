#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <mach/vm_prot.h>
#include <mach/i386/vm_types.h>
#include <mach/shared_region.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>
#include <sys/types.h>

#define PAGESIZE 0x1000

int main(int ac, char **av)
{
	kern_return_t kr; 
	task_t mytask;
	uint32_t sz;
	unsigned long startaddr,endaddr,i=0,numpages=0;
	unsigned char **outbuff;
	
	FILE *fp;

	if(ac != 5) {
		printf("usage: %s <pid> <output file> <start address> <end address>\n",av[0]);
		exit(1);
	}

	if(task_for_pid(mach_task_self(),atoi(av[1]),&mytask)) {
		printf("[!] error: could not attach to pid.\n");
		exit(1);
	}

	if(task_suspend(mytask) != KERN_SUCCESS) {
		printf("[!] Failed suspending task, trying again.\n");
		exit(1);
	}

	sscanf(av[3],"%lx",&startaddr);
	sscanf(av[4],"%lx",&endaddr);

	numpages = ((endaddr - startaddr) / PAGESIZE);

	fp = fopen(av[2],"w+");
	if(fp == NULL){
		printf("[!] error: opening output file.\n");
		exit(1);
	}

	for(i=0; i<=numpages; i++) {
/*
kern_return_t   vm_read
                (vm_task_t                          target_task,
                 vm_address_t                           address,
                 vm_size_t                                 size,
                 size                                  data_out,
                 target_task                         data_count);
*/
		sz = 4;
		//printf("[+] reading from 0xx%lx\n",startaddr);
		if(mach_vm_read(mytask,(unsigned long)startaddr,PAGESIZE,&outbuff,&sz) != KERN_SUCCESS) {
			printf("error: reading from process\n");
			exit(1);
		}
	
		if(fwrite(outbuff,PAGESIZE,1,fp) != 1) {
			printf("error: writing to file\n");
			exit(1);
		}
		startaddr+=PAGESIZE;
	}

	fclose(fp);

	if(task_resume(mytask) != KERN_SUCCESS) {
		printf("[!] Failed resuming task, trying again.\n");
		exit(1);
	}

	return 0;
}
