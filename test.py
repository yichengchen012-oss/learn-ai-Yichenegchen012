a=[1,2,3,4,5]
a.extend('6')
print(a)
print(a[1:4:2])
l=len([1,2,3,4])
print(l)
class Test:
    x=100
    def test(self):
        print(self.x)
        #self+=10
        #print(self)
a=Test()
a.test()