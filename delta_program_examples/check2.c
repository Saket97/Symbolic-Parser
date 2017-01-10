#include<stdio.h>
#include<stdlib.h>
struct base
{
	int l;
	int b;
	int area;
};
typedef struct base Base;
void scan(int i,Base* arr)
{
	int len,bre,h;
	scanf("%d%d%d",&len,&bre,&h);
	int j = 3*(i);
	arr[j].l = len;
	arr[j].b = bre;
	arr[j+1].l = bre;
	arr[j+1].b = h;
	arr[j+2].l = len;
	arr[j+2].b = h;
}
void area(Base* arr,int n)
{
	int i = 0;
	for(i=0;i<3*n;++i)
	arr[i].area = (arr[i].l)*(arr[i].b);
}
void merge(Base* arr,int start,int end);

void msort(Base* arr,int start,int end)
{
	if(start >= end)
	return;
	int mid = (start+end)/2;
	if(mid != start)
	msort(arr,start,mid-1);
	if(mid != end)
	msort(arr,mid,end);
	merge(arr,start,end);
}
int lis(Base* arr,int n)
{
	int k = 3*n;
	int len[3*n];
	len[0] = 1;
	int max = 0;
	int i;
	for(i=1;i<k;++i)
	{ 
		//max = 0;
		int j=0;
		for(j=0;j<i;++j)
		{
			if(arr[i].l > arr[j].l && arr[i].b > arr[j].b)
			{
				if(len[j] > max)
				max = len[j];
			}
			
		}
		len[i] = max+1;
	}
	return len[k-1];
}
int main()
{
	int n;
	scanf("%d",&n);
	Base arr[3*n];
	int i=0;
	for(i=0;i<n;++i)
	scan(i,arr);
	area(arr,n);
	msort(arr,0,3*n-1);
//	printf("%d",lis(arr,n));
}
void merge(Base* arr,int start,int end)
{
	if(start == end)
	return;
	int mid = (start+end)/2;
	int n1 = mid - start;
	int n2 = end - mid + 1;
	Base a1[n1],a2[n2];
	int l = 0,r = 0;
	int i = 0;
	
	for(i=0;i<n1;++i)
	a1[i] = arr[start+i];
	
	for(i=0;i<n2;++i)
	a2[i] = arr[mid+i];
	for(i=start;i<=end;++i)
	{
		if(l < n1 && r < n2)
		{
			if(a1[l].area <= a2[r].area)
			{
				arr[i] = a1[l];
				++l;
			}
			else
			{
				arr[i] = a2[r];
				++r
			}
		}
		else
		{
			if(l<n1)
			{
				arr[i] = a1[l];
				++l;
			}
			else
			{
				arr[i] = a2[r];
				++r;
			}
		}
	}
}

int cube(int x)
{
    return x*x*x;
}
void wordCost(int n,int mat[][n],int limit,char** s)
{
    int i=0,j=0;
    for(i=0;i<n;++i)
    {
        for(j=i;j<n;++j)
        {
            if(i == j)
            {
                mat[i][j] = limit - strlen(s[i]);
                continue;
            }
            if(mat[i][j-1] == infinite)
            {
                mat[i][j] = infinite;
                continue;
            }
            if(j)
            {
                mat[i][j] = mat[i][j-1] - strlen(s[j]) - 1;
                continue;
            }
        }
    }
}
void optimalCost(int* c,int n,int mat[][n])
{
    int j=0;
    for(j=0;j<n;++j)
    {
        if(!j)
        {
            c[j] = cube(mat[0][0]);
            continue;
        }
        int min = cube(mat[j][j]),k=0;
        for(k = 1;k<=j;++k)
        {
            if(mat[k][j] == infinite)
            {
                continue;
            }
            if(c[k-1] + cube(mat[k][j]) < min)
            {
                min = c[k-1] + cube(mat[k][j]);
            }
        }
    }
}
void safearr(int* safe,int* arr,int n)
{
    int i=n-1;
    safe[i] = arr[i];
    for(i=n-1;i>=0;--i)
    {
        if(arr[i] == 0)
        i = pos0(arr,safe,i)-1;
        else
        safe[i] = arr[i];
    }
}
int pos0(int* arr,int* safe,int pos)
{
    int count = 0;
    int i = pos;
    safe[i] = arr[i];
    for(i=pos-1;i>=0;--i)
    {
        if(arr[i] == 0)
        return i;
        if(arr[i] > pos-i || count)
        {
            safe[i] = arr[i];
            ++count;
        }
        else
        safe[i] = 0;
    }
    return 0;
}
int min(int x,int y)
{
    if(x<y)
    return x;
    else
    return y;
}
int minjumps(int* safe,int n,int pos,int count,int sum,int lastTaken)
{
	if(pos>=n-1)
	return INT_MAX-2;
    if(safe[pos] == 0)
    return minjumps(safe,n,pos+1,count,sum,lastTaken);
    if(sum >= n-1)
    return count;
    int count1,count2 = INT_MAX;
    
    if(sum + safe[pos] >= n-1)
    count1 = count+1;
    else
    count1 = minjumps(safe,n,pos+1,count+1,sum+safe[pos],pos);
    if(pos && lastTaken + safe[lastTaken] > pos)
    count2 = minjumps(safe,n,pos+1,count,sum,lastTaken);
    //printf("pos:%d %d %d %d\n",pos,count1,count2,sum);
    return min(count1,count2);
}
