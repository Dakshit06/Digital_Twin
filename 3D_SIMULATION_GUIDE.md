# 🎮 CNC Digital Twin - 3D Simulation Guide

## ✨ **NEW FEATURE: Real-Time 3D Machine Simulation!**

Your CNC Digital Twin now includes a **fully interactive 3D visualization** of the machine operating in real-time!

---

## 🎯 **What's New**

### 🏭 **3D CNC Machine Model**

The simulation displays a realistic 3D model with:

1. **Machine Base** (Gray Platform)
   - Solid foundation platform
   - Realistic metallic appearance

2. **X-Axis Rail** (Red)
   - Horizontal movement rail
   - Moves left/right along the X-axis

3. **Y-Axis Carriage** (Green)
   - Moves forward/backward along the Y-axis
   - Carries the Z-axis assembly

4. **Z-Axis Spindle** (Blue)
   - Vertical movement assembly
   - Moves up/down for cutting depth
   - Rotates based on spindle RPM

5. **Cutting Tool** (Yellow)
   - Cone-shaped cutting tool
   - Rotates in real-time with spindle
   - Positioned at end of Z-axis

6. **Workpiece** (Orange)
   - Material being machined
   - Stationary on the machine bed

---

## 🎬 **Live Animation Features**

### Real-Time Position Tracking
- **X Position**: -200 to +200 mm (left/right)
- **Y Position**: -200 to +200 mm (forward/backward)
- **Z Position**: -20 to 0 mm (up/down from top)
- **Spindle RPM**: 1000-7000 RPM rotation speed

### Smooth Animations
- ✅ Smooth interpolation between positions
- ✅ Realistic spindle rotation based on actual RPM
- ✅ Auto-updates every 5 seconds with new data
- ✅ Physics-based movement timing

---

## 🎮 **Interactive Controls**

### Mouse Controls
- **Left Click + Drag**: Rotate camera around machine
- **Right Click + Drag**: Pan camera view
- **Scroll Wheel**: Zoom in/out
- **Double Click**: Focus on machine

### Button Controls
- **🎥 Reset View**: Returns camera to default position
- **⏯️ Pause/Play**: Toggle animation on/off

---

## 📊 **Dashboard Layout**

### Split-Screen Design

**LEFT PANEL (3D Simulation):**
```
┌─────────────────────────┐
│ 🎮 Live 3D Simulation   │
│                         │
│   [Interactive 3D View] │
│                         │
│ Controls: [Reset] [||]  │
│                         │
│ Position Info:          │
│ • X: 125.5 mm          │
│ • Y: -45.2 mm          │
│ • Z: -12.8 mm          │
│ • RPM: 5500            │
└─────────────────────────┘
```

**RIGHT PANEL (Analytics):**
```
┌─────────────────────────┐
│ KPI Cards (8 metrics)   │
│ [RPM] [Temp] [Power]   │
│                         │
│ Charts:                 │
│ • Spindle Speed         │
│ • Temperature           │
│ • Vibration             │
│ • Surface Quality       │
└─────────────────────────┘
```

---

## 🔧 **Technical Details**

### Technologies Used
- **Three.js**: 3D graphics rendering
- **OrbitControls**: Camera manipulation
- **WebGL**: Hardware-accelerated graphics
- **Real-time Data**: Updates from CSV dataset

### Performance
- **60 FPS**: Smooth animation
- **Auto-LOD**: Optimized for performance
- **Responsive**: Works on all screen sizes

---

## 🌐 **How to Access**

### Main 3D Dashboard
```
http://127.0.0.1:5000
```
Features: 3D simulation + analytics

### Classic 2D Dashboard (Optional)
```
http://127.0.0.1:5000/2d
```
Features: Charts only (no 3D)

---

## 📁 **New Files Added**

```
dashboard/
├── static/
│   └── js/
│       └── cnc_simulation.js     ← 3D simulation engine
└── templates/
    └── dashboard_3d.html         ← 3D dashboard page
```

---

## 🎨 **Visual Features**

### Lighting & Effects
- ✅ Ambient lighting for overall illumination
- ✅ Directional lights for shadows
- ✅ Spotlight on work area
- ✅ Realistic metallic materials
- ✅ Soft shadows enabled

### Color Coding
- 🔴 **Red**: X-axis (horizontal movement)
- 🟢 **Green**: Y-axis (depth movement)
- 🔵 **Blue**: Z-axis (vertical movement)
- 🟡 **Yellow**: Cutting tool (active element)
- 🟠 **Orange**: Workpiece (material)

---

## 📖 **Usage Guide**

### Quick Start
1. **Launch**: Run `python run.py`
2. **Open**: Navigate to http://127.0.0.1:5000
3. **Watch**: See your CNC machine operating in real-time!
4. **Interact**: Click and drag to explore the 3D model

### Understanding the Simulation
- The machine animates based on **real data** from your CSV
- Position values are **normalized** to fit the 3D workspace
- Spindle rotation speed matches **actual RPM** from dataset
- Updates automatically every **5 seconds** with latest data

---

## 🎯 **Use Cases**

### Training & Education
- 🎓 Teach CNC machine operation visually
- 📚 Demonstrate axis movements
- 🔍 Show tool positioning

### Monitoring & Analysis
- 👁️ Visualize machine state in real-time
- 📊 Correlate 3D position with analytics
- ⚠️ Identify unusual movement patterns

### Presentations & Demos
- 🖥️ Impressive visual for stakeholders
- 🎬 Record screen for documentation
- 📸 Screenshot machine states

---

## ⚡ **Performance Tips**

### For Best Experience
- Use **Chrome** or **Firefox** for best WebGL support
- Ensure **hardware acceleration** is enabled
- Close unnecessary browser tabs
- Use a **discrete GPU** if available

### If Slow
- Reduce update frequency in code (change from 5s to 10s)
- Lower anti-aliasing quality
- Disable shadows in simulation.js

---

## 🐛 **Troubleshooting**

### 3D View Not Loading
```
Problem: Black screen or "WebGL not supported"
Solution: Enable hardware acceleration in browser settings
```

### Choppy Animation
```
Problem: Stuttering or low FPS
Solution: Close other applications, use simpler scene
```

### Data Not Updating
```
Problem: Machine stuck in one position
Solution: Check dataset exists, verify API endpoint works
```

---

## 🚀 **Advanced Features**

### Camera Presets (Coming Soon)
- Front view
- Side view
- Top view
- Isometric view

### Tool Path Visualization (Planned)
- Draw cutting path
- Show historical positions
- Predict future positions

### Multi-Machine View (Future)
- Display multiple CNC machines
- Compare operations side-by-side

---

## 📊 **Data Integration**

### Position Mapping
```python
CSV Data          →  3D Coordinate
────────────────     ──────────────
X: -200 to 200   →   -8 to 8
Y: -200 to 200   →   -4 to 4
Z: -20 to 0      →   2 to 10
```

### RPM to Rotation
```python
rotation_speed = (RPM / 60000) * 2π
```

---

## 🎉 **Summary**

Your CNC Digital Twin now includes:

✅ **Real-time 3D visualization** of machine operations  
✅ **Interactive controls** for camera manipulation  
✅ **Live data integration** from actual CSV dataset  
✅ **Professional graphics** with lighting and shadows  
✅ **Dual dashboard modes** (3D + Classic 2D)  
✅ **Responsive design** for all devices  

**Everything runs automatically with `python run.py`!**

---

## 🌟 **What Makes This Special**

1. **Industry-First**: Full 3D digital twin with real data
2. **No Installation**: Runs in any modern web browser
3. **Real-Time**: Updates automatically from dataset
4. **Interactive**: Full camera control
5. **Beautiful**: Professional-grade graphics
6. **Educational**: Perfect for learning CNC operations

---

**Enjoy your new 3D CNC Digital Twin!** 🎊

Access it now at: **http://127.0.0.1:5000**
