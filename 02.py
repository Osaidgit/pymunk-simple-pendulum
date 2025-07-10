import pygame
import pymunk
import pymunk.pygame_util


class Pendulum:
    def __init__(self, space, pivot_pos, length=200, bob_radius=20):
        self.space = space
        self.pivot_pos = pivot_pos
        self.length = length
        self.bob_radius = bob_radius

        # Create pivot (static)
        self.pivot_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.pivot_body.position = pivot_pos

        # Create bob (dynamic)
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, bob_radius)
        self.bob_body = pymunk.Body(mass, moment)
        self.bob_body.position = (pivot_pos[0], pivot_pos[1] + length)
        self.bob_shape = pymunk.Circle(self.bob_body, bob_radius)
        self.bob_shape.density = 1
        self.bob_shape.elasticity = 0.9

        # Add bob to space
        self.space.add(self.bob_body, self.bob_shape)

        # Add pin joint
        self.joint = pymunk.PinJoint(self.pivot_body, self.bob_body, (0, 0), (0, 0))
        self.space.add(self.joint)

        # For dragging
        self.mouse_joint = None

    def draw(self, screen):
        # Draw pivot
        pygame.draw.circle(
            screen, (0, 0, 0),
            (int(self.pivot_body.position.x), int(self.pivot_body.position.y)), 5
        )

        # Draw rod
        pygame.draw.line(
            screen, (0, 0, 0),
            self.pivot_body.position,
            self.bob_body.position, 2
        )

        # Draw bob
        pygame.draw.circle(
            screen, (255, 0, 0),
            (int(self.bob_body.position.x), int(self.bob_body.position.y)),
            self.bob_radius
        )

    def start_drag(self, pos):
        """Create a mouse joint to drag the bob."""
        distance = (self.bob_body.position - pos).length
        if distance < self.bob_radius:
            mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            mouse_body.position = pos
            self.mouse_joint = pymunk.PivotJoint(mouse_body, self.bob_body, (0, 0), (0, 0))
            self.space.add(self.mouse_joint)
            self.mouse_body = mouse_body

    def drag(self, pos):
        """Update mouse joint position."""
        if self.mouse_joint:
            self.mouse_body.position = pos

    def end_drag(self):
        """Remove mouse joint."""
        if self.mouse_joint:
            self.space.remove(self.mouse_joint)
            self.mouse_joint = None


class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Movable Pendulum (OOP)")
        self.clock = pygame.time.Clock()
        self.running = True

        # Pymunk space
        self.space = pymunk.Space()
        self.space.gravity = (0, 980)

        # Draw options (not used, manual draw here)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        # Pendulum
        self.pendulum = Pendulum(self.space, pivot_pos=(300, 100))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.pendulum.start_drag(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.pendulum.end_drag()

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    self.pendulum.drag(pos)

    def update(self):
        dt = 1 / 60.0
        self.space.step(dt)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.pendulum.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
