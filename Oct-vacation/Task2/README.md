# Task 2

请补充个人信息后，在此完成报告！

代码：
#include <stdio.h>

int array[8] = {49, 38, 65, 97, 76, 13, 27, 49};
int number = sizeof(array) / sizeof(array[0]);

// 直接插入排序
void Direct_sort(int array[])
{
    for (int i = 1; i < number; i++)
    {
        for (int j = 0; j < i; j++)
        {
            if (array[j] > array[i])
            {
                int sentry = array[i];

                for (int k = i - j; k > 0; k--)
                {
                    array[j + k] = array[j + k -1];
                }
                array[j] = sentry;
                break;
            }
        }
    }
}

int main()
{
    Direct_sort(array);
    for (int i = 0; i < number; i++)
    {
        printf("%d\t", array[i]);
    }
    printf("\n");
    return 0;
}

问题：
1.k--不是k++，发现如果是k++，则在每一次后移时，都需要一个哨兵
2.把array[j] = sentry;放到了k的for循环中了，导致当k > 1时sentry把array[j+1]的值覆盖
3sizeof(array)还以为直接就是数组的个数

@Author:  王兴
@Email:   243286054@qq.com
