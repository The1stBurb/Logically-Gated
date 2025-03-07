import pygame 
import random
# print("12345"[:5])
#re color an image
#DO NOT CHANGE BACK THIS IS BETTER!!!!!!!!!!!!!!!!!!!!!!
#IT ENABLES LOTS OF STUFFS
class pb:
    def __init__(self,screen,font):
        self.moveBy=[0,0]
        self.screen=screen
        self.font=font
    def colorize(self,image, new_color):
        tinted = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        tinted.fill(new_color)
        tinted.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
    def transparent(self,image,level):
        return image.fill((255, 255, 255, 0 if level<0 else (255 if level>255 else level)), special_flags=pygame.BLEND_RGBA_MULT)
    def greyscale(self,surface):
        width, height = surface.get_size()
        grayscale = pygame.Surface((width, height), pygame.SRCALPHA)
        
        for x in range(width):
            for y in range(height):
                r, g, b, a = surface.get_at((x, y))
                L = 0.3 * r + 0.59 * g + 0.11 * b
                grayscale.set_at((x, y), (int(L), int(L), int(L), a))
        
        return grayscale
    def recolour(self,image, new_color):
        # Create a copy of the original image
        recolored = image.copy()
        
        # Get the dimensions of the image
        width, height = image.get_size()
        
        # Lock the surface for pixel manipulation
        recolored.lock()
        
        # Iterate through each pixel
        for x in range(width):
            for y in range(height):
                # Get the current pixel color
                current_color = image.get_at((x, y))
                
                # Calculate the intensity (assuming R, G, and B are equal in greyscale)
                intensity = current_color.r / 255.0
                
                # Calculate the new color components
                new_r = int(new_color[0] * (1 - intensity))
                new_g = int(new_color[1] * (1 - intensity))
                new_b = int(new_color[2] * (1 - intensity))
                
                # Set the new color
                recolored.set_at((x, y), (new_r, new_g, new_b, current_color.a))
        
        # Unlock the surface
        recolored.unlock()
        
        return recolored
    #resize an image
    def resize(self,img,w,h):
        return pygame.transform.scale(img,(w,h))
    #rotate an image
    def rot90(self,img,r):
        # if r==-1:
        #     r=random.randint(0,3)*90
        return pygame.transform.rotate(img,r*90)
    def rotate_image(self,image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    #create a rectanngle
    def rect(self,x,y,w,h,col=(255,255,255),width=0,radius=-1):
        # print(col)
        if len(col)==3:
            col=col+(255,)
        srfce=pygame.Surface((w,h),pygame.SRCALPHA)
        pygame.draw.rect(srfce, col,(0,0, w, h),width=width,border_radius=radius)
        self.screen.blit(srfce,(x+self.moveBy[0], y+self.moveBy[1]))
    #write text
    def text(self,txt,x,y,col=(0,0,0)):
        self.screen.blit(self.font.render(str(txt), True, col),(x+self.moveBy[0],y+self.moveBy[1]))
    #make a quadrilateral
    def quad(self,x1,y1,x2,y2,x3,y3,x4,y4,col=(255,255,255)):
        pygame.draw.polygon(self.screen, col, [(x1+self.moveBy[0],y1+self.moveBy[1]),(x2+self.moveBy[0],y2+self.moveBy[1]),(x3+self.moveBy[0],y3+self.moveBy[1]),(x4+self.moveBy[0],y4+self.moveBy[1]),])
    #blit an image
    def image(self,img,x=0,y=0):
        self.screen.blit(img,(x+self.moveBy[0],y+self.moveBy[1]))
    def line(self,x1,y1,x2,y2,col=(0,0,0),width=1):
        pygame.draw.line(self.screen, col, (x1+self.moveBy[0],y1+self.moveBy[1]), (x2,y2), width=width)
    def circle(self,x=0,y=0,width=10,col=(0,0,0)):
        pygame.draw.circle(self.screen, col, (x+self.moveBy[0],y+self.moveBy[1]), width, width=0)
    #pull image form path
    def gitImg(self,path):
        return pygame.image.load(path).convert_alpha()
    #pull image and resize lol
    def imgGit(self,path,w,h):
        return self.resize(self.gitImg(path),w,h)
    def translate(self,x,y):
        self.moveBy=[x,y]
    def pop(self):
        self.moveBy=[0,0]
    def flip(self):
        pygame.display.flip()