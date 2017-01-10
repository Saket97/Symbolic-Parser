#include<stdio.h>     
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
	int j = 3*(i);     
}     
void area(Base* arr,int n)     
{     
	int i = 0;     
}     
void merge(Base* arr,int start,int end);     
void msort(Base* arr,int start,int end)     
{     
}     
int lis(Base* arr,int n)     
{     
	int k = 3*n;     
	int len[3*n];     
	int max = 0;     
	int i;     
	{      
		int j=0;     
		{     
			{     
			}     
		}     
	}     
}     
void merge(Base* arr,int start,int end)     
{     
	int mid = (start+end)/2;     
	int n1 = mid - start;     
	int n2 = end - mid + 1;     
	Base a1[n1],a2[n2];     
	int l = 0,r = 0;     
	int i = 0;     
	{     
		if(l < n1 && r < n2)     
		{     
			{     
				++r     
			}     
		}     
		{     
			if(l<n1)     
			{     
			}     
			{     
			}     
		}     
	}     
}     
int cube(int x)     
{     
}     
void wordCost(int n,int mat[][n],int limit,char** s)     
{     
    int i=0,j=0;     
    {     
        for(j=i;j<n;++j)     
        {     
            {     
                mat[i][j] = limit - strlen(s[i]);     
            }     
            if(mat[i][j-1] == infinite)     
            {     
                mat[i][j] = mat[i][j-1] - strlen(s[j]) - 1;     
            }     
        }     
    }     
}     
void optimalCost(int* c,int n,int mat[][n])     
{     
    int j=0;     
    for(j=0;j<n;++j)     
    {     
        {     
        }     
        int min = cube(mat[j][j]),k=0;     
        {     
            if(mat[k][j] == infinite)     
            {     
            }     
        }     
    }     
}     
void safearr(int* safe,int* arr,int n)     
{     
    int i=n-1;     
    {     
        if(arr[i] == 0)     
        safe[i] = arr[i];     
    }     
}     
int pos0(int* arr,int* safe,int pos)     
{     
    int i = pos;     
    {     
        return i;     
    }     
}     
int min(int x,int y)     
{     
}     
int minjumps(int* safe,int n,int pos,int count,int sum,int lastTaken)     
{     
	return INT_MAX-2;     
    int count1,count2 = INT_MAX;     
    if(sum + safe[pos] >= n-1)     
    count1 = count+1;     
}     
