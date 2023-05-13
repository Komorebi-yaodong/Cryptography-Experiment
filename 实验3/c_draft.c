#include<stdio.h>
#define LL long long

typedef struct BigNumber{
	LL head;
	LL tail;
}BN;

BN KEY[16] ;

void get_key(BN key){
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
	
	BN k1 , k2 ;
	LL C = 0 , D = 0 ;
	LL tmp = 0 ;
	int ls = 0 ;
	int i = 0 , j = 0 , count = 0 ;
	int distance = 0 ;
	int flag = 0 ;
	
	k1.head = 0 ;
	k1.tail = 0 ;
	for(i=0;i<56;i++){
		distance = 64-PC1[i] ;
		if(distance >= 32){
			flag = 1&(key.head>>(distance-32));
		}
		else{
			flag = 1&(key.tail>>(distance));
		}
		if(i>=28){
			k1.tail = k1.tail^(flag<<(55-i)) ;
		}
		else{
			k1.head = k1.head^(flag<<(27-i)) ;
		}
	}
	C = k1.head ;
	D = k1.tail ;

	for(i = 0 ; i < 16 ; i++ ){
		
		ls = LS[i] ;
		tmp = C>>(28-ls) ;
		C = ((C<<ls)^tmp)&0xfffffff ;
		tmp = D>>(28-ls) ;
		D = ((D<<ls)^tmp)&0xfffffff ;
		
		k2.head = 0 ;
		k2.tail = 0 ;
		for(j = 0 ; j < 48 ; j++ ){
			distance = 56 - PC2[j] ;
			if(distance >= 28){
				flag = 1&(C>>(distance-28));
			}
			else{
				flag = 1&(D>>(distance));
			}
			if(j>=24){
				k2.tail = k2.tail^(flag<<(47-j)) ;
			}
			else{
				k2.head = k2.head^(flag<<(23-j)) ;
			}
		}
		KEY[count++] =  k2 ;
	} 
}

BN h2n(char *s){
	BN num ;
	int i = 0 ;
	int c = 0 ;
	int point = 1 ;
	
	num.head = 0 ;
	num.tail = 0 ;
	
	for(i = 2 ,point = 1; i < 18 ; i++ ,point++){
		if(i < 10){
			if(s[i]>='0' && s[i] <= '9'){
				num.head ^= ((s[i]-'0')<<(32-4*point)) ;
			}
			else{
				num.head ^= ((s[i]-'a'+10)<<(32-4*point)) ;
			}
		}
		else{
			if(s[i]>='0' && s[i] <= '9'){
				num.tail ^= ((s[i]-'0')<<(64-4*point)) ;
			}
			else{
				num.tail ^= ((s[i]-'a'+10)<<(64-4*point)) ;
			}
		}
	}
	return num ;
}

BN IP_substitution(BN s_64 , int mode ){
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
	int i = 0 ;
	int distance , flag = 0 ;
	BN result ;
	
	
	result.head = 0 ;
	result.tail = 0 ;
	
	if(mode==1){
		for(i = 0 ; i < 64 ; i++ ){
			distance = 64-IP[i] ;
			if(distance >= 32){
				flag = 1&(s_64.head>>(distance-32)) ;
			}
			else{
				flag = 1&(s_64.tail>>(distance)) ;
			}
			if(i>=32){
				result.tail = (result.tail^(flag<<(63-i)))&0xffffffff ;
			}
			else{
				result.head = (result.head^(flag<<(31-i)))&0xffffffff ;
			}
		}
	}
	
	else{
		for(i = 0 ; i < 64 ; i++ ){
			distance = 64-IP_[i] ;
			if(distance >= 32){
				flag = 1&(s_64.head>>(distance-32)) ;
			}
			else{
				flag = 1&(s_64.tail>>(distance)) ;
			}
			if(i>=32){
				result.tail = (result.tail^(flag<<(63-i)))&0xffffffff ;
			}
			else{
				result.head = (result.head^(flag<<(31-i)))&0xffffffff ;
			}
		}
	}
	return result ;
}

BN expand_substitution(LL num){
	BN res ;
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
	int i = 0 ;
	int distance ,flag = 0;
	
	res.head = 0 ;
	res.tail = 0 ;
	
	for(i = 0 ; i < 48 ; i++){
		distance = E[i] - 1 ;
			flag = 1 & (num >> distance);
			if(i>=24){
				res.head = (res.head^(flag<<(i-24)))&0xffffff ;
			}
			else{
				res.tail = (res.tail^(flag<<(i)))&0xffffff ;
			}
	}
	return res ;
}

LL s_box(BN s_48){
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
	int tmp ;
	int i , j ;
	LL res = 0 ;
	int s0,s1,s2,s3,s4,s5,s6,s7 ;
	
	tmp = (s_48.head>>18)&0b111111 ;
	i = (((tmp>>4)&0b10)^(tmp&1))&0b11 ;
	j = (tmp>>1)& 0b01111 ;
	s0 = sbox[0][i][j] ;
	
	tmp = (s_48.head>>12)&0b111111 ;
	i = (((tmp>>4)&0b10)^(tmp&1))&0b11 ;
	j = (tmp>>1)& 0b01111 ;
	s1 = sbox[1][i][j] ;
	
	tmp = (s_48.head>>6)&0b111111 ;
	i = (((tmp>>4)&0b10)^(tmp&1))&0b11 ;
	j = (tmp>>1)& 0b01111 ;
	s2 = sbox[2][i][j] ;
		
	tmp = (s_48.head>>0)&0b111111 ;
	i = (((tmp>>4)&0b10)^(tmp&1))&0b11 ;
	j = (tmp>>1)& 0b01111 ;
	s3 = sbox[3][i][j] ;
		
	tmp = (s_48.tail>>18)&0b111111 ;
	i = (((tmp>>4)&0b10)^(tmp&1))&0b11 ;
	j = (tmp>>1)& 0b01111 ;
	s4 = sbox[4][i][j] ;
		
	tmp = (s_48.tail>>12)&0b111111 ;
	i = (((tmp>>4)&0b10)^(tmp&1))&0b11 ;
	j = (tmp>>1)& 0b01111 ;
	s5 = sbox[5][i][j] ;
		
	tmp = (s_48.tail>>6)&0b111111 ;
	i = (((tmp>>4)&0b10)^(tmp&1))&0b11 ;
	j = (tmp>>1)& 0b01111 ;
	s6 = sbox[6][i][j] ;
		
	tmp = (s_48.tail>>0)&0b111111 ;
	i = (((tmp>>4)&0b10)^(tmp&1))&0b11 ;
	j = (tmp>>1)& 0b01111 ;
	s7 = sbox[7][i][j] ;
	
	res = ((s0<<28)^(s1<<24)^(s2<<20)^(s3<<16)^(s4<<12)^(s5<<8)^(s6<<4)^(s7<<0))&0xffffffff ;
	
	return res ;
}

LL permutation(LL s_32){
	int P[32] = {
		16,  7, 20, 21, 29, 12, 28, 17,  1, 15, 23, 26,  5, 18, 31, 10,
		2,  8, 24, 14, 32, 27,  3,  9, 19, 13, 30,  6, 22, 11,  4, 25
	} ;
	LL res = 0 ;
	int i = 0 ;
	int distance , flag ;
	
	for(i = 0 ; i < 32 ;i++ ){
		distance = 32-P[i] ;
		flag = 1&(s_32>>distance) ;
		res = (res ^ (flag<<(31-i)))&0xffffffff ;
	}
	
	return res ;
	
}

BN F_func(BN s , BN key ){
	LL left = s.head , right = s.tail ;
	BN after_e ;
	BN after_k ;
	LL after_s ;
	LL after_p ;
	BN res ;
	int i = 0 ; 

	after_e = expand_substitution(right) ;

	after_k.head = after_e.head ^ key.head ;
	after_k.tail = after_e.tail ^ key.tail ;
	
	//sºĞ 
	after_s = s_box(after_k) ;
	//pºĞ 
	after_p = permutation(after_s) ;

	res.head = right & 0xffffffff ;
	res.tail = (left ^ after_p) & 0xffffffff ;

	return res ;
}

BN des(BN res ){
	int i = 0 ;
	int round = 0 ;
	LL tmp = 0 ;
	
	for(round = 0 ; round < 16 ; round++){
		res = F_func(res,KEY[round]) ;
	}
	tmp = res.head ;
		res.head = res.tail ;
		res.tail = tmp ;

	
	
	return res ;
}

int main(){
	int T = 0 ;
	char s[19] , k[19] ;
	int i = 0 ;
	BN ans ;
	BN k_64 ;
	
	scanf("%d" , &T ) ;
	scanf("%s" , s ) ;
	scanf("%s" , k ) ;
	
	ans = h2n(s) ;
	k_64 = h2n(k) ;
	
	get_key(k_64) ; 
	
	ans = IP_substitution(ans , 1) ;
	
	for(i = 0 ; i < T; i++){
		ans = des(ans) ;
	}
	
	ans = IP_substitution(ans , 0) ;
	
	printf("0x%08llx%08llx" , ans.head , ans.tail) ;
	
	return 0 ;
}

