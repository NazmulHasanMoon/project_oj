

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
		printf("YES\n");//cout<<"YES\n";
	else printf("NO\n");
	}
    	return 0;
}
