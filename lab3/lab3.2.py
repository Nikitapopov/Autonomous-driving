from gym_duckietown.tasks.task_solution import TaskSolution
import numpy as np
import cv2


class DontCrushDuckieTaskSolution(TaskSolution):
    lower_limit = np.array([0, 130, 170])
    upper_limit = np.array([2, 255, 255])

    def __init__(self, generated_task):
        super().__init__(generated_task)

    def check_is_duck_ahead(self, img):
        mask = cv2.inRange(img, self.lower_limit, self.upper_limit)
        contour, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contour:
            _, _, _, h = cv2.boundingRect(contour[0])
            if h > 150:
                return True
        return False

    def change_lanes(self, env, is_oncoming_lane):
        angular = -45 if is_oncoming_lane else 45
        img, _, _, _ = env.step([1, angular])
        env.render()
        for step in range(10):
            img, _, _, _ = env.step([1, 0])
            env.render()
            print('forward')
        img, _, _, _ = env.step([1, -angular])
        env.render()
        print('change angle')

    def solve(self):
        env = self.generated_task['env']
        # getting the initial picture
        img, _, _, _ = env.step([0, 0])

        is_oncoming_lane = False
        condition = True
        while condition:
            img, reward, done, info = env.step([1, 0])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            is_duck_ahead = self.check_is_duck_ahead(img)
            if (is_duck_ahead and not is_oncoming_lane) or (not is_duck_ahead and is_oncoming_lane):
                self.change_lanes(env, is_oncoming_lane)
                is_oncoming_lane = not is_oncoming_lane

            env.render()
