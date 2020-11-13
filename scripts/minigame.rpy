init python:

    import math
    import pygame

    CONTROL_WITH_MOUSE = False

    player_speed = 4
    playerx = 0
    playery = 0
    dx = 0
    dy = 0

    player_controls = {
        pygame.K_i : [0, -1, False],
        pygame.K_k : [0, 1, False],
        pygame.K_j : [-1, 0, False],
        pygame.K_l : [1, 0, False]
    }



    class Appearing(renpy.Displayable):

        def __init__(self, child, opaque_distance, transparent_distance, **kwargs):

            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(Appearing, self).__init__(**kwargs)

            # The child.
            self.child = renpy.displayable(child)

            # The distance at which the child will become fully opaque, and
            # where it will become fully transparent. The former must be less
            # than the latter.
            self.opaque_distance = opaque_distance
            self.transparent_distance = transparent_distance

            # The alpha channel of the child.
            self.alpha = 1.0

            # The width and height of us, and our child.
            self.width = 0
            self.height = 0

        def render(self, width, height, st, at):
            global playerx
            global playery

            # Create a transform, that can adjust the alpha channel of the
            # child.
            t = Transform(child=self.child, alpha=self.alpha)

            # Create a render from the child.
            child_render = renpy.render(t, width, height, st, at)

            # Get the size of the child.
            self.width, self.height = child_render.get_size()

            # Create the render we will return.
            render = renpy.Render(self.width, self.height)

            if not CONTROL_WITH_MOUSE:
                playerx = playerx + dx * player_speed
                playery = playery + dy * player_speed

            # Blit (draw) the child's render to our render.
            render.blit(child_render, (playerx, playery))

            renpy.redraw(self, 0)

            # Return the render.
            return render


        # Handles events.
        def event(self, ev, x, y, st):
            global dx
            global dy

            # Set the position of the player
            if CONTROL_WITH_MOUSE:
                playery = y - (self.width/2)
                playerx = -50

            else:
                if ev.type == pygame.KEYDOWN and ev.key in player_controls and not player_controls[ev.key][2]:
                    diffs = player_controls[ev.key]
                    dx = dx + diffs[0]
                    dy = dy + diffs[1]
                    player_controls[ev.key][2] = True
                elif ev.type == pygame.KEYUP and ev.key in player_controls and player_controls[ev.key][2]:
                    diffs = player_controls[ev.key]
                    dx = dx - diffs[0]
                    dy = dy - diffs[1]
                    player_controls[ev.key][2] = False


        def visit(self):
            return [ self.child ]

screen alpha_magic:
    add Appearing("player.png", 100, 200):
        xalign 0.5
        yalign 0.5

label start_game:

    show screen alpha_magic

    if CONTROL_WITH_MOUSE:
        "Use the mouse to control your character"

    else:
        "Use IJKL to control your character"

    hide screen alpha_magic

    return
