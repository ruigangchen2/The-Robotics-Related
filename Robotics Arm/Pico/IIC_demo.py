import machine

# Create I2C object
i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))  #GP16 GP17

# Print out any addresses found
devices = i2c.scan()

if devices:
    for d in devices:
        print(hex(d))   #0x68 是 mpu9250地址， 0x76是气压计地址
        
