# main.py

# 导入环境和学习方法
from env import mlRoboEnv
from DDPG_dropout_small_net import DDPG  #_dropout
import numpy as np
import time

# 设置全局变量
MAX_EPISODES = 40000
MAX_EP_STEPS = 500
ON_TRAIN = False  # True or False
LEARN_START = 2500000
ALPHA = LEARN_START / MAX_EP_STEPS
BELTA = MAX_EPISODES - LEARN_START / MAX_EP_STEPS
VAR = 4  # control exploration
ACTION_NOISE = True

# 设置环境
env = mlRoboEnv()
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound[1]

# 设置学习方法 (这里使用 DDPG)
rl = DDPG(a_dim, s_dim, a_bound, ACTION_NOISE)


t1 = time.time()

# 开始训练
def train():

    for i in range(MAX_EPISODES):

        s = env.reset()                # 初始化回合设置
        ep_r = 0.

        if ACTION_NOISE:
            if i <= LEARN_START / MAX_EP_STEPS:
                var = VAR
            elif i > LEARN_START / MAX_EP_STEPS and i <= (MAX_EPISODES - 1000):

                var = (np.arctan(((MAX_EPISODES-20000) / 2 - i)/2000) / (np.pi / 2) + 1) * (VAR - 2)
            else:
                var = 0

            # var = 0
            # if i <= ALPHA + BELTA * 2 / 3:
            #     if i <= ALPHA + BELTA / 3:
            #         if i <= ALPHA:
            #             var = VAR
            #         else:
            #             if i <= ALPHA + BELTA / 6:
            #                 var = VAR/2
            #             else:
            #                 print(var)
            #     else:
            #         if i <= ALPHA + BELTA * 3 / 6:
            #             var = VAR / 2
            #         else:
            #             print(var)
            # else:
            #     if i <= ALPHA + BELTA * 5 / 6:
            #         var = VAR / 2
            #     else:
            #         print(var)
        else:
            if i <= LEARN_START / MAX_EP_STEPS:
                var = VAR
            else:
                var = 0

        STU_FLAG = 0
        for j in range(MAX_EP_STEPS):

            env.render()                # 环境的渲染
            a = rl.choose_action(s)     # RL 选择动作
            # a = np.clip(np.random.normal(a, var), -2, 2)
            a = np.random.normal(a, var)
            if np.sum(np.absolute(a)) <= 0.0001:
                STU_FLAG += 1
                if STU_FLAG >= 150:
                    print('Ep: %i | %s | ep_r: %.1f | steps: %i' % (i, '---' if not done else 'done', ep_r, j))
                    break
            else:
                STU_FLAG = 0
            a[0:3] = a[0:3] * np.pi/6
            a[3] = a[3] * 20
            s_, r, done, info = env.step(a)   # 在环境中施加动作

            # DDPG 这种强化学习需要存放记忆库
            # if (i * MAX_EP_STEPS + j) < LEARN_START:
            rl.store_transition(s, a, r, s_)

            ep_r += r
            # if rl.pointer > LEARN_START:
            if (i * MAX_EP_STEPS + j) > LEARN_START:
                rl.learn()              # 记忆库满了, 开始学习

            s = s_                      # 变为下一回合
            if done or j == MAX_EP_STEPS - 1:
                print('Ep: %i | %s | ep_r: %.1f | steps: %i' % (i, '---' if not done else 'done', ep_r, j))
                break

        # if i == 5999 or i == 7999:
        #     rl.save()
    rl.save()


def eval():
    rl.restore()
    env.render()
    env.viewer.set_vsync(True)
    i = 0.0
    j = 0
    T = 0.0
    f = open('results.txt', 'a')
    while True:
        s = env.reset()
        ep_r = 0.
        i += 1
        for j in range(300):
            env.render()
            a = rl.choose_action(s)
            # if sum(a) < 0.00001:
            #     a = np.array([0., 0., 0., 0.])
            a[0:3] = a[0:3] * np.pi / 6  # * 2
            a[3] = a[3] * 20  # * 2
            s, r, done, info = env.step(a)
            ep_r += r
            if done or j == 299:
                if done:
                    T += 1
                else:
                    for t in range(len(s)):
                        f.write(str(s[t]))
                        f.write(' ')
                    f.write(str(env.goal['y']))
                    f.write('\n')
                print('Ep: %i | %s | ep_r: %.1f | steps: %i' % (i, '---' if not done else 'done', ep_r, j))
                break
        if i >= 1000:
            accuracy = T / i
            print("Steps accuracy: %f " % (accuracy))
            f.close()
            break


if ON_TRAIN:
    train()
else:
    eval()
