import pygame
import math

class Ball:
    def __init__(self, position:tuple = (0,0), radius:int = 1, color:tuple = (0,0,0), velocity:tuple = (0, 0), elasticity:float = 0.95,drag = 0.99, surface=None):
        self.position = position
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.surface = surface
        self.elasticity = elasticity
        self.drag = drag
    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.position, self.radius)
    def move(self):
        meta_position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        if meta_position[0] - self.radius < 0 or meta_position[0] + self.radius > self.surface.get_width():
            self.X_reverse()
        if meta_position[1] - self.radius < 0 or meta_position[1] + self.radius > self.surface.get_height():
            self.Y_reverse()
        self.velocity = (self.velocity[0]*(self.drag) , self.velocity[1]*(self.drag))
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.draw()
    def Y_reverse(self):          
        self.velocity = (self.velocity[0], (-self.velocity[1])*self.elasticity)
    def X_reverse(self):
        self.velocity = (-self.velocity[0]*self.elasticity, self.velocity[1])


    def check_collision(self, wall):
        """
        Check collision with wall and return collision info.
        Returns: (collision_exists, normal_x, normal_y, overlap_distance)
        """
        # Initialize variables
        collision = False
        normal_x = 0
        normal_y = 0
        overlap = float('inf')
        
        # Find closest point on rectangle to circle center
        points = wall.points
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            
            # Vector from p1 to p2
            edge_x = p2[0] - p1[0]
            edge_y = p2[1] - p1[1]
            
            # Vector from p1 to circle center
            to_circle_x = self.position[0] - p1[0]
            to_circle_y = self.position[1] - p1[1]
            
            # Calculate edge length squared
            edge_length_sq = edge_x**2 + edge_y**2
            
            if edge_length_sq > 0:
                # Project circle center onto edge line (clamped to segment)
                t = max(0, min(1, (to_circle_x * edge_x + to_circle_y * edge_y) / edge_length_sq))
                
                # Closest point on edge segment to circle center
                closest_x = p1[0] + t * edge_x
                closest_y = p1[1] + t * edge_y
                
                # Vector from closest point to circle center
                dist_x = self.position[0] - closest_x
                dist_y = self.position[1] - closest_y
                distance = math.sqrt(dist_x**2 + dist_y**2)
                
                if distance < self.radius:
                    # Collision detected with this edge
                    if distance > 0:
                        # Calculate collision normal (pointing from edge to circle)
                        edge_normal_x = dist_x / distance
                        edge_normal_y = dist_y / distance
                        edge_overlap = self.radius - distance
                    else:
                        # Circle center exactly on edge - use perpendicular to edge
                        edge_normal_x = -edge_y / math.sqrt(edge_length_sq)
                        edge_normal_y = edge_x / math.sqrt(edge_length_sq)
                        edge_overlap = self.radius
                    
                    # Keep the smallest overlap (most penetrating collision)
                    if edge_overlap < overlap:
                        collision = True
                        overlap = edge_overlap
                        normal_x = edge_normal_x
                        normal_y = edge_normal_y
        
        if not collision and self.point_in_polygon(self.position, points):
            # Circle center is inside polygon - find closest edge to push out
            collision = True
            min_dist = float('inf')
            closest_normal_x = 0
            closest_normal_y = 0
            
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]
                
                # Distance from point to line segment
                edge_x = p2[0] - p1[0]
                edge_y = p2[1] - p1[1]
                edge_length = math.sqrt(edge_x**2 + edge_y**2)
                
                if edge_length > 0:
                    # Vector from p1 to circle center
                    to_circle_x = self.position[0] - p1[0]
                    to_circle_y = self.position[1] - p1[1]
                    
                    # Project onto edge
                    t = (to_circle_x * edge_x + to_circle_y * edge_y) / (edge_length**2)
                    t = max(0, min(1, t))
                    
                    # Closest point on edge
                    closest_x = p1[0] + t * edge_x
                    closest_y = p1[1] + t * edge_y
                    
                    # Distance to closest point
                    dist_x = self.position[0] - closest_x
                    dist_y = self.position[1] - closest_y
                    dist = math.sqrt(dist_x**2 + dist_y**2)
                    
                    if dist < min_dist:
                        min_dist = dist
                        if dist > 0:
                            closest_normal_x = dist_x / dist
                            closest_normal_y = dist_y / dist
                        else:
                            # Perpendicular to edge
                            closest_normal_x = -edge_y / edge_length
                            closest_normal_y = edge_x / edge_length
            
            if min_dist < float('inf'):
                overlap = self.radius + min_dist  # Push out by radius + distance
                normal_x = closest_normal_x
                normal_y = closest_normal_y
        
        return collision, normal_x, normal_y, overlap if collision else 0

    def point_in_polygon(self, point, polygon):
        """
        Check if a point is inside a polygon using ray casting algorithm
        """
        x, y = point
        inside = False
        
        for i in range(len(polygon)):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % len(polygon)]
            
            # Check if the point is on a vertex or edge
            if (x == x1 and y == y1) or (x == x2 and y == y2):
                return True
            
            # Check if the point is on the horizontal edge
            if (y1 == y2 and y == y1 and 
                min(x1, x2) <= x <= max(x1, x2)):
                return True
            
            # Ray casting algorithm
            if ((y1 > y) != (y2 > y)):
                x_intersect = (x2 - x1) * (y - y1) / (y2 - y1) + x1
                if x_intersect == x:
                    return True
                if x_intersect > x:
                    inside = not inside
        
        return inside
    
    def resolve_collision(self, wall):
        """Detect and resolve collision with wall"""
        collision, normal_x, normal_y, overlap = self.check_collision(wall)
        
        if collision:
            # Move ball out of collision
            self.position = (
                self.position[0] + normal_x * overlap,
                self.position[1] + normal_y * overlap
            )
            
            # Reflect velocity based on collision normal
            dot_product = self.velocity[0] * normal_x + self.velocity[1] * normal_y
            self.velocity = (
                self.velocity[0] - 2 * dot_product * normal_x ,
                self.velocity[1] - 2 * dot_product * normal_y
            )
            self.velocity = (self.velocity[0] * self.elasticity, self.velocity[1] * self.elasticity)
            return True
        return False