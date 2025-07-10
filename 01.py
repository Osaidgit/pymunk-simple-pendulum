import pygame as pg
import pymunk as pu
import pymunk.pygame_util

pg.init()
res=400,400
white=200,200,200
fps=30
clock= pg.time.Clock()
win = pg.display.set_mode(res)



# --- Pymunk setup ---
space = pu.Space()
space.gravity = (0, 500)  # Gravity (x, y)

# Create a static floor
floor_body = pu.Body(body_type=pu.Body.STATIC)
floor_shape = pu.Segment(floor_body, (0, 380), (400, 380), 5)
floor_shape.friction = 1.0
space.add(floor_body, floor_shape)

# Create a dynamic circle
mass = 1
radius = 20
moment = pu.moment_for_circle(mass, 0, radius)
circle_body = pu.Body(mass, moment)
circle_body.position = (200, 50)
circle_shape = pu.Circle(circle_body, radius)
circle_shape.elasticity = 1
space.add(circle_body, circle_shape)

# For drawing pymunk shapes
draw_options = pu.pygame_util.DrawOptions(win)


run=True
while run:
    win.fill(white)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
      # Step the physics
    space.step(1 / fps)

    # Draw all objects
    space.debug_draw(draw_options)
    pg.display.update()
    clock.tick(fps)
pg.quit()    