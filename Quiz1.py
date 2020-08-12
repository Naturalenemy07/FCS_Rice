#####Question 8#####
import math

def polygon_area(n,s):
    area = (n * s**2)/(4 * math.tan(math.pi/n))
    return area

#print polygon_area(7,3)

#####Question 9#####

def max_of_2(a, b):
    if a > b:
        return a
    else:
        return b

def max_of_3(a, b, c):
    return max_of_2(a, max_of_2(b, c))

#print max_of_3(21, 6, 1)

#####Question 10#####

def project_to_distance(point_x, point_y, distance):
    dist_to_origin = math.sqrt(point_x ** 2 + point_y ** 2)
    scale = distance / dist_to_origin
    print point_x * scale, point_y * scale

#project_to_distance(2, 7, 4)
