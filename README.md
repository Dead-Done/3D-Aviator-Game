# 🛩️ 3D Aviator Game

A thrilling 3D flight simulation game built with Python and OpenGL, featuring realistic flight physics, dynamic obstacles, and engaging gameplay mechanics.

## 🎮 Game Features

### Core Gameplay
- **Realistic 3D Flight Physics**: Experience authentic airplane movement with pitch, yaw, and roll mechanics
- **Continuous Forward Flight**: Endless gameplay with procedurally managed obstacles
- **Multiple Camera Modes**: Switch between chase, cockpit, and free camera perspectives
- **Dynamic Difficulty**: Progressive level system that increases challenge over time

### Visual Elements
- **Detailed 3D Airplane Model**: Fully rendered aircraft with body, wings, tail, and animated propeller
- **Beautiful Sky Gradient**: Immersive blue sky background
- **Terrain System**: Green landscape with grid lines and varied topography
- **Particle Effects**: Explosion animations and visual feedback

### Game Objects & Obstacles
- **🎯 Rings**: Fly through rings to score points (200 pts each)
- **☁️ Clouds**: Navigate around cloud obstacles
- **🪨 Rocks**: Avoid rocky formations
- **🎈 Balloons**: Dodge colorful balloon clusters
- **✈️ Enemy Aircraft**: Combat AI-controlled enemy planes (100 pts each)
- **⚡ Power-ups**: Collect cyan speed boost cubes

### Combat System
- **Shooting Mechanism**: Fire bullets to destroy enemies and obstacles
- **Collision Detection**: Comprehensive collision system for all game objects
- **Health System**: 3 lives with crash recovery mechanics

### User Interface
- **Comprehensive HUD**: Real-time display of score, lives, speed, and level
- **Game Over Screen**: Restart functionality with score display
- **Control Instructions**: On-screen help for player guidance

## 🎯 Controls

### Flight Controls
| Key | Action |
|-----|--------|
| `W` | Pitch up / Ascend |
| `S` | Pitch down / Descend |
| `A` | Roll left / Move left |
| `D` | Roll right / Move right |
| `Q` | Immediate left movement |
| `E` | Immediate right movement |
| `↑` | Pitch up |
| `↓` | Pitch down |
| `←` | Yaw left |
| `→` | Yaw right |

### Game Controls
| Key | Action |
|-----|--------|
| `SPACE` | Fire bullets |
| `C` | Cycle camera modes (Chase → Cockpit → Free) |
| `X` | Toggle cheat mode (Invincible + Auto-fire) |
| `R` | Restart game |
| `ESC` | Quit game |

### Mouse Controls
- **Left Click**: Fire bullets (alternative to spacebar)

## 🚀 Installation & Setup

### Prerequisites
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### Required Dependencies
- **Python 3.x**
- **PyOpenGL**: 3D graphics rendering
- **PyOpenGL_accelerate**: Performance optimization
- **GLUT**: Window management and input handling (install FreeGLUT if not included with your system or PyOpenGL)

### Running the Game
```bash
# Replace <main_script.py> with the actual entry point when available
python <main_script.py>
```

## 🎮 Gameplay Mechanics

### Scoring System
- **Rings**: 200 points each
- **Enemy Aircraft**: 100 points each
- **Survival Bonus**: Points accumulate over time

### Lives & Health
- Start with 3 lives
- Lose a life when colliding with obstacles or enemies
- Game over when all lives are lost

### Level Progression
- Difficulty increases every 30 seconds
- More enemies spawn at higher levels
- Faster obstacle movement
- Increased challenge and scoring opportunities

### Power-ups
- **Speed Boost**: Cyan cubes provide temporary speed enhancement
- **Duration**: 5-second boost effect
- **Effect**: Increased forward velocity for better maneuverability

### Camera Modes
1. **Chase Camera**: Third-person view following behind the aircraft
2. **Cockpit Camera**: First-person view from pilot's perspective
3. **Free Camera**: Side view for strategic gameplay

## 🛠️ Technical Features

### 3D Rendering
- **OpenGL Integration**: Hardware-accelerated 3D graphics
- **Depth Testing**: Proper 3D object layering
- **Dynamic Lighting**: Realistic lighting effects
- **Smooth Animations**: 60 FPS gameplay experience

### Physics Engine
- **Realistic Flight Dynamics**: Authentic airplane physics simulation
- **Momentum System**: Gradual acceleration and deceleration
- **Collision Detection**: Precise 3D collision algorithms
- **Particle Systems**: Explosion and effect animations

### Performance Optimization
- **Object Recycling**: Efficient memory management for endless gameplay
- **Culling System**: Only render visible objects
- **Optimized Rendering**: Minimal draw calls for smooth performance

## 🎯 Game Strategy Tips

1. **Master the Controls**: Practice smooth flight maneuvers
2. **Plan Your Route**: Look ahead for optimal ring sequences
3. **Combat Tactics**: Use shooting to clear paths through enemies
4. **Power-up Management**: Collect speed boosts strategically
5. **Camera Usage**: Switch cameras for different situations
6. **Risk vs Reward**: Balance safety with high-scoring opportunities

## 🐛 Troubleshooting

### Common Issues
- **Game won't start**: Ensure PyOpenGL is properly installed
- **Poor performance**: Update graphics drivers
- **Controls not responding**: Check keyboard focus on game window

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.6 or higher
- **Graphics**: OpenGL 2.1 compatible graphics card
- **RAM**: 512MB minimum

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New features
- Performance improvements
- Documentation updates

## 📝 Notes for Contributors

- If you are working on Windows and see warnings about line endings (LF/CRLF), consider configuring Git to handle line endings automatically:
  ```bash
  git config --global core.autocrlf true
  ```

**Enjoy your flight adventure! 🛩️✈️**

