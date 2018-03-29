# coding: utf-8
# handling private data type
# define class
import json
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return 'Person Object name : %s , age : %d' % (self.name, self.age)

    # define transfer functions

def object2dict(obj):
    # convert object to a dict
    d = {'__class__': obj.__class__.__name__, '__module__': obj.__module__}
    d.update(obj.__dict__)
    return d


def dict2object(d):
    # convert dict to object
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        print 'the module is:', module
        class_ = getattr(module, class_name)
        args = dict((key.encode('utf-8'), value) for key, value in d.items())  # get args
        print 'the atrribute:', repr(args)
        inst = class_(**args)  # create new instance
    else:
        inst = d
    return inst


# recreate the default method
class LocalEncoder(json.JSONEncoder):
    def default(self, obj):
        # convert object to a dict
        d = {'__class__': obj.__class__.__name__, '__module__': obj.__module__}
        d.update(obj.__dict__)
        return d


class LocalDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict2object)

    def dict2object(self, d):
        # convert dict to object
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items())  # get args
            inst = class_(**args)  # create new instance
        else:
            inst = d
        return inst
    # test function


if __name__ == '__main__':
    p = Person('秦始皇', 22)
    print '原始数据',p
    # json.dumps(p)#error will be throwed
    d = object2dict(p)
    print '编码数据', d

    o = dict2object(d)
    print '原始数据: %s, obj:%s' % (type(o), repr(o))

    dump = json.dumps(p, default=object2dict)
    print '编码:', dump
    load = json.loads(dump, object_hook=dict2object)
    print '原始:', load
    d = LocalEncoder().encode(p)
    o = LocalDecoder().decode(d)

    print 'recereated encode method: ', d
    print 'recereated decode method: ', type(o), o