import pygame, math
from random import choice

##### MAZE ATTRIBUTES
maze_size = [33,33]

maze_wall_color = 'black'
background_color = 'light grey'
entrance_color = "maroon"
exit_color = entrance_color

trail_color = "maroon"
trail_thickness = 5.5 #Recommended 1-9

maze_size = [maze_size[0]+4,maze_size[1]+4]
wall_thickness = int(10-(max(maze_size)-4)*(2/25))
if wall_thickness <= 0:
    wall_thickness = 1


##### Determine Window's Resolution and Tile Size, Calculate Column/Rows Based On Resolution
TILE = 200
while maze_size[0]*TILE > 1800 or maze_size[1]*TILE > 1000: #Scale the maze's cell size to fit within window frame
    TILE= TILE-1
    
maze_size = (maze_size[0]*TILE+3,maze_size[1]*TILE+3)
RES = WIDTH, HEIGHT = maze_size #Set game's resolution size to be the same size as the maze
cols, rows = WIDTH // TILE, HEIGHT // TILE


##### Initialize Pygame to use Pygame's Functions
pygame.init() 
sc = pygame.display.set_mode(RES) #Set display Windows Width/Height Parameter

##### Construct a Graph made of Individual Interactive Cells
class Cell:
    def __init__(self, x,y): #Determine Cell's Properties: General[Coordinates, Visited],Maze[Walls, Barrier, Entrance, Exit], Runner[Trail, Direction]
        self.x, self.y = x, y
        self.barrier = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.entrance = {'top': False, 'left': False}
        self.exit = {'right': False, 'bottom': False}
        self.visited = False
        self.trail = False
        self.path = {'top': False, 'right': False, 'bottom': False, 'left': False}


    def draw(self): #Determine Cell's Visuals [Width/Height, Border Color]
        x,y = self.x * TILE, self.y * TILE
        
        if self.walls['top']: #Draw Cell's Wall
            pygame.draw.line(sc, pygame.Color(maze_wall_color), (x,y), (x + TILE, y), wall_thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color(maze_wall_color), (x + TILE, y), (x + TILE, y + TILE), wall_thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color(maze_wall_color), (x + TILE, y + TILE), (x, y + TILE), wall_thickness) 
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color(maze_wall_color), (x, y + TILE), (x, y), wall_thickness)
            
        if self.entrance['top']: #Draw Entrance/Exit Beacon
            pygame.draw.ellipse(sc, pygame.Color(entrance_color),(x, y-2*TILE , TILE , TILE))
        if self.exit['right']:
            pygame.draw.ellipse(sc, pygame.Color(exit_color),(x+2*TILE, y , TILE , TILE))
        if self.exit['bottom']:
            pygame.draw.ellipse(sc, pygame.Color(exit_color),(x, y+2*TILE , TILE , TILE))
        if self.entrance['left']:
            pygame.draw.ellipse(sc, pygame.Color(entrance_color),(x-2*TILE, y , TILE , TILE))
        
        scale = trail_thickness/10
        adjust = TILE*(1-scale)/(0.2139*math.log(57.541343*TILE))
        if self.trail and self.path["top"]: #Draw Runner
            pygame.draw.rect(sc, pygame.Color(trail_color), (x+adjust, y-TILE+adjust, TILE*scale, TILE*(1+scale)))
        if self.trail and self.path["right"]:
            pygame.draw.rect(sc, pygame.Color(trail_color), (x+adjust, y+adjust, TILE*(1+scale), TILE*scale))
        if self.trail and self.path["bottom"]:
            pygame.draw.rect(sc, pygame.Color(trail_color), (x+adjust, y+adjust, TILE*scale, TILE*(1+scale)))
        if self.trail and self.path["left"]:
            pygame.draw.rect(sc, pygame.Color(trail_color), (x-TILE+adjust, y+adjust, TILE*(1+scale), TILE*scale))
                
    def check_cell(self, x, y): #Locate a Cell by its Position
        find_index = lambda x,y: x+y*cols
        if x < 0 or x > cols-1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x,y)]
    
    
    def cell_check(self, side): #Locate a Cell by its direction
        if side == "top":
            hole = self.check_cell(self.x, self.y - 1)
        if side == "right":
            hole = self.check_cell(self.x+1, self.y)
        if side == "bottom":
            hole = self.check_cell(self.x, self.y + 1)
        if side == "left":
            hole = self.check_cell(self.x - 1, self.y)
        return hole
    
    
    def check_neighbors(self): #Search For New Cell from current cell by Randomized Choice
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x+1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        list(map(lambda x: neighbors.append(x) if x and not x.visited and not x.barrier else False, [top,right,bottom,left]))
            
        return choice(neighbors) if neighbors else False


    ##### MAZE RUNNER
    def find_path(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x+1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if not self.walls["left"] and not left.visited and not left.barrier:
            true_path(self,3)
            return left
        
        elif not self.walls["top"] and not top.visited and not top.barrier:
            true_path(self,0)
            return top
        elif not self.walls["bottom"] and not bottom.visited and not bottom.barrier:
            true_path(self,2)
            return bottom
        elif not self.walls["right"] and not right.visited and not right.barrier:
            true_path(self,1)
            return right

def true_path(cell,side):
    pathway = ["top","right","bottom","left"]
    next_path = pathway.pop(side)
    cell.path[next_path] = True
    cell.path[pathway[0]] = False
    cell.path[pathway[1]] = False
    cell.path[pathway[2]] = False

        
def remove_walls(current, next): #Remove The Wall between the current and next cell
    def wall_setFalse(a,b):
        current.walls[a], next.walls[b] = False, False
    dx , dy = current.x - next.x, current.y - next.y
    dxd = {1: ['left','right'], -1: ['right','left']}
    dyd = {1: ['top','bottom'], -1: ['bottom','top']}
    
    wall_setFalse(*(dxd.get(dx) or dyd.get(dy)))


def set_barrier(cell):
    cell.barrier = True

    cell.walls["top"] = False
    cell.walls["bottom"] = False
    cell.walls["left"] = False
    cell.walls["right"] = False


def set_walls(cell,sides,bools):
        if sides == "horz":
            cell[0].walls["left"], cell[-1].walls["right"] = bools, bools
        if sides == "vert":
            cell[0].walls["top"], cell[-1].walls["bottom"] = bools, bools


##### Generate the cells to form a graph
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)] #Create a List of Cells with (X,Y) Positions 

##### Define Barriers of graph


list(map(lambda x: list(map(lambda y: set_barrier(grid_cells[x+y]), [0,cols, (rows-1)*(cols),(rows-2)*(cols)])), range(cols))) #Top/Bottom Barriers
list(map(lambda x: list(map(lambda y: set_barrier(grid_cells[x*cols+y]), [0,1, cols-1,cols-2])), range(rows))) #Left/Right Barriers


current_cell = grid_cells[2+2*cols] #Start of the List is cell in top-left corner within the barrier
stack = []


##### Initiate First Move to add to stack
current_cell.visited = True
next_cell = current_cell.check_neighbors() # Visit A New Neighboribng Cell
next_cell.visited = True
stack.append(current_cell)
remove_walls(current_cell, next_cell)
current_cell = next_cell #Make New Cell the current Cell


##### Create Maze with Algorithm
while stack: #Generate Maze until stack is empty
    next_cell = current_cell.check_neighbors() # Visit A New Neighboribng Cell
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell #Make New Cell the current Cell

    elif stack:
        current_cell = stack.pop()
    
    if len(stack) == 0: #Create Entrance/Exit
        if choice([1,2]) == 1: #Top/Bottom
            en_cell = grid_cells[choice(range(2,cols-2))+cols*2]
            ex_cell = grid_cells[choice(range(2,cols-2))+(rows-3)*(cols)]
            
            set_walls([en_cell,ex_cell],"vert",False)
            set_walls([en_cell.cell_check("top")],"horz",True)
            set_walls([ex_cell.cell_check("bottom")],"horz",True)
            
            en_cell.entrance["top"] = True
            ex_cell.exit["bottom"] = True
            
            en_cell.cell_check("top").trail = True
            en_cell.cell_check("top").path["bottom"]=True

        else: #Left/Right
            en_cell = grid_cells[choice(range(2,rows-2))*(cols)+2]
            ex_cell = grid_cells[choice(range(2,rows-2))*(cols)+cols-3]
            
            set_walls([en_cell,ex_cell],"horz",False)
            set_walls([en_cell.cell_check("left")],"vert",True)
            set_walls([ex_cell.cell_check("right")],"vert",True)
            
            en_cell.entrance["left"] = True
            ex_cell.exit["right"] = True
            
            en_cell.cell_check("left").trail = True
            en_cell.cell_check("left").path["right"] = True

def deny_visit(var):
    var.visited = False
list(map(lambda x: deny_visit(x), grid_cells))

current_cell = en_cell

##### Actualize the Game
run_finished = False
while not run_finished:
    
    current_cell.trail = True
    current_cell.visited = True
       
    next_cell = current_cell.find_path() # Visit A New Neighboribng Cell
    if next_cell:
        next_cell.trail = True
        next_cell.visit = True
        stack.append(current_cell)
        current_cell = next_cell #Make New Cell the current Cell
    
    elif stack:
        current_cell.trail = False
        current_cell = stack.pop()

    if any([current_cell.exit["bottom"],current_cell.exit["right"]]):
    
        if current_cell.exit["bottom"]:
            current_cell.path["bottom"] = True
        else:
            current_cell.path["right"] = True
        
        run_finished = True


##### Actualize the Game
while True:
    sc.fill(pygame.Color(background_color)) #Determine BackGround Color
    
    for event in pygame.event.get(): #Retrieve all event that have occurred since this the last time this function was called
        if event.type == pygame.QUIT: #End Loop when Press (X) Button
            exit()
    
    
    [cell.draw() for cell in grid_cells] #Draw The Cell Graph
    
    
    pygame.display.flip() #Update Contents of Entire Display












