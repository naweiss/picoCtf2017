#include <stdio.h>
 
int doMain(unsigned int a){
	// int a;
	// printf("Please input an integer value: ");
	// scanf("%d", &a);
	
	unsigned int PART_1	= a&0xFF000000;
	unsigned int PART_2	= a&0x00FF0000;
	unsigned int PART_3	= a&0x0000FF00;
	unsigned int PART_4 	= a&0x000000FF;

	unsigned int ans = (PART_1 >> 24);
	unsigned int tmp = 0;

	while (tmp < 13){
		tmp++;
		ans -= 13;
	}
	
	ans -= 6;
	unsigned int UNKNOWN	= (ans << 24);
	PART_2 >>= 16;
	tmp = PART_2-81;
	ans = (tmp << 8) - (tmp << 6);
	ans = tmp - ans;
	PART_3 >>= 8;
	tmp = (PART_4 << 1) + 3;
	
	if (tmp != PART_3){
		tmp = 165;
	}
	else{
		ans <<= 16;
		tmp = 94;
	}
	
	tmp -= 94;
	tmp <<= 8;
	PART_1 >>= 24;
	PART_2 = PART_1 - PART_2;
	PART_4 -= PART_2;
	ans += UNKNOWN;
	ans += tmp;
	PART_2 = PART_4 + ans;
	return (PART_2 == 0);
}

int main () {
	
	for (unsigned int i=0; i <=4294967294; i++)
	{
		unsigned int ans = doMain(i);
		if (ans){
			printf("Success :) 0x%x\n",i);
			break;
		}
	}
	
	return 0;
}