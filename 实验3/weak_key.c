#include<stdio.h>
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
#define Max_num 4294967295

int KEY[16][48] ;

void show(int n[] , int num ){
	int i = 0 ;
	for( i = 0 ; i < num ; i++ ){
		printf("%d" , n[i] ) ;
	}
	puts("");
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
	for(i = 0 ; i < 56 ; i++ ){
		k1[i] = k_64[PC1[i]-1] ;
	}

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

void h2b( char *s , int n[]){
	
	int i = 0;
	int point = 0 ;
	int length = 18 ;
	
//	printf("%s\n" , s) ;
	
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
}

int is_same_key(int k[][48]){
	int  i = 0 , j = 0 ;
	int judge = 1 ;
	int flag = 1 ;
	
	for(i = 0 ; i < 48 ; i++ ){
		judge = k[0][i] ;
		for(j = 1 ; j < 16 ; j++ ){
			if(k[j][i] != judge){
				flag = 0 ;
				break ;
			}
		}
		if(flag == 0 ){
			break ;
		}
	}
	return flag ;
}
int main() {
	
	ULL head = 0 , tail = 0 ;
	
	int i , j ;
	int k[64] = {0} ;
	char key[66] = {"0"} ;
	int count = 0 ;
	
	FILE *f = NULL ;
	
	f = fopen("WEAK_KEY.txt" , "w+" ) ;

	for(head = 0 ; head <= Max_num ; head++ ){
		for(tail = 0 ; tail <= Max_num ; tail++ ){
			for(i = 0 ; i < 64 ; i++ ){
				if(i < 32 ){
					k[i] = (head>>(31-i))&1 ;
				}
				else{
					k[i] = (tail>>(63-i))&1 ;
				}
			}
			show(k,64) ;
			get_key(k) ;
			if(is_same_key(KEY)){
				for(j=0;j<64;j++){
					key[j] = k[j] + '0' ;
				}
				key[j++] = '\n' ;
				key[j] = '\0' ;
				count = fprintf(f,key) ;
				if(count > 0){
					printf("Yes\n") ;
				}
			}
		}
	}

/*
	for(tail = 0 ,head = 0; tail <= 10000 ; tail++ ){
		for(i = 0 ; i < 64 ; i++ ){
			if(i < 32 ){
				k[i] = (head>>(31-i))&1 ;
			}
			else{
				k[i] = (tail>>(63-i))&1 ;
			}
		}
		show(k,64) ;
		get_key(k) ;
		if(is_same_key(KEY)){
			for(j=0;j<64;j++){
				key[j] = k[j] + '0' ;
			}
			key[j++] = '\n' ;
			key[j] = '\0' ;
			count = fprintf(f,key) ;
			if(count > 0){
				printf("Yes\n") ;
			}
		}
	}
*/		
	fclose(f) ;
	
	return 0 ;
}

