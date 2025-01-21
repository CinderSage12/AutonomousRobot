from machine import Pin, UART
import time
import ultrasonico

class UARTData():
    def __init__(self,Baudrate ,tx_Pin, rx_Pin, GPS_module=0, IMU_module=0, distance_sensor=0):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.distance_to_obstacle = 5
        self.baudrate = Baudrate
        self.tx_Pin = tx_Pin
        self.rx_Pin = rx_Pin
        self.GPS = GPS_module
        self.IMU = IMU_module
        self.distance_sensor = distance_sensor
        self.uart = UART(1, baudrate= self.baudrate, tx=Pin(self.tx_Pin), rx=Pin(self.rx_Pin))
        self.uart.init(bits=8, parity=None, stop=1)

    
    def refresh_data(self):

        ##SOLO PARA SIMULAR
#         self.x, self.y = self.GPS.get_coordenates()
#         self.angle, speed = self.IMU.get_data()
#         self.distance_to_obstacle = self.distance_sensor.display_distance()

        ##PARA EL PICO PI
        x = self.x
        y = self.y
        angle = self.angle
        distance_to_obstacle = self.distance_to_obstacle
        
        if self.uart.any():  #
            data = self.uart.readline().strip()
            values = data.decode('ascii').split(',')
            #data = self.uart.readline().decode('ascii').strip()
            try:
                # Separar los datos y convertirlos a números
                x, y, angle = [float(s) for s in values]#map(float, data.split(","))
            except ValueError:
                x = self.x
                y = self.y
                angle = self.angle
                distance_to_obstacle = self.distance_to_obstacle
            time.sleep(0.1)
        
        else:
            x = self.x
            y = self.y
            angle = self.angle
            distance_to_obstacle = self.distance_to_obstacle
            
        self.x = x
        self.y = y
        self.angle = angle
        self.distance_to_obstacle = ultrasonico.get_distance()

    def get_data(self):
        return self.x, self.y, self.angle, self.distance_to_obstacle
    
    