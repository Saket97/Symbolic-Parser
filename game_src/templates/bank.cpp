#include <iostream>
#include <stdio.h>
using namespace std;
typedef struct node Node;
struct node
{
	int repeat;
	int control;
	int bank;
	int usr1;
	int usr2;
	int usr3;
	int usr4;
	struct node* left;
	struct node* right;
};
void add_node(Node* root, Node* newnode);
void add(Node* root)
{
	Node* newnode = new Node;
	cin >> newnode->control >> newnode->bank >> newnode->usr1 >> newnode->usr2 >> newnode->usr3 >> newnode->usr4;
	newnode->repeat = 1;
	newnode->left = NULL;
	newnode->right = NULL;
	add_node(root,newnode);

}
void add_node(Node* root, Node* newnode)
{
	Node* tmp = root;
	while(1)
	{
		if(newnode->control > tmp->control)
		{
			if(tmp->right == NULL)
			{
				tmp->right = newnode;
				return;
			}
			else
			{
				tmp = tmp->right;
				continue;
			}
		}
		else
		{
			if(newnode->control < tmp->control)
			{
				if(tmp->left == NULL)
				{
					tmp->left = newnode;
					return;
				}
				else
				{
					tmp = tmp->left;
					continue;
				}
			}
			else
			{
				if(newnode->bank > tmp->bank)
				{
					if(tmp->right == NULL)
					{
						tmp->right = newnode;
						return;
					}
					else
					{
						tmp = tmp->right;
						continue;
					}
				}
				else
				{
					if(newnode->bank < tmp->bank)
					{
						if(tmp->left == NULL)
						{
							tmp->left = newnode;
							return;
						}
						else

						{
							tmp = tmp->left;
							continue;
						}
					}
					else
					{
						if(newnode->usr1 > tmp->usr1)
						{
							if(tmp->right == NULL)
							{
								tmp->right = newnode;
								return;
							}
							else
							{
								tmp = tmp->right;
								continue;
							}
						}
						else
						{
							if(newnode->usr1 < tmp->usr1)
							{
								if(tmp->left == NULL)
								{
									tmp->left = newnode;
									return;
								}
								else
								{
									tmp = tmp->left;
									continue;
								}
							}
							else
							{
								if(newnode->usr2 > tmp->usr2)
								{
									if(tmp->right == NULL)
									{
										tmp->right = newnode;
										return;
									}
									else
									{
										tmp = tmp->right;
										continue;
									}
								}
								else
								{
									if(newnode->usr2 < tmp->usr2)
									{
										if(tmp->left == NULL)
										{
											tmp->left = newnode;
											return;
										}
										else
										{
											tmp = tmp->left;
											continue;
										}
									}
									else
									{
										if(newnode->usr3 > tmp->usr3)
										{
											if(tmp->right == NULL)
											{
												tmp->right = newnode;
												return;
											}
											else
											{
												tmp = tmp->right;
												continue;
											}
										}
										else
										{
											if(newnode->usr3 < tmp->usr3)
											{
												if(tmp->left == NULL)
												{
													tmp->left = newnode;
													return;
												}
												else
												{
													tmp = tmp->left;
													continue;
												}
											}
											else
											{
												if(newnode->usr4 > tmp->usr4)
												{
													if(tmp->right == NULL)
													{
														tmp->right = newnode;
														return;
													}
													else
													{
														tmp = tmp->right;
														continue;
													}
												}
												else
												{
													if(newnode->usr4 < tmp->usr4)
													{
														if(tmp->left == NULL)
														{
															tmp->left = newnode;
															return;
														}
														else
														{
															tmp = tmp->left;
															continue;
														}
													}
													else
													{
														tmp->repeat += 1;
														return;
													}
												}
											}
										}
									}
								}
							}
						}

					}
				}
				
			}	
		}
	}
}
void print(Node* root)
{
	if(root->left)
	{
		print(root->left);
	}
	printf("%.2d %.8d %.4d %.4d %.4d %.4d %d\n",root->control,root->bank,root->usr1,root->usr2,root->usr3,root->usr4,root->repeat );
	if (root->right)
	{
		print(root->right);
	}
}

int main()
{
	int t;
	cin >> t;
	for(int i = 0; i<t; ++i)
	{
		int n;
		// cin >> n;
		scanf("%d\n",&n);
		Node* root = new Node;
		cin >> root->control >> root->bank >> root->usr1 >> root->usr2 >> root->usr3 >> root->usr4;
		root->repeat = 1;
		root->left = NULL;
		root->right = NULL;
		for(int j=1;j<n;++j)
		{
			add(root);
		}
		print(root);
		cout<<endl;
	}
}