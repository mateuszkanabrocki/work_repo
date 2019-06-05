class one(object):

    def __init__(self, name):
        self.constant = '1'
        self.name = name

two = one('two')
three = one('three')

print(two.name, two.constant)
print(three.name, three.constant)
