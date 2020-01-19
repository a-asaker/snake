#!/usr/bin/env python3
# Coded By :: A_Asaker

from time import sleep
import curses
#import os
import random

#Curses Window Init
stdscr = curses.initscr()
#curses.start_color()
#curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.cbreak()
curses.curs_set(False)
curses.noecho()
stdscr.keypad(1)
stdscr.nodelay(1)

#Terminal Width And Height
height, width = stdscr.getmaxyx()
#  width=os.get_terminal_size(0).columns
#  height=os.get_terminal_size(0).lines

#Print Function For Curses
def print_c(string,attr=None,x=None,y=None):
 args=[i for i in [x,y,string,attr] if i is not None]
 stdscr.addstr(*args)
 stdscr.refresh()

##init vars##
head_shape={"r":">","l":"<","u":"^","d":"v"}
direction=['r','u','d','l'][random.randint(0,3)]
#Random Head Point
head=[random.randint(4,height-4),random.randint(4,width-4)]#head[0]=>y,head[1]=>x
#Speed Of Moving
time=115
#Body Points
body=[[0,0],[0,0],[0,0]]
#Pick A Random 'O' Point
point=[random.randint(1,height-2),random.randint(1,width-2)]
level=1
points=0
last_points=0

#main
try:
 while 1:
  stdscr.border(0)
  stdscr.timeout(time)
#  stdscr.timeout(100)
  height, width = stdscr.getmaxyx()
#  width=os.get_terminal_size(0).columns
#  height=os.get_terminal_size(0).lines
#Capture Pressed keys 
  x=stdscr.getch()
  if x==curses.KEY_UP:
   if direction=="d":pass
   else:direction="u"
  elif x==curses.KEY_DOWN:
   if direction=="u":pass
   else:direction="d"
  elif x==curses.KEY_RIGHT:
   if direction=="l":pass
   else:direction="r"
  elif x==curses.KEY_LEFT:
   if direction=="r":pass
   else:direction="l"
  elif x==ord('q') or x== ord('Q'):break
#Lose If Any Border Is Hit
  if direction=="u":
   if head[0]-1>=1 :head[0]-=1
   else:
    lose=1
    sleep(.5)
    break
  elif direction=="d":
   if head[0]+1<=height-2:head[0]+=1
   else:
    lose=1
    sleep(.5)
    break
  elif direction=="r":
   if head[1]+1<=width-2:head[1]+=1
   else:
    lose=1
    sleep(.5)
    break
  elif direction=="l":
   if head[1]-1>=1:head[1]-=1
   else:
    lose=1
    sleep(.5)
    break
#Lose If You Hit The Body
  if [head[0],head[1]] in body:
   lose=1
   sleep(.5)
   break
#Drawing The Moving Snake(head,body), Tail=body[0]
  [print_c(string="#",x=i[0],y=i[1]) for i in body[::-1]]
  #print_c(string="#",x=body[-1][0],y=body[-1][1])
  print_c(string=" ",x=body[0][0],y=body[0][1])
  del body[0]
  print_c(string=head_shape[direction],y=head[1],x=head[0])
  body.append([head[0],head[1]])
#When The 'O' Is Eaten
  if point[1]==head[1] and point[0]==head[0]:
   body.insert(0,[head[0],head[1]])
   #body.append([head[0],head[1]])
   #print_c(string="#",x=body[-1][0],y=body[-1][1])
   point[0]=random.randint(1,height-2)
   point[1]=random.randint(1,width-2)
   points+=1
#Printing 'O'
  try:
   print_c(string="O",x=point[0],y=point[1])
  except Exception:
#If The Window Is resized , Pick A New Random 'O'
   point[0]=random.randint(1,height-2)
   point[1]=random.randint(1,width-2)
#Level Increasing
  if points-last_points>6:
   time-=15 if time>20 else time
   last_points=points
   level+=1
 # sleep(time)
except Exception:
 pass

#Printing The Final Message
stdscr.clear()
stdscr.border(0)
stdscr.refresh()
win = curses.newwin(round(height/3),round(width/3),round(height/3),round(width/3))
win.border(0)
win.addstr(round(height/6)-3,round(width/6-len("[$] Points : {}".format(points))/2),"[$] Points : {}".format(points))
win.addstr(round(height/6)-1,round(width/6-len("[$] Level : {}".format(level))/2),"[$] Level : {}".format(level))
win.addstr(round(height/6)+1,round(width/6-len("[*] Press Any Key To Exit!")/2)+1,"[*] Press Any Key To Exit")
win.refresh()
win.getch()

#Back To The Default Terminal's Configuration
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
print("\n\t [$] Points : {} \n\t [$] Level : {} \n".format(points,level))
