 
#include <bits/stdc++.h> 
using namespace std; 
 
long long findDigits(int n,int b) 
{ 
	// factorial of -ve number 
	// doesn't exists 
	if (n < 0) 
		return 0; 

	// base case 
	if (n <= 1) 
		return 1; 

	// Use Kamenetsky formula to calculate 
	// the number of digits
	double x = ((n * log10(n / M_E)/log10(b) + 
				log10(2 * M_PI * n) / 
				(2.0*log10(b)))); 

	return floor(x) + 1; 
} 
 
int main() 
{ 
	int x,y,n,t(1);
	//cin>>n;
	scanf("%d",&n);
	while(t<=n){
	//cin>>x>>y;
	scanf("%d %d",&x,&y);
	printf("Case %d: %lld\n",t++,findDigits(x,y));
	//cout <<"Case "<<t++<<": "<<findDigits(x,y)<< endl; 
	}
	return 0; 
} 

