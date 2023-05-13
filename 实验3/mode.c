/*#include<stdio.h>
#include<math.h>
#include<ctype.h>
#include<string.h>
#include<stdlib.h>

#define MAX(a,b) ((a)>(b)?(a):(b))
#define MIN(a,b) ((a)<(b)?(a):(b))
#define Pi 3.1415926535
#define eps 1e-8
#define ULL unsigned long long
#define LL long long

int KEY[16][64] ;

int * h2b( char *s , int *n){
	
	int i = 0;
	int point = 0 ;
	int length = 0 ;
	
	length = strlen(s) ;
	
	for( i = 2 , point = 0 ; i < length ; i++ ){
		switch (s[i]){
			case '0' : n[point++] = 0 , n[point++] = 0 , n[point++] = 0 , n[point++] = 0 ; break;
			case '1' : n[point++] = 0 , n[point++] = 0 , n[point++] = 0 , n[point++] = 1 ; break;
			case '2' : n[point++] = 0 , n[point++] = 0 , n[point++] = 1 , n[point++] = 0 ; break;
			case '3' : n[point++] = 0 , n[point++] = 0 , n[point++] = 1 , n[point++] = 1 ; break;
			case '4' : n[point++] = 0 , n[point++] = 1 , n[point++] = 0 , n[point++] = 0 ; break;
			case '5' : n[point++] = 0 , n[point++] = 1 , n[point++] = 0 , n[point++] = 1 ; break;
			case '6' : n[point++] = 0 , n[point++] = 1 , n[point++] = 1 , n[point++] = 0 ; break;
			case '7' : n[point++] = 0 , n[point++] = 1 , n[point++] = 1 , n[point++] = 1 ; break;
			case '8' : n[point++] = 1 , n[point++] = 0 , n[point++] = 0 , n[point++] = 0 ; break;
			case '9' : n[point++] = 1 , n[point++] = 0 , n[point++] = 0 , n[point++] = 1 ; break;
			case 'a' : n[point++] = 1 , n[point++] = 0 , n[point++] = 1 , n[point++] = 0 ; break;
			case 'b' : n[point++] = 1 , n[point++] = 0 , n[point++] = 1 , n[point++] = 1 ; break;
			case 'c' : n[point++] = 1 , n[point++] = 1 , n[point++] = 0 , n[point++] = 0 ; break;
			case 'd' : n[point++] = 1 , n[point++] = 1 , n[point++] = 0 , n[point++] = 1 ; break;
			case 'e' : n[point++] = 1 , n[point++] = 1 , n[point++] = 1 , n[point++] = 0 ; break;
			case 'f' : n[point++] = 1 , n[point++] = 1 , n[point++] = 1 , n[point++] = 1 ; break;
		}
	}
	return n ;
}

int * IP_substitution(int *num_64 , int mode ){
	int IP[65] = {
		58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
	};
	int IP_[65] = {
		40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
	} ;
	int ans_64[64] = {0} ;
	int i = 0 ;
	
	for(i = 0 ; i < 64 ; i++ ){
		ans_64[i] = num_64[i] ;
	}
	
	if(mode == 1){
		for(i = 0 ; i < 64 ; i++ ){
			num_64[i] = ans_64[IP[i]-1] ;
		}
	}
	else{
		for(i = 0 ; i < 64 ; i++ ){
			num_64[i] = ans_64[IP_[i]-1] ;
		}
	}
	return num_64 ;
}

int *ox_key(int *s_48,int *k_48){
	int *ans;
	int i = 0 ;
	
	ans = (int*)malloc(sizeof(int)*49);
	
	for(i = 0 ; i<48 ; i++){
		ans[i] = s_48[i] ^ k_48[i];
	}
	return ans ;
}


int *SBox(int *s_48){
	int sbox[8][4][16]={
	{
		{14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7},
		{0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8},
		{4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0},
		{15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13}
	},
	{
		{15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10},
		{3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5},
		{0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15},
		{13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9}
	},
	{
		{10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8},
		{13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1},
		{13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7},
		{1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12}
	},
	{
		{7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15},
		{13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9},
		{10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4},
		{3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14}
	},
	{
		{2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9},
		{14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6},
		{4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14},
		{11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3}
	},
	{
		{12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11},
		{10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8},
		{9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6},
		{4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13}
	},
	{
		{4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1},
		{13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6},
		{1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2},
		{6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12}
	},
	{
		{13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7},
		{1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2},
		{7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8},
		{2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11}
	}
						};
	int tmp[32]= {0} ;
	int *n ;
	
	n = (int*)malloc(sizeof(int)*33);
	
	int i = 0 , j = 0 , k = 0 , count = 0, point = 0;
	int length = 0;
	
	printf("sbox:\n") ;
	
	while(count < 48){
		i = (s_48[count]<<1) + (s_48[count+5]);
		j = (s_48[count+1]<<3) + (s_48[count+2]<<2) + (s_48[count+3]<<1) + (s_48[count+4]) ;
		k = count/6;
		tmp[point++] = sbox[k][i][j] ;
		printf("%d " , tmp[point-1] ) ;
		count += 6 ;
	}
	printf("\n") ;
	length = point ;
	point = 0 ;
	for( i = 0 ; i < length ; i++ ){
		switch (tmp[i]){
			case 0 : n[point++] = 0 , n[point++] = 0 , n[point++] = 0 , n[point++] = 0 ; break;
			case 1 : n[point++] = 0 , n[point++] = 0 , n[point++] = 0 , n[point++] = 1 ; break;
			case 2 : n[point++] = 0 , n[point++] = 0 , n[point++] = 1 , n[point++] = 0 ; break;
			case 3 : n[point++] = 0 , n[point++] = 0 , n[point++] = 1 , n[point++] = 1 ; break;
			case 4 : n[point++] = 0 , n[point++] = 1 , n[point++] = 0 , n[point++] = 0 ; break;
			case 5 : n[point++] = 0 , n[point++] = 1 , n[point++] = 0 , n[point++] = 1 ; break;
			case 6 : n[point++] = 0 , n[point++] = 1 , n[point++] = 1 , n[point++] = 0 ; break;
			case 7 : n[point++] = 0 , n[point++] = 1 , n[point++] = 1 , n[point++] = 1 ; break;
			case 8 : n[point++] = 1 , n[point++] = 0 , n[point++] = 0 , n[point++] = 0 ; break;
			case 9 : n[point++] = 1 , n[point++] = 0 , n[point++] = 0 , n[point++] = 1 ; break;
			case 10 : n[point++] = 1 , n[point++] = 0 , n[point++] = 1 , n[point++] = 0 ; break;
			case 11 : n[point++] = 1 , n[point++] = 0 , n[point++] = 1 , n[point++] = 1 ; break;
			case 12 : n[point++] = 1 , n[point++] = 1 , n[point++] = 0 , n[point++] = 0 ; break;
			case 13 : n[point++] = 1 , n[point++] = 1 , n[point++] = 0 , n[point++] = 1 ; break;
			case 14 : n[point++] = 1 , n[point++] = 1 , n[point++] = 1 , n[point++] = 0 ; break;
			case 15 : n[point++] = 1 , n[point++] = 1 , n[point++] = 1 , n[point++] = 1 ; break;
		}
	}
	return n ;
}

int *permutation(int *s_32){
	int ans[32] ;
	int P[32] = {
		16,  7, 20, 21, 29, 12, 28, 17,  1, 15, 23, 26,  5, 18, 31, 10,
		2,  8, 24, 14, 32, 27,  3,  9, 19, 13, 30,  6, 22, 11,  4, 25
	} ;
	int i = 0 ;
	
	for(i = 0 ; i < 32 ; i++ ){
		ans[i] = s_32[i] ;
	}
	
	for(i = 0 ; i<32 ; i++){
		s_32[i] = ans[P[i]-1] ;
	} 
	return s_32 ;
}
int *F_func( int *s , int*k ){
	int i = 0 ;
	int l[32] = {0} , r[32] = {0} ;
	int s1[49] ;
	int s2[49] ;
	int *s3 ;
	int *s4 ;
	int s5[32] ;
	int *ans ;
	
	int E[48] = {
		32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
	};
	
	ans = (int*)malloc(sizeof(int)*64);
	
	//初始化：分组 
	for(i = 0 ; i < 64 ; i++){
		if(i < 32 ){
			l[i] = s[i] ;
		}
		else{
			r[i-32] = s[i] ;
		}
	} 
	printf("明文分为两组：\nL: ");
	for(i = 0 ; i<32;i++){
		printf("%d",l[i]) ;
	}
	printf(" R: ") ;
	for(i = 0 ; i<32;i++){
		printf("%d",r[i]) ;
	}
	printf(" %d位\n",i) ;
	
	//拓展置换
	for(i = 0 ; i < 48 ; i++){
		s1[i] = r[E[i]-1] ;
	}
	
	printf("拓展置换:\n");
	for(i = 0 ; i < 48 ; i++ ){
		printf("%d" , s1[i] ) ;
	}
	printf(" %d位\n",i) ;
	
	//与密钥异或
	for(i = 0 ; i<48 ; i++){
		s2[i] = s1[i] ^ k[i];
	}
	
	printf("密钥：\n");
	for(i = 0 ; i < 48 ; i++ ){
		printf("%d" , k[i] ) ;
	}
	printf("\n") ;
	printf("与密钥异或：\n");
	for(i = 0 ; i < 48 ; i++ ){
		printf("%d" , s2[i] ) ;
	}
	printf(" %d位\n",i) ;
	
	//压缩置换sbox
	s3 = SBox(s2) ;
	printf("压缩置换：\n");
	for(i = 0 ; i < 32 ; i++ ){
		printf("%d" , s3[i] ) ;
	}
	printf(" %d位\n",i) ;
	//置换运算p
	s4 = permutation(s3);
	printf("P置换：\n");
	for(i = 0 ; i < 32 ; i++ ){
		printf("%d" , s3[i] ) ;
	}
	printf(" %d位\n",i) ;
	//与左半侧异或并易位 
	for(i = 0 ; i < 32 ; i++){
		s5[i] = s4[i] ^ l[i] ;
	}
	printf("与左侧异或并易位\n");
	for(i = 0 ; i < 64 ; i++){
		if(i < 32){
			ans[i] = r[i] ;
		}
		else{
			ans[i] = l[i-32];
		}
		printf("%d", ans[i]) ;
	}
	printf("\n") ;
	
	return ans ;
}

void get_key(int *k_64){
	int LS[16] = {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};
	int PC1[56] = {
		57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
	} ;
	int PC2[48] = {
		14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
	};
	int k1[56] = {0} , k2[56] = {0} ;
	int l[28] = {0} , r[48] = {0} ; 
	int ls = 0;
	int temp[28] = {0} ;
	int i = 0 , round = 0 , point = 0 ;
	
	//初始密钥置换 
//	printf("密钥置换:\n"); 
	for(i = 0 ; i < 56 ; i++ ){
		k1[i] = k_64[PC1[i]-1] ;
//		printf("%d" , k1[i]); 
	}
//	printf(" %d位" , i) ;
//	puts("");
	//置换后分为左右两组
	for(i = 0 ; i < 56 ; i++ ){
		if(i < 28){
			l[i] = k1[i] ;
		}
		else{
			r[i-28] = k1[i] ;
		}
	} 
	
	for(round = 0 ; round < 16 ; round++ ){
		ls = LS[round] ;
		//l左循环 
		point = 0;
		for(i = ls ; i < 28 ; i++ ){
			temp[point++] = l[i] ;
		}
		for(i = 0 ; i < ls ; i++ ){
			temp[point++] = l[i] ;
		}
		for( i = 0 ; i < 28 ; i++ ){
			l[i] = temp[i] ;
		}
		//r左循环 
		point = 0;
		for(i = ls ; i < 28 ; i++ ){
			temp[point++] = r[i] ;
		}
		for(i = 0 ; i < ls ; i++ ){
			temp[point++] = r[i] ;
		}
		for( i = 0 ; i < 28 ; i++ ){
			r[i] = temp[i] ;
		}
		//PC2置换 组合为k2->置换 
		for(i = 0 ; i<56 ; i++ ){
			if(i<28){
				k2[i] = l[i] ;
			}
			else{
				k2[i] = r[i-28] ;
			}
		}
		for(i = 0 ; i < 48 ; i++){
			KEY[round][i] = k2[PC2[i]-1] ;
		} 
	}
}

int * DES(char *s , char *k, int mode){
	int *s_64 = NULL , *k_64 = NULL ;
	int *s1 ; 
	int *s2 ;
	int *s3 ;
	static int *ans ;
	
	int i = 0 , j = 0 ;
	
	// 初始化，将明文和密钥由字符串转化为数组形式方便后续计算 
	s_64 = h2b(s) ;
	k_64 = h2b(k) ;
	printf("DES初始化\n");
	for(i = 0 ; i < 64 ; i++ ){
		printf("%d" , s_64[i]) ;
	}
	puts("") ;
	printf("密钥输入：\n");
	for(i = 0 ; i < 64 ; i++ ){
		printf("%d" , k_64[i]) ;
	}
	puts("") ;
	//获得密钥 
	get_key(k_64) ;
	
	

	printf("DES密钥：\n");
	for(i = 0 ; i < 16 ; i++ ){
		for(j = 0 ; j < 48 ; j++ ){
			printf("%d" , KEY[i][j]) ; 
		}
		puts("") ;
	}

	// 初始置换 
	s1 = IP_substitution(s_64,1) ;
	printf("初始置换：\n");
	for( i = 0 ; i < 64 ; i++ ){
		printf("%d" , s1[i] ) ;
	}
	printf(" %d位\n",i) ;
	
	if(mode == 1){
		for(i = 0 ; i < 16 ; i++){
			printf("-------------第%d轮-------------\n",i+1) ;
			s2 = F_func(s1,KEY[i]);
			printf("每轮结果：\n") ;
			for(j = 0 ; j < 64 ; j++){
				s1[j] = s2[j] ;
				printf("%d",s1[i]);
			}
			puts("");
		}
		//交换 
		for(j = 0 ; j < 64 ; j++){
			if(j<32){
				s3[j] = s1[j+32] ;
			}
			else{
				s3[j] = s1[j-32];
			}
		}
		printf("交换：\n");
		for( i = 0 ; i < 64 ; i++ ){
			printf("%d" , s3[i] ) ;
		}
		printf(" %d位\n",i) ;
		ans = IP_substitution(s3,0);
	}
	else{
		
	}
	free(s_64) ;
	free(k_64) ;
	return ans ;
}

int main() {
	int T ;
	char s[19] , k[19] ;
	int op ;
	int i = 0 ;
	int *ans ;
	
	
	int *num ;
	int *s_64 ;

//	scanf("%d" , &T ) ;
	scanf("%s" , s ) ;
	scanf("%s" , k ) ;
	scanf("%d" , &op ) ;
	
	ans = DES(s,k,op) ;
	
	for( i = 0 ; i < 64 ; i++ ){
		printf("%d",ans[i]) ;
	}
	
	free(ans);
	
	return 0 ;
}
*/
/*
1
0x02468aceeca86420
0x0f1571c947d9e859
1

*/

