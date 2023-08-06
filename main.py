import time

class Constants:
    # pixels
    blank_pixel = {'r': 0, 'g': 0, 'b': 0, 'a': 0}
    black_pixel = {'r': 83, 'g': 83, 'b': 83, 'a': 255}
    dino_eye_color = {'r': 255, 'g': 255, 'b': 255, 'a': 255}

    # moves
    m_jump = 'M_JUMP'
    m_duck = 'M_DUCK'
    m_space = 'M_SPACE'

    # states
    state_airborne = 'S_AIRBONE'
    state_ground = 'S_GROUND'
    state_duck = 'S_DUCK'

    # dimensions
    width = 600  # Update with the correct width
    height = 150  # Update with the correct height

    # reference positions
    ground_y = 131
    dino_end_x = 70

    # position of dino eye in running state
    dino_eye_x = 50
    dino_eye_y = 99

    # position of dino eye in duck state
    dino_duck_eye_x = 68
    dino_duck_eye_y = 116

    # position to look for birds in
    mid_bird_x = 75 + 5
    mid_bird_y = 98 - 10

    # interval between bot function runs (in seconds)
    run_interval_ms = 0.05

    # look ahead configurations
    look_ahead_x = 70 + 5
    look_ahead_y = 131 - 10

    look_down_width = 60
    look_down_start_x = 10
    look_down_start_y = 131 - 10

    mid_bird_look_ahead = 50

# Simulate the canvas and context with dummy functions for demonstration
class DummyContext:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getImageData(self, x, y, width, height):
        # Simulate the image data here
        return []

canvas = DummyContext(Constants.width, Constants.height)

# Game logic
class Game:
    def __init__(self):
        self.ctx = DummyContext(Constants.width, Constants.height)
        self.current_dino_state = Constants.state_ground
        self.state_commanded = False
        self.old_dino_state = Constants.state_ground
        self.current_time = 0
        self.current_look_ahead_buffer = None
        self.current_bird_look_ahead_buffer = None

    def run(self):
        while True:
            self.play()

    def play(self):
        self.current_look_ahead_buffer = self.get_look_ahead_buffer(self.current_time)
        self.current_bird_look_ahead_buffer = self.get_look_ahead_buffer_bird(self.current_time)

        image_data = self.ctx.getImageData(0, 0, Constants.width, Constants.height)

        eye_pixel = self.get_pixel(image_data, Constants.dino_eye_x, Constants.dino_eye_y)
        eye_pixel_duck = self.get_pixel(image_data, Constants.dino_duck_eye_x, Constants.dino_duck_eye_y)

        if self.is_pixel_equal(eye_pixel, Constants.dino_eye_color):
            self.current_dino_state = Constants.state_ground
        elif self.is_pixel_equal(eye_pixel_duck, Constants.dino_eye_color):
            self.current_dino_state = Constants.state_duck
        else:
            self.current_dino_state = Constants.state_airborne

        look_forward_danger = False
        for i in range(0, self.current_look_ahead_buffer, 2):
            if self.is_pixel_equal(self.get_pixel(image_data, Constants.look_ahead_x + i, Constants.look_ahead_y), Constants.black_pixel):
                look_forward_danger = True
                break

        if self.current_dino_state == Constants.state_ground:
            if look_forward_danger and not self.state_commanded:
                self.issue_move(Constants.m_jump)
                self.state_commanded = True
                print('JUMP!')
            else:
                bird_danger = False
                for i in range(Constants.mid_bird_x, Constants.mid_bird_x + self.current_bird_look_ahead_buffer, 2):
                    if self.is_pixel_equal(self.get_pixel(image_data, i, Constants.mid_bird_y), Constants.black_pixel):
                        bird_danger = True
                        break
                if bird_danger:
                    self.issue_move(Constants.m_duck, 0.4)
                    print('DUCK!')

        if self.old_dino_state != self.current_dino_state:
            self.state_commanded = False

        self.old_dino_state = self.current_dino_state
        self.current_time += Constants.run_interval_ms * 1000

        print({
            'currentDinoState': self.current_dino_state,
            'lookForwardDanger': look_forward_danger,
            'birdDanger': bird_danger,
            'stateCommanded': self.state_commanded,
            'currentTime': self.current_time,
            'lookAheadBuffer': self.current_look_ahead_buffer,
            'birdLookAhead': self.current_bird_look_ahead_buffer,
        })

    def issue_move(self, move, timeout=None):
        if move == Constants.m_jump:
            if timeout is None:
                timeout = 0.085
            self.issue_key_press('keydown', 38)
            time.sleep(timeout)
            self.issue_key_press('keyup', 38)
        elif move == Constants.m_duck:
            if timeout is None:
                timeout = 0.2
            self.issue_key_press('keydown', 40)
            time.sleep(timeout)
            self.issue_key_press('keyup', 40)
        else:
            print(f'Invalid move {move}')

    def issue_key_press(self, type_, keycode):
        # Simulate issuing a key press here
        pass

    def get_look_ahead_buffer(self, time):
        if time < 40000:
            return 62
        elif time < 60000:
            return 92
        elif time < 70000:
            return 110
        elif time < 85000:
            return 120
        elif time < 100000:
            return 135
        elif time < 115000:
            return 150
        elif time < 140000:
            return 180
        elif time < 170000:
            return 190
        return 190

    def get_look_ahead_buffer_bird(self, time):
        if time < 50000:
            return 50
        return 70

    def get_pixel(self, img_data, x, y):
        data_start = (x + y * Constants.width) * 4
        return {
            'r': img_data[data_start],
            'g': img_data[data_start + 1],
            'b': img_data[data_start + 2],
            'a': img_data[data_start + 3]
        }

    def is_pixel_equal(self, p1, p2):
        return p1['r'] == p2['r'] and p1['g'] == p2['g'] and p1['b'] == p2['b'] and p1['a'] == p2['a']

game = Game()
game.run()
