/**
 * 3D CNC Machine Simulation using Three.js
 * Real-time visualization of CNC machine operations
 */

class CNCSimulation {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        
        // Machine components
        this.machineBase = null;
        this.xAxisRail = null;
        this.yAxisRail = null;
        this.zAxisSpindle = null;
        this.cuttingTool = null;
        this.workpiece = null;
        
        // Current position
        this.currentPosition = { x: 0, y: 0, z: 0 };
        this.spindleRotation = 0;
        this.spindleSpeed = 0;
        
        this.init();
    }
    
    init() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);
        this.scene.fog = new THREE.Fog(0x1a1a2e, 50, 200);
        
        // Create camera
        this.camera = new THREE.PerspectiveCamera(
            60,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(30, 30, 30);
        this.camera.lookAt(0, 0, 0);
        
        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
        
        // Add lights
        this.addLights();
        
        // Add grid
        const gridHelper = new THREE.GridHelper(50, 50, 0x444444, 0x222222);
        this.scene.add(gridHelper);
        
        // Add axes helper
        const axesHelper = new THREE.AxesHelper(15);
        this.scene.add(axesHelper);
        
        // Create CNC machine
        this.createMachine();
        
        // Add orbit controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.maxPolarAngle = Math.PI / 2;
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize(), false);
        
        // Start animation loop
        this.animate();
    }
    
    addLights() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
        this.scene.add(ambientLight);
        
        // Main directional light
        const mainLight = new THREE.DirectionalLight(0xffffff, 1);
        mainLight.position.set(20, 30, 20);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        mainLight.shadow.camera.near = 0.5;
        mainLight.shadow.camera.far = 100;
        mainLight.shadow.camera.left = -30;
        mainLight.shadow.camera.right = 30;
        mainLight.shadow.camera.top = 30;
        mainLight.shadow.camera.bottom = -30;
        this.scene.add(mainLight);
        
        // Fill lights
        const fillLight1 = new THREE.DirectionalLight(0x4466ff, 0.3);
        fillLight1.position.set(-10, 10, -10);
        this.scene.add(fillLight1);
        
        const fillLight2 = new THREE.DirectionalLight(0xff6644, 0.3);
        fillLight2.position.set(10, 5, 10);
        this.scene.add(fillLight2);
        
        // Spotlight on work area
        const spotlight = new THREE.SpotLight(0xffffff, 1);
        spotlight.position.set(0, 25, 0);
        spotlight.angle = Math.PI / 6;
        spotlight.penumbra = 0.3;
        spotlight.decay = 2;
        spotlight.distance = 50;
        spotlight.castShadow = true;
        this.scene.add(spotlight);
    }
    
    createMachine() {
        // Machine base (platform)
        const baseGeometry = new THREE.BoxGeometry(20, 1, 15);
        const baseMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x2c3e50,
            metalness: 0.7,
            roughness: 0.3
        });
        this.machineBase = new THREE.Mesh(baseGeometry, baseMaterial);
        this.machineBase.position.y = 0.5;
        this.machineBase.castShadow = true;
        this.machineBase.receiveShadow = true;
        this.scene.add(this.machineBase);
        
        // X-axis rail (red) - moves left/right
        const xRailGeometry = new THREE.BoxGeometry(18, 0.5, 1);
        const xRailMaterial = new THREE.MeshStandardMaterial({ 
            color: 0xe74c3c,
            metalness: 0.8,
            roughness: 0.2
        });
        this.xAxisRail = new THREE.Mesh(xRailGeometry, xRailMaterial);
        this.xAxisRail.position.set(0, 2, -6);
        this.xAxisRail.castShadow = true;
        this.scene.add(this.xAxisRail);
        
        // Y-axis carriage (green) - moves forward/backward
        const yCarriageGeometry = new THREE.BoxGeometry(3, 2, 2);
        const yCarriageMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x27ae60,
            metalness: 0.8,
            roughness: 0.2
        });
        this.yAxisRail = new THREE.Mesh(yCarriageGeometry, yCarriageMaterial);
        this.yAxisRail.position.set(0, 3, -6);
        this.yAxisRail.castShadow = true;
        this.scene.add(this.yAxisRail);
        
        // Z-axis spindle assembly (blue) - moves up/down
        const zSpindleGeometry = new THREE.CylinderGeometry(0.4, 0.4, 8, 16);
        const zSpindleMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x3498db,
            metalness: 0.9,
            roughness: 0.1
        });
        this.zAxisSpindle = new THREE.Mesh(zSpindleGeometry, zSpindleMaterial);
        this.zAxisSpindle.position.set(0, 7, -6);
        this.zAxisSpindle.castShadow = true;
        this.scene.add(this.zAxisSpindle);
        
        // Cutting tool (yellow cone)
        const toolGeometry = new THREE.ConeGeometry(0.3, 2, 8);
        const toolMaterial = new THREE.MeshStandardMaterial({ 
            color: 0xf39c12,
            metalness: 0.6,
            roughness: 0.4,
            emissive: 0xf39c12,
            emissiveIntensity: 0.2
        });
        this.cuttingTool = new THREE.Mesh(toolGeometry, toolMaterial);
        this.cuttingTool.position.set(0, 2, -6);
        this.cuttingTool.rotation.x = Math.PI;
        this.cuttingTool.castShadow = true;
        this.scene.add(this.cuttingTool);
        
        // Workpiece (orange cube)
        const workpieceGeometry = new THREE.BoxGeometry(8, 1.5, 6);
        const workpieceMaterial = new THREE.MeshStandardMaterial({ 
            color: 0xe67e22,
            metalness: 0.3,
            roughness: 0.7
        });
        this.workpiece = new THREE.Mesh(workpieceGeometry, workpieceMaterial);
        this.workpiece.position.set(0, 1.75, 2);
        this.workpiece.castShadow = true;
        this.workpiece.receiveShadow = true;
        this.scene.add(this.workpiece);
        
        // Add label
        this.addLabel();
    }
    
    addLabel() {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 512;
        canvas.height = 128;
        
        context.fillStyle = '#ffffff';
        context.font = 'Bold 48px Arial';
        context.textAlign = 'center';
        context.fillText('CNC MACHINE - LIVE', 256, 64);
        
        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.position.set(0, 15, 0);
        sprite.scale.set(10, 2.5, 1);
        this.scene.add(sprite);
    }
    
    updatePosition(x, y, z, spindleRPM) {
        // Normalize positions to machine workspace
        // X: -200 to 200 -> -8 to 8
        // Y: -200 to 200 -> -4 to 4  
        // Z: -20 to 0 -> 2 to 10
        
        const normalizedX = (x / 200) * 8;
        const normalizedY = (y / 200) * 4;
        const normalizedZ = 10 + (z / 20) * 8; // Z is negative, so this works
        
        this.currentPosition = { x: normalizedX, y: normalizedY, z: normalizedZ };
        this.spindleSpeed = spindleRPM || 0;
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Smooth interpolation to target position
        const lerpFactor = 0.1;
        
        // Update Y-axis carriage position (X movement)
        if (this.yAxisRail) {
            this.yAxisRail.position.x += (this.currentPosition.x - this.yAxisRail.position.x) * lerpFactor;
        }
        
        // Update Y-axis carriage position (Y movement)
        if (this.yAxisRail) {
            this.yAxisRail.position.z += (this.currentPosition.y - 6 - this.yAxisRail.position.z) * lerpFactor;
        }
        
        // Update Z-axis spindle position
        if (this.zAxisSpindle) {
            this.zAxisSpindle.position.x = this.yAxisRail.position.x;
            this.zAxisSpindle.position.z = this.yAxisRail.position.z;
            this.zAxisSpindle.position.y += (this.currentPosition.z - this.zAxisSpindle.position.y) * lerpFactor;
        }
        
        // Update cutting tool position and rotation
        if (this.cuttingTool) {
            this.cuttingTool.position.x = this.yAxisRail.position.x;
            this.cuttingTool.position.z = this.yAxisRail.position.z;
            this.cuttingTool.position.y = this.zAxisSpindle.position.y - 5;
            
            // Rotate spindle based on RPM
            this.spindleRotation += (this.spindleSpeed / 60000) * Math.PI * 2;
            this.cuttingTool.rotation.y = this.spindleRotation;
            this.zAxisSpindle.rotation.y = this.spindleRotation;
        }
        
        // Update controls
        if (this.controls) {
            this.controls.update();
        }
        
        // Render scene
        this.renderer.render(this.scene, this.camera);
    }
    
    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    updateFromData(data) {
        if (data && data.length > 0) {
            const latest = data[0]; // Get most recent record
            this.updatePosition(
                latest.axis_x_pos || 0,
                latest.axis_y_pos || 0,
                latest.axis_z_pos || 0,
                latest.spindle_speed_rpm || 0
            );
        }
    }
}

// Global instance
let cncSim = null;

// Initialize simulation when page loads
function initSimulation() {
    if (typeof THREE !== 'undefined') {
        cncSim = new CNCSimulation('simulation-container');
        console.log('✅ 3D CNC Simulation initialized');
    } else {
        console.error('❌ Three.js not loaded');
    }
}

// Update simulation with new data
function updateSimulation(data) {
    if (cncSim && data) {
        cncSim.updateFromData(data);
    }
}
