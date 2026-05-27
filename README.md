# 芒果方块 - Tetris Pro 🎮

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Library](https://img.shields.io/badge/library-Pygame--2.x-green.svg)](https://www.pygame.org/)

一个基于 Python + Pygame 开发的经典俄罗斯方块重制版。项目采用面向对象设计，不仅完美还原了经典方块的消除与碰撞逻辑，还融入了霓虹科技风的视觉动效与动态动态难度加速机制。

---

## 🚀 项目亮点与技术实现

作为独立开发者，我完成了从架构设计到核心算法编写的完整流程，核心技术点包括：

* **面向对象架构 (OOP)：** 独立设计 `Tetromino`（方块）类，封装了方块的矩阵状态、颜色属性，将渲染驱动、物理碰撞与核心状态机进行解耦。
* **矩阵旋转与精准碰撞检测：** * 通过 `zip(*matrix[::-1])` 巧妙实现方块矩阵的顺时针 $90^\circ$ 旋转。
    * 设计了前置预测算法 `can_move()`，在方块实际发生位移/旋转前，预先计算目标坐标与二维地图网格（Grid Matrix）的边界及既有方块的重合度，完美解决“穿墙”与“越界”的 Bug。
* **动态难度机制 (Dynamic Speed Scaling)：** 实现了经典的行消除得分梯队（单行100/双行300/三行500/四行800），并引入**动态定时器更新机制**。每消除 5 行自动提升 Level，通过调整 `FALL_EVENT` 的触发间隔（最高可达 100ms/格），实现游戏难度的平滑递增。
* **现代化 HUD 渲染：** 使用 Pygame 游戏主循环（Game Loop）控制 60 帧稳定渲染。重构了侧边栏 HUD 面板，支持街机风格的 6 位数分数补齐（`zfill(6)`），并加入了关节感方块边缘绘制，提升视觉体验。

---

## 📸 游戏画面 (Screenshots)



![游戏主界面]("C:\Users\wu\Desktop\mango\game1.png")

---

## 🛠️ 控制指南 (Controls)

游戏右侧自带高科技 HUD 提示，核心操作如下：
* `▲` 键：变形 (Rotate)
* `◀` / `▶` 键：左右移动
* `▼` 键：加速下落
* `Ctrl + C`：退出游戏

---

## 📦 快速开始 (Quick Start)

### 1. 克隆仓库
```bash
git clone [https://github.com/](https://github.com/)[Anmicius]/[mango].git
cd [mango]