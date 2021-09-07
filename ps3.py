#does_drop_dust# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Keilee Northcutt
# Collaborators (discussion): Zoe Pasetsky (pset buddy)
# Time: 7 hours

import math
import random
import matplotlib
#matplotlib.use("TkAgg")

from ps3_visualize import *
import pylab

# === Provided class Position, do NOT change
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

# === Problem 1
class StandardRoom(object):
    """
    A StandardRoom represents a rectangular region containing clean or dusty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dust. The tile is considered clean only when the amount
    of dust on this tile is 0.
    """
    def __init__(self, width, height, dust_amount):
        """
        Initializes a rectangular room with the specified width, height, and
        dust_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dust_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        self.dust_amount = dust_amount
        #create a list to store amount of dust on each tile
        self.tiles = []
        for h in range(self.height):
            self.tiles += [[]]
            for w in range(self.width):
                self.tiles[h] += [dust_amount]
    
    #create new function to set dust on each tile
    def set_dust_amount(self, w, h, dust_amount):
        self.tiles[int(h)][int(w)] = dust_amount


    def get_dust_amount(self, w, h):
        """
        Return the amount of dust on the tile (w, h)

        Assumes that (w, h) represents a valid tile inside the room.

        w: an integer
        h: an integer

        Returns: a float
        """
        return self.tiles[int(h)][int(w)]
    
    
    def clean_tile_at_position(self, pos, cleaning_volume):
        """
        Mark the tile under the position pos as cleaned by cleaning_volume amount of dust.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        cleaning_volume: a float, the amount of dust to be cleaned in a single time-step.
                  Can be negative which would mean adding dust to the tile.

        Note: The amount of dust on each tile should be NON-NEGATIVE.
              If the cleaning_volume exceeds the amount of dust on the tile, mark it as 0.
        """
        #get coordinates and dust amounts; if dust is low enough, clean completely; 
        #if there's too much dust, update dust amount after cleaning
        x, y = pos.get_x(), pos.get_y()
        dust = self.get_dust_amount(x, y)
        if cleaning_volume > dust:
            dust = 0
        else: 
            dust -= cleaning_volume
            
        self.set_dust_amount(x, y, dust)

    def is_tile_cleaned(self, w, h):
        """
        Return True if the tile (w, h) has been cleaned.

        Assumes that (w, h) represents a valid tile inside the room.

        w: an integer
        h: an integer

        Returns: True if the tile (w, h) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dust on this
              tile is 0.
        """
        #check if dust amount is 0
        if self.get_dust_amount(w, h) == 0:
            return True
        else:
            return False

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        #start at 0, check every tile and add those that are clean
        clean_tiles = 0
        
        for h in range(self.height):
            for w in range(self.width):
                clean_tiles += self.is_tile_cleaned(w, h)
        
        return clean_tiles

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        #check if coordinates are between 0 and height/width of room
        return 0 <= pos.get_x() < self.width and 0 <= pos.get_y() < self.height

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        #number of tiles is room width times height
        return self.width*self.height

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        #get random coordinates inside room
        x = random.randrange(0, self.width)
        y = random.randrange(0, self.height)
        #create position object with coordinates
        pos = Position(x, y)
        
        return pos


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning_volume.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, cleaning_volume):
        """
        Initializes a Robot with the given speed and given cleaning_volume in the
        specified room. The robot initially has a random direction and a random
        position in the room.

        room:  a StandardRoom object.
        speed: a positive float.
        cleaning_volume: a positive float; the amount of dust cleaned by the robot
                  in a single time-step.
        """
        self.room = room
        self.speed = speed
        self.cleaning_volume = cleaning_volume
        #generate random position and direction to start
        self.position = self.room.get_random_position()
        self.direction = random.randrange(0.0, 360.0)

    def get_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position

    def set_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Moves robot to new position and cleans tile according to robot movement
        rules.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Calculate the next position for the robot.

        If that position is valid, move the robot to that position. Mark the
        tile it is on as having been cleaned by cleaning_volume amount.

        If the new position is invalid, do not move or clean the tile, but
        rotate once to a random new direction.
        """
        #initialize starting position and new position
        current = self.get_position()
        new = current.get_new_position(self.direction, self.speed)
        #if new position is valid, move to tile, reset position, clean tile
        if (self.room).is_position_in_room(new):
            self.set_position(new)
            self.room.clean_tile_at_position(self.get_position(), self.cleaning_volume)
        #if new position isn't valid, try another direction
        else:
            self.set_direction(random.uniform(0.0, 360.0))


# Uncomment this line to see your implementation of StandardRobot in action!
#test_robot_movement(StandardRobot, StandardRoom)

# === Problem 3
class LeakingRobot(Robot):
    """
    A LeakingRobot is a robot that may accidentally drop dust on a tile. A LeakingRobot will
    drop some dust on the tile it's on and pick a new, random direction for itself
    with probability p. If the robot does drop dust, the amount of dropped dust should be a
    decimal value between 0 and 0.5. Afterwards, the robot will behave exactly like the StandardRobot
    by attempting to move to a new tile and clean it.
    """
    p = 0.05

    @staticmethod
    def set_dust_probability(prob):
        """
        Sets the probability of the robot accidentally dropping dust on the tile equal to prob.

        prob: a float (0 <= prob <= 1)
        """
        LeakingRobot.p = prob

    def does_drop_dust(self):
        """
        Answers the question: Does the robot accidentally drop dust on the tile
        at this timestep?
        The robot drops dust with probability p.

        returns: True if the robot drops dust on its tile, False otherwise.
        """
        return random.random() < LeakingRobot.p

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Check if the robot accidentally releases dust. If so, add dust to the current tile
        by a random decimal value between 0 (inclusive) and 0.5 (exclusive) and change
        its direction randomly.

        Calculate the next position for the robot regardless if the robot releases dust or not.

        If that position is valid, move the robot to that position. Mark the tile it moved to
        as having been cleaned by cleaning_volume amount.

        If it is not a valid position, the robot should change to a random direction.

        """
        #initialize starting position
        current = self.get_position()
        #if robot drops dust on tile, add random amount of dust between 0 and 0.5 to dust amount on that tile
        if self.does_drop_dust():
            self.room.clean_tile_at_position(current, -random.uniform(0, 0.5))
        #intialize new position
        new = current.get_new_position(self.direction, self.speed)
        #if new position is valid, move to tile, reset position, clean tile
        if (self.room).is_position_in_room(new):
            self.set_position(new)
            self.room.clean_tile_at_position(self.get_position(), self.cleaning_volume)
        #if new position isn't valid, try another direction
        else:
            self.set_direction(random.uniform(0.0, 360.0))

# Uncomment this line to see your implementation of LeakingRobot in action!
#test_robot_movement(LeakingRobot, StandardRoom)


# === Problem 4
class SpeedyRobot(Robot):
    """
    A SpeedyRobot is a robot that moves extra fast and can clean two tiles in one
    timestep.

    It moves in its current direction, cleans the tile it lands on, and continues
    moving in that direction and cleans the second tile it lands on, all in one
    unit of time.

    If the SpeedyRobot hits a wall when it attempts to move in its current direction,
    it may add dust to the current tile by one unit because it moves very fast and can
    knock dust off of the wall.

    """
    p = 0.15

    @staticmethod
    def set_dust_probability(prob):
        """
        Sets the probability of adding dust to the tile equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        SpeedyRobot.p = prob

    def does_drop_dust(self):
        """
        Answers the question: Does the robot accidentally drop dust on the tile
        at this timestep?
        The robot drops dust with probability p.

        returns: True if the robot drops dust on its tile, False otherwise.
        """
        return random.random() < SpeedyRobot.p

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Within one time step (i.e. one call to update_position_and_clean), there are
        three possible cases:

        1. The next position in the current direction at the robot's given speed is
           not a valid position in the room, so the robot stays at its current position
           without cleaning the tile. The robot then turns to a random direction.

        2. The robot successfully moves forward one position in the current direction
           at its given speed. Let's call this Position A. The robot cleans Position A.
           The next position in the current direction is not a valid position in the
           room, so it does not move to the new location. With probability p, it drops dust on
           Position A by cleaning_volume 1. Regardless of whether or not the robot drops dust on Position A,
           the robot will turn to a random direction.

        3. The robot successfully moves forward two positions in the current direction
           at its given speed. It cleans each position that it lands on.
        """
        #initialize starting position and new positions
        current = self.get_position()
        new1 = current.get_new_position(self.get_direction(), self.speed)
        new2 = new1.get_new_position(self.get_direction(), self.speed)
        #if first position isn't valid, change direction
        if self.room.is_position_in_room(new1) == False:
            self.set_direction(random.uniform(0.0, 360.0))
        #if first position is valid, update position and clean tile
        if self.room.is_position_in_room(new1):
            self.set_position(new1)
            self.room.clean_tile_at_position(new1, self.cleaning_volume)
            #if second position isn't also valid, check if dust is added to tile, change direction
            if self.room.is_position_in_room(new2) == False:
                if self.does_drop_dust():
                    self.room.clean_tile_at_position(new1, -self.cleaning_volume)
                self.set_direction(random.uniform(0.0, 360.0))
            #if second position is also valid, update position, clean tile
            else:
                self.set_position(new2)
                self.room.clean_tile_at_position(new2, self.cleaning_volume)
    

# Uncomment this line to see your implementation of SpeedyRobot in action!
#test_robot_movement(SpeedyRobot, StandardRoom)

# === Problem 5
def run_simulation(num_robots, speed, cleaning_volume, width, height, dust_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each
    with the input speed and cleaning_volume in a room of dimensions width x height
    with the dust dust_amount on each tile. Each trial is run in its own StandardRoom
    with its own robots.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    cleaning_volume: a float (cleaning_volume > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    dust_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                LeakingRobot)
    """
    #create empty list of how long it takes for each trial
    trial_times = []
    #iterate through as many trials as specified
    for t in range(num_trials):
        #begin at 0 time steps for each trial
        time_step = 0
        #create room
        room = StandardRoom(width, height, dust_amount)
        #create a list of every robot working in room
        working_robots = []
        for bot in range(num_robots):
            working_robots.append(robot_type(room, speed, cleaning_volume))
        #infinitely loop 
        while True:
            #iterate through working robot list, update their positions and clean tiles
            for bot in range(len(working_robots)):
                working_robots[bot].update_position_and_clean()
            #check what percentage of the tiles are clean
            percent_clean_tiles = (room.get_num_cleaned_tiles())/(room.get_num_tiles())
            #check if min_coverage has been acheived, if so, break from loop
            if percent_clean_tiles >= min_coverage:
                break
            #update time_step
            time_step += 1
        #once out of loop, add time_step for trial
        trial_times.append(time_step)
    #add up all of the times  
    total = 0
    for time in trial_times:
        total += time
    #return avg time    
    return total/num_trials

#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room?
# the SpeedyRobot is quite a bit faster than the StandardRobot
# which is only slightly faster than the LeakingRobot with 1 robot,
# but the times for each type are much faster and closer as the number
# of robots increase for each type
#
# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions
#       10x30, 20x15, 25x12, and 50x6?
# once again, the SpeedyRobot is much faster than the StandardRobot which is faster
# than the LeakingRobot in every case without much variance in the time differences.
# all of the robot types' cleaning times for each room in order from fastest to slowest
# are 25x15 < 25x12 < 10x30 < 50x6

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, LeakingRobot))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, SpeedyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'LeakingRobot', 'SpeedyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, LeakingRobot))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, SpeedyRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('StandardRobot', 'LeakingRobot', 'SpeedyRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time (steps)')
show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time (steps)')
