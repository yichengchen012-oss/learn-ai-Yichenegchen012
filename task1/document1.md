# Python 语法和编程技巧
## 基础容器：List（列表）、Dict（字典）的使用技巧
粗略关系图

    可迭代对象
    ├── 序列 sequence
    │   ├── 列表 list
    │   ├── 元组 tuple
    │   ├── 字符串 str
    │   └── range
    ├── 映射 mapping
    │   └── 字典 dict
    └── 集合 set
        ├── set
        └── frozenset

### List（列表）
列表索引：可以用负数索引

    a=[1,2,3]
    a[-1]
    3

列表切片：[起始：结尾：步进]

    a=[1,2,3,4,5]
    a[1:4:2]
    [2,4]
    a[::-1]
    [5,4,3,2,1]

增、删、改、查

    #增
    a=[1,2]
    a.attend(3)
    a.extend[4,5]
    #extend 用于可迭代对象
    a.insert(0,-1)
    a=[-1,1,2,3,4,5]

    #删
    a=[1,2,1,3,5]
    a.remove(1)
    a=[2,1,3,5]
    a.pop(2)
    a=[2,1,5]
    a.clear()
    a=[]
    
    #改
    a=[1,2,3]
    a[0]=0
    a[3:]=[4,5]
    a=[0,2,3,4,5]
    #排序
    a=[3,2,9,5,3]
    a.sort()
    a=[2,3,3,5,9]
    #倒序
    a=[2,3,3,5,9]
    a.reverse()
    a=[9,5,3,3,2]
    
    #查
    a=[9,5,3,3,2]
    a.count(3)
    2
    #查找参数个数
    a.index(3)
    2
    #查找参数下标
    a.index(3,3,4)
    3
    a。index(参数，start，end)

    #拷贝(浅拷贝)
    a_copy_1=a.copy()

浅拷贝：只拷贝一维列表
![ ](images\4.png )
对应的深拷贝：

    import copy
    x=[[1,2,3],[4,5,6],[7,8,9]]
    y=copy.deepcopy(x)
    x[1][1]=0
    x
    [[1,2,3],[4,0,6],[7,8,9]]
    y
    [[1,2,3],[4,5,6],[7,8,9]]

列表推导式[expression for target in iterable]

    a=[[1,2,3],[4,5,6],[7,8,9]]
    zhongxiang=[row[1] for row in a]
    zhongxiang
    [2,5,8]

    even=[i for i in range(10) if i%2==0]

    flatten=[col for row in matrix for col in row]
    flatten
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #等效（大循环在前，小循环在后）
    for row in matrix: 
        for col in row: 
            flatten.append(col)
    flatten
    [1, 2, 3, 4, 5, 6, 7, 8, 9]

### Dict（字典）
键值对，左键右值

增、删、改、查

    #增
    d=dict.fromkeys(iterable[,values])

    #删
    d=dict.fromkeys(range(1,4),10)
    d.pop(1)
    10
    d
    {2: 10, 3: 10}
    #随机删除
    d.popitem()
    del.d[2]
    {3: 10}
    #删除字典
    del.d
    #清空字典
    d.clear()

    #改
    d.update({1:1000,2:100})

    #查
    d=dict.fromkeys(range(1,4),10)
    d.get(0,"没有0")
    '没有0'
    #查并改(有则返回值，无则存入并返回给定的值)
    d.setdefault("C","ccc")
    #获得视图对象（会实时随字典改变）
    keys=d.keys()
    values=d.values()
    items=d.items()
    keys
    dict_keys([1, 2, 3])
    values
    dict_values([10, 10, 10])
    items
    dict_items([(1, 10), (2, 10), (3, 10)])

## 函数：Lambda 匿名函数、Decorator 装饰器

### Lambda 匿名函数
lambda arg1,arg2,arg3, …… argN:expression

    def X(x):
        return x*x
    X(3)
    9
    Y=lambda x:x*x
    Y(3)
    9

### Decorator 装饰器
闭包：
1. 利用嵌套函数的外层作用域具有记忆能力的特性，让数据保存在外层函数的参数或变量中
2. 将内层函数作为返回值返回

在此基础上将一个函数作为参数传递给另一函数即为装饰器。

    def call_counter(function):
    count = 0

        def inner():
            function()
            nonlocal count
            count += 1
            return count

    return inner

    @call_counter
    def my_function():
        print("Function called")

    for i in range(5):
        print(my_function())

## 面向对象：Class（类）与 Magic Methods（魔法方法），以及 OOP（面向对象编程）的思想
### Class（类）
类中的方法默认的第一个参数都是 self 即实例本身。

构造函数： __init__ 自动初始化实例对象

钻石继承
![ ](images\2.png)
![ ](images\1.png)
![ ](images\3.png)

私有变量：__x 用于不想被外界访问的变量，实现逻辑是在开头+_类名

    __slots __:规定只能有固定的属性

 ### Magic Methods（魔法方法）
 拦截
 
    __init__
    __new__
    __del__