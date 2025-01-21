from machine import Pin

pin10 = Pin(10, Pin.OUT) 
pin11 = Pin(11, Pin.OUT)
pin12 = Pin(12, Pin.OUT)

pin10.value(1) 
pin11.value(1)
pin12.value(1)

class wheels_motor_drives:
    def __init__(self, bot, vr, vl):
        self.bot = bot
        self.vr = vr
        self.vl = vl

    def control_driver(self, new_vr, new_vl):
        self.vr = new_vr
        self.vl = new_vl

        #SOLO PARA LA SIMULACION
#         self.bot.rueda_izquierda = self.vl
#         self.bot.rueda_derecha = self.vr
        
        #PARA EL PICO 
        if(self.vl>0 and self.vr>0):
            #ADELANTE
            pin10.value(0) 
            pin11.value(0)
            pin12.value(1)
        elif(self.vl<0 and self.vr>0):
            #DERECHA
            pin10.value(0) 
            pin11.value(1)
            pin12.value(1)
        elif(self.vl>0 and self.vr<0):
            #DERECHA
            pin10.value(1) 
            pin11.value(0)
            pin12.value(1)
        elif(self.vl<0 and self.vr<0):
            #ATRAS
            pin10.value(1) 
            pin11.value(1)
            pin12.value(0)
        else:
            #PARAR
            pin10.value(1) 
            pin11.value(1)
            pin12.value(1)
