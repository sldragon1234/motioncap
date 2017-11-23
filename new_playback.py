# Debug Modules
from __future__ import division
import sys
from pprint import pprint


# Required Modules
import math
import time
import pygame
import datetime
from pygame.locals import *

class InputFileClass:
    def __init__(self, filename):
        self.filename = filename
        self.content = ""
        self.cur_index = 0

        # Read in File Data
        self.readFile()

    def readFile(self):
        handler = open(self.filename)
        raw_content = handler.read()
        handler.close()
        self.content = raw_content.split('\n')
        return self.content

    def getNextIndex(self):
        pass

if __name__ == "__main__":
    # Variables
    filename = "170901.dat"
    cur_index = 0
    x = 50
    y = 50
    width = 5
    height = 90
    drag_flag = False

    # Screen Variables
    screen_width = 640
    screen_height = 600

    # Color Variables
    red = (230,50,50)
    white = (255,255,255)
    black = (0,0,0)
    blue = (40, 50, 180)

    # Slider Variables
    slider_text = ""
    slider_min = 50
    slider_max = screen_width - 100
    slider_thickness = 5
    slider_speed = slider_max / content_len
    slider_index = 0
    slider_delay = .05
    slider_pos = slider_min
    cur_x = slider_min

    # Person Variables
    person_thickness = 2
    person_x = 200
    person_y = 200
    prev_x = 0
    prev_y = 0

    # File Content
    file_class = InputFileClass(filename)
    content = file_class.content
    content_len = len(content)

    # Initalize PyGame
    pygame.init()
    window = pygame.display.set_mode([screen_width, screen_height])
    pygame.font.init()

    while True:
        # Set Background Color
        window.fill(blue)

        # Initalize Moveable Objects
        person = pygame.Rect(person_x, person_y, 5, 100)
        the_circle = pygame.Rect(cur_x, slider_max - slider_min, 5, 5)
        slider_info_time = pygame.font.SysFont('arial', 14)
        slider_info_date = pygame.font.SysFont('arial', 14)
        slider_info_index = pygame.font.SysFont('arial', 14)

        # Listen for user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #if the_circle.collidepoint(event.pos):
                    drag_flag = True
                    mouse_x, mouse_y = event.pos
                    offset_x = cur_x - mouse_x
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag_flag = False

            elif event.type == pygame.MOUSEMOTION:
                if drag_flag:
                    mouse_x, mouse_y = event.pos
                    if mouse_x < slider_min:
                        cur_x = slider_min
                        slider_index = 0
                    elif mouse_x > slider_max + slider_min:
                        cur_x = slider_max + slider_min
                    else:
                        cur_x = mouse_x + offset_x

        # Add Motion to Slider Dot
        if drag_flag is False and cur_x <= (slider_max + slider_min):
            cur_x += slider_speed

        # Moves the slider
        slider_index = int(math.ceil((cur_x - slider_min) / slider_speed))
        the_circle.x = cur_x
        the_circle.move(the_circle.x, the_circle.y)

        # Display Slider
        pygame.draw.rect(window, black, [slider_min, slider_max - slider_min, slider_max, slider_thickness])
        pygame.draw.rect(window, white, person, person_thickness)
        #pygame.draw.circle(window, white, [50, screen_height - 48], 7, 4)
        pygame.draw.circle(window, white, the_circle.center, 7, 4)

        # Move Person
        if drag_flag is False:
            try:
                person_data = content[slider_index].split(',')
                timestamp = person_data[0]
                new_x = person_data[1]
                new_y = person_data[2]
                if new_x > prev_x:
                    person_x = person_x + float(person_data[1])
                else:
                    person_x = person_x - float(person_data[1])

                if new_y > prev_y:
                    person_y = person_y + float(person_data[2])
                else:
                    person_y = person_y - float(person_data[2])

                prev_x = new_x
                prev_y = new_y
            except IndexError:
                pass

        # Convert Timestamp
        curDate = datetime.datetime.fromtimestamp(float(timestamp))
        usetime = curDate.strftime("%H:%M:%S")
        usedate = curDate.strftime("%m-%d-%Y")
        useindex = "Index: " + slider_index.__str__()

        # Display Slider Information
        timetext = slider_info_time.render(usetime, True, white)
        window.blit(timetext, (cur_x - 3, the_circle.y + 10))
        datetext = slider_info_date.render(usedate, True, white)
        window.blit(datetext, (cur_x - 3, the_circle.y + 30))
        indextext = slider_info_index.render(useindex, True, white)
        window.blit(indextext, (cur_x - 3, the_circle.y + 50))

        # Update the Display
        pygame.display.update()
        time.sleep(slider_delay)
