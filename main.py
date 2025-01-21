from machine import Pin
import time
#import gc

#import Filtro_Kalman1 as FK
import PID_Controller1 as PID
import RRT_Searh as RRT
import Mapping as MP
import Control
import Wheels_motor_drivers as WMdrivers
import ReceiveUartData as Receiver

#gc.collect()
########## DATOS ##########
bot = 0
gps_module = 0
imu_module = 0
ultrasonic_sensor = 0
kalman = 0

# Configuracion de la dimencion del entorno
tile_size = 10
width =  500
height = 500
destiny_position = (38.71, -2.89)

########## INSTANCIA DE CLASES ##########
# Congigutacion del controlador de movimento
pid_controller = PID.PIDController()
driver = WMdrivers.wheels_motor_drives(bot,0,0)

#Inicializacion del recividor UART
receiver = Receiver.UARTData(9600,4,5,gps_module,imu_module,ultrasonic_sensor)

#Inicializacion del mapa y el mapeo
#my_map = MP.Map()
my_map = 0
#mapping = MP.Mapping(my_map,receiver)
mapping = 0


# # Inicializar el Filtro de Kalman
# dt = 1/60.0  # Intervalo de tiempo (60 FPS)
# kalman = FK.KalmanFilter(dt=dt,
#                       process_variance=1e-4, 
#                       measurement_variance_gps=1e-2, 
#                       measurement_variance_imu=1e-2)

## INICIALIZACION DE LA CLASE CONTROLADOR ##
distancia_entre_nodos = 15
controlador = Control.Controlador(destiny_position, 
                                  tile_size, 
                                  width, 
                                  height,  
                                  my_map, 
                                  pid_controller, 
                                  kalman,
                                  distancia_entre_nodos,
                                  driver,
                                  receiver)

activar = Pin(20,Pin.IN,Pin.PULL_UP)

while(1):
#     receiver.refresh_data()
#     x,y,angle,distance = receiver.get_data()
#     print(f'{x} {y} {angle} {distance} {activar.value()}\n')
    
    if(activar.value()==0):
        #gc.collect()
        controlador.controlar_mov()
        #controlador.generate_new_path()
        #mapping.map_the_space()
        time.sleep(1)
        
        

    

