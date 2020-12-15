

#include<stdio.h>
//using namaespace std;
int main()
{ 
	char c[100];
	scanf("%s",c);
	int n,x,y;
	scanf("%d",&n);
	while(n--)
	{
	scanf("%d %d",&x,&y);
	///cin>>x>>y;
	if(y==5||y==6)
		cout<<"YES\n";
	else cout<<"NO\n";
	}
    	return 0;
}
