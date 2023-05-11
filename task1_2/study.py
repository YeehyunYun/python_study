# type(class_name, class_parents, class_attributes)
YunYeeHyun = type('', (), {})

def Punch():
    power = 100
    print(power)

# setattr(obj, name, value)
setattr(YunYeeHyun, 'Punch', Punch)

YunYeeHyun.Punch() 