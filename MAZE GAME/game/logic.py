import random
import copy

class CellType:
    EMPTY = "empty"
    HERO = "hero"
    DEVIL = "devil"
    REWARD = "reward"
    FIRE = "fire"

class Game:
    def __init__(self, size=10, level=1, score=0):
        self.size = size
        self.level = level
        self.score = score
        self.target_score = self.random_target_score()
        self.status = "Playing"
        self.hero = [0, 0]
        self.devil = [size - 1, size - 1]
        self.rewards = {}
        self.fires = {}  # Fires stored with their penalty (1 for -5, 2 for -10)
        self.generate_maze()

    def random_target_score(self):
        # Adjust target score based on the level
        if self.level == 1:
            return random.randint(20, 30)  # Easy
        elif self.level == 5:
            return random.randint(30, 35)  # Hard
        else:
            return random.randint(25,30)  # Medium difficulty

    def generate_maze(self):
        self.grid = [[CellType.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.grid[self.hero[0]][self.hero[1]] = CellType.HERO
        self.grid[self.devil[0]][self.devil[1]] = CellType.DEVIL

        # Generate rewards with varying difficulty based on the level
        reward_count = 10 + self.level * 2  # Increase rewards per level
        for _ in range(reward_count):
            while True:
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                if self.grid[x][y] == CellType.EMPTY:
                    value = random.choice([5, 10, 15])
                    self.rewards[(x, y)] = value
                    self.grid[x][y] = CellType.REWARD
                    break

        # Generate fire hazards with varying difficulty based on the level
        fire_count = 5 + self.level * 2  # Increase fire hazards per level
        fire_type = 1  # Start with fire type 1
        for _ in range(fire_count):
            while True:
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                if self.grid[x][y] == CellType.EMPTY:
                    self.fires[(x, y)] = fire_type  # Store the fire type (1 or 2)
                    self.grid[x][y] = CellType.FIRE
                    fire_type = 2 if fire_type == 1 else 1  # Toggle between fire type 1 and 2
                    break

    def move_hero(self, direction):
        if self.status != "Playing":
            return self.state()

        # Direction map
        dx, dy = {
            "up": (-1, 0), "down": (1, 0),
            "left": (0, -1), "right": (0, 1)
        }[direction]

        new_x, new_y = self.hero[0] + dx, self.hero[1] + dy

        # Valid move check
        if 0 <= new_x < self.size and 0 <= new_y < self.size:
            self.grid[self.hero[0]][self.hero[1]] = CellType.EMPTY
            self.hero = [new_x, new_y]

            # Collect reward if on reward cell
            if tuple(self.hero) in self.rewards:
                self.score += self.rewards.pop(tuple(self.hero))
            # Apply penalty if on fire
            elif tuple(self.hero) in self.fires:
                fire_type = self.fires[tuple(self.hero)]
                penalty = -5 if fire_type == 1 else -10
                self.score += penalty

            self.grid[new_x][new_y] = CellType.HERO
            self.move_devil()  # Move the devil after the hero moves
            self.check_game_status()  # Check if the game has ended or progressed

        return self.state()

    def move_devil(self):
        # Devil moves towards the hero
        dx = 1 if self.devil[0] < self.hero[0] else -1 if self.devil[0] > self.hero[0] else 0
        dy = 1 if self.devil[1] < self.hero[1] else -1 if self.devil[1] > self.hero[1] else 0

        self.grid[self.devil[0]][self.devil[1]] = CellType.EMPTY
        self.devil[0] += dx
        self.devil[1] += dy
        self.grid[self.devil[0]][self.devil[1]] = CellType.DEVIL

    def check_game_status(self):
        # Check for game over condition (when the devil catches the hero)
        if self.hero == self.devil:
            self.status = "Game Over"
        # Check if the player has reached or exceeded the target score to finish the game
        elif self.score >= self.target_score:
            if self.level >= 5:
                self.status = "Victory"  # Player wins after level 5
            else:
                self.level += 1
                self.score = 0
                self.target_score = self.random_target_score()  # Randomize new target score for next level
                self.hero = [0, 0]  # Reset hero position
                self.devil = [self.size - 1, self.size - 1]  # Reset devil position
                self.rewards.clear()  # Clear previous rewards
                self.fires.clear()  # Clear previous fire hazards
                self.generate_maze()  # Generate new maze for the next level

    def state(self):
        return {
            "grid": self.grid,
            "rewards": {f"{x},{y}": v for (x, y), v in self.rewards.items()},
            "fires": {f"{x},{y}": f"Fire {t}" for (x, y), t in self.fires.items()},  # Serialize fires with their type
            "hero": self.hero,
            "devil": self.devil,
            "score": self.score,
            "level": self.level,
            "target_score": self.target_score,
            "status": self.status
        }

    def to_dict(self):
        # Convert set to list for serialization in session
        data = copy.deepcopy(self.__dict__)
        data["fires"] = {f"{x},{y}": f"Fire {t}" for (x, y), t in data["fires"].items()}  # Convert fires with their type
        data["rewards"] = {f"{x},{y}": v for (x, y), v in data["rewards"].items()}  # Convert rewards tuples to strings
        return data

    @staticmethod
    def from_dict(data):
        game = Game(data["size"], data["level"], data["score"])
        data = copy.deepcopy(data)
        data["fires"] = {tuple(map(int, k.split(','))): int(v.split()[-1]) for k, v in data["fires"].items()}  # Convert back fires
        data["rewards"] = {tuple(map(int, k.split(','))): v for k, v in data["rewards"].items()}  # Convert reward keys back to tuples
        game.__dict__.update(data)
        return game
