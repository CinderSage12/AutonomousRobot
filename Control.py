import math
import RRT_Searh as RRT

class Controlador:
    def __init__(self, destiny_position, tile_size, width, height, map_, PID_Controller, kalman_filter, distance_at_node, driver, receiver_data):
        #self.bot = bot
        self.destiny_position = destiny_position
        self.map = map_
        self.prev_path  = []
        self.current_path = []  # Para almacenar el camino generado
        self.current_target_index = 0  # Para seguir el camino paso a paso
        self.generarar_camino = True
        self.PID_Controller = PID_Controller
        self.kalman_filter = kalman_filter
        self.distance_at_node = distance_at_node
        self.driver = driver
        self.receiver_data = receiver_data 
    
        self.tile_size = tile_size
        self.width = width
        self.height = height
        self.rrt_search = RRT.RRTPatchSearch(self.map, self.tile_size, self.width, self.height, self.distance_at_node)
        self.generate_new_path()

    def filer_state_data(self, gps_posx, gps_posy, vx_imu, vy_imu):
        self.kalman_filter.predict()
        self.kalman_filter.update([gps_posx, gps_posy, vx_imu, vy_imu])
        estimated_pos = self.kalman_filter.get_estimated_position()
        return estimated_pos

    def get_state_data(self):
        # Actualizar el Filtro de Kalman con las mediciones
        # Obtener datos de GPS e IMU

        self.receiver_data.refresh_data()
        x, y, angle, distance_to_obstacle = self.receiver_data.get_data()

        # # Convertir velocidad y ángulo a componentes vx e vy
        #vx = speed * math.cos(angle)
        #vy = speed * math.sin(angle)

        #x, y = self.filer_state_data(x, y, vx, vy)

        return x, y, angle


    def generate_new_path(self):
        xi,yi,theta = self.get_state_data()
        #self.prev_path.append(self.current_path)
        del self.current_path
        self.current_path = self.rrt_search.genere_patch(xi, yi, self.destiny_position)
        # similar = False
        # for path in self.prev_path:
        #     similar = new_path_too_similar(path,self.current_path) 
        #     break
        # if(similar):
        #     self.generate_new_path()

        print(self.current_path)
        self.current_target_index = 0

    def follow_path(self,n):
        if n < len(self.current_path):
            target = self.current_path[self.current_target_index+1]
            xd, yd = target

            x,y,theta = self.get_state_data()

            r_iz, r_der = self.PID_Controller.adjust_wheel_speeds(x, y, xd, yd, theta)

            #self.bot.rueda_izquierda = r_iz
            #self.bot.rueda_derecha = r_der

            self.driver.control_driver(r_der,r_iz)


            distance_to_destiny = math.sqrt((x - self.destiny_position[0])**2 + (y - self.destiny_position[1])**2)
            distance_to_next_node = math.sqrt((x - xd)**2 + (y - yd)**2)

            if distance_to_destiny < 4:
                self.driver.control_driver(0,0)
                print("Chuck a llegado")
            elif distance_to_next_node < 1:
                #print(self.current_target_index)
                self.current_target_index = self.current_target_index +1

    def retroceder(self):
        # Retroceder el bot por un breve período
        self.driver.control_driver(-50,-50)


    def controlar_mov(self):
        self.receiver_data.refresh_data()
        x, y, angle, distance_to_obstacle = self.receiver_data.get_data()
        if distance_to_obstacle < 1:
            # Retroceder antes de recalcular el camino
            self.retroceder()
            self.generarar_camino = True


        elif distance_to_obstacle >= 1:
            if(self.generarar_camino):
                self.generarar_camino = False
                self.generate_new_path()
            self.follow_path(self.current_target_index)