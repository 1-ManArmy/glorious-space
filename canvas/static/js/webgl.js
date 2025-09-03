/**
 * 3D WebGL Engine for Developer Crown Site
 * Provides interactive 3D rendering and visualization capabilities
 * Uses Three.js for 3D graphics rendering
 */

class Canvas3D {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.animationFrame = null;
        
        // 3D Objects
        this.objects = [];
        this.selectedObject = null;
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        
        // Collaboration
        this.sessionId = options.sessionId || null;
        this.isCollaborative = options.collaborative || false;
        this.socket = null;
        
        // Tools and modes
        this.currentTool = 'select';
        this.isAddingObject = false;
        
        this.init();
    }
    
    init() {
        this.setupScene();
        this.setupCamera();
        this.setupRenderer();
        this.setupControls();
        this.setupLighting();
        this.setupEventListeners();
        this.setupUI();
        this.addDefaultObjects();
        this.animate();
        
        if (this.isCollaborative) {
            this.initWebSocket();
        }
    }
    
    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);
        
        // Add fog for depth perception
        this.scene.fog = new THREE.Fog(0x1a1a2e, 10, 100);
    }
    
    setupCamera() {
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.set(5, 5, 5);
        this.camera.lookAt(0, 0, 0);
    }
    
    setupRenderer() {
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1;
        
        this.container.appendChild(this.renderer.domElement);
    }
    
    setupControls() {
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.25;
        this.controls.screenSpacePanning = false;
        this.controls.maxPolarAngle = Math.PI / 2;
    }
    
    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);
        
        // Directional light (sun)
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 10, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 100;
        directionalLight.shadow.camera.left = -10;
        directionalLight.shadow.camera.right = 10;
        directionalLight.shadow.camera.top = 10;
        directionalLight.shadow.camera.bottom = -10;
        this.scene.add(directionalLight);
        
        // Point light for dynamic lighting
        const pointLight = new THREE.PointLight(0xff6b35, 0.8, 20);
        pointLight.position.set(-5, 5, -5);
        pointLight.castShadow = true;
        this.scene.add(pointLight);
        
        // Hemisphere light for realistic outdoor lighting
        const hemisphereLight = new THREE.HemisphereLight(0x87ceeb, 0x98fb98, 0.3);
        this.scene.add(hemisphereLight);
    }
    
    setupEventListeners() {
        // Mouse events
        this.renderer.domElement.addEventListener('click', this.onMouseClick.bind(this));
        this.renderer.domElement.addEventListener('mousemove', this.onMouseMove.bind(this));
        
        // Window resize
        window.addEventListener('resize', this.onWindowResize.bind(this));
        
        // Keyboard controls
        document.addEventListener('keydown', this.onKeyDown.bind(this));
    }
    
    setupUI() {
        this.setupToolbar();
        this.setupObjectPanel();
        this.setupPropertiesPanel();
    }
    
    setupToolbar() {
        const toolbar = document.getElementById('toolbar3d');
        if (!toolbar) return;
        
        const tools = [
            { id: 'select', name: 'Select', icon: '🔍' },
            { id: 'move', name: 'Move', icon: '↔️' },
            { id: 'rotate', name: 'Rotate', icon: '🔄' },
            { id: 'scale', name: 'Scale', icon: '📏' },
            { id: 'cube', name: 'Add Cube', icon: '🟦' },
            { id: 'sphere', name: 'Add Sphere', icon: '🔵' },
            { id: 'cylinder', name: 'Add Cylinder', icon: '🛡️' },
            { id: 'light', name: 'Add Light', icon: '💡' }
        ];
        
        tools.forEach(tool => {
            const button = document.createElement('button');
            button.className = 'tool-btn-3d';
            button.dataset.tool = tool.id;
            button.innerHTML = `${tool.icon} ${tool.name}`;
            button.addEventListener('click', () => this.setTool(tool.id));
            toolbar.appendChild(button);
        });
    }
    
    setupObjectPanel() {
        // Create object hierarchy panel
        const panel = document.getElementById('objectPanel');
        if (!panel) return;
        
        this.updateObjectList();
    }
    
    setupPropertiesPanel() {
        // Create properties panel for selected object
        const panel = document.getElementById('propertiesPanel');
        if (!panel) return;
        
        // This will be populated when an object is selected
    }
    
    setTool(tool) {
        this.currentTool = tool;
        
        // Update UI
        document.querySelectorAll('.tool-btn-3d').forEach(btn => {
            btn.classList.remove('active');
        });
        
        const activeBtn = document.querySelector(`[data-tool="${tool}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }
        
        // Handle tool-specific actions
        switch(tool) {
            case 'cube':
            case 'sphere':
            case 'cylinder':
            case 'light':
                this.isAddingObject = true;
                this.renderer.domElement.style.cursor = 'crosshair';
                break;
            default:
                this.isAddingObject = false;
                this.renderer.domElement.style.cursor = 'default';
        }
    }
    
    addDefaultObjects() {
        // Add a ground plane
        const groundGeometry = new THREE.PlaneGeometry(20, 20);
        const groundMaterial = new THREE.MeshLambertMaterial({ color: 0x2c3e50 });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        ground.name = 'Ground';
        this.scene.add(ground);
        this.objects.push(ground);
        
        // Add a sample cube
        this.addCube(new THREE.Vector3(0, 1, 0), { color: 0x3498db });
        
        // Add a sample sphere
        this.addSphere(new THREE.Vector3(2, 1, 2), { color: 0xe74c3c });
        
        this.updateObjectList();
    }
    
    addCube(position = new THREE.Vector3(0, 1, 0), options = {}) {
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshPhongMaterial({ 
            color: options.color || 0x3498db,
            transparent: options.transparent || false,
            opacity: options.opacity || 1
        });
        
        const cube = new THREE.Mesh(geometry, material);
        cube.position.copy(position);
        cube.castShadow = true;
        cube.receiveShadow = true;
        cube.name = `Cube_${Date.now()}`;
        cube.userData = { type: 'cube', createdBy: window.currentUser };
        
        this.scene.add(cube);
        this.objects.push(cube);
        this.updateObjectList();
        
        if (this.isCollaborative) {
            this.broadcastObjectChange('add', cube);
        }
        
        return cube;
    }
    
    addSphere(position = new THREE.Vector3(0, 1, 0), options = {}) {
        const geometry = new THREE.SphereGeometry(0.5, 32, 32);
        const material = new THREE.MeshPhongMaterial({ 
            color: options.color || 0xe74c3c,
            transparent: options.transparent || false,
            opacity: options.opacity || 1
        });
        
        const sphere = new THREE.Mesh(geometry, material);
        sphere.position.copy(position);
        sphere.castShadow = true;
        sphere.receiveShadow = true;
        sphere.name = `Sphere_${Date.now()}`;
        sphere.userData = { type: 'sphere', createdBy: window.currentUser };
        
        this.scene.add(sphere);
        this.objects.push(sphere);
        this.updateObjectList();
        
        if (this.isCollaborative) {
            this.broadcastObjectChange('add', sphere);
        }
        
        return sphere;
    }
    
    addCylinder(position = new THREE.Vector3(0, 1, 0), options = {}) {
        const geometry = new THREE.CylinderGeometry(0.5, 0.5, 1, 32);
        const material = new THREE.MeshPhongMaterial({ 
            color: options.color || 0x9b59b6,
            transparent: options.transparent || false,
            opacity: options.opacity || 1
        });
        
        const cylinder = new THREE.Mesh(geometry, material);
        cylinder.position.copy(position);
        cylinder.castShadow = true;
        cylinder.receiveShadow = true;
        cylinder.name = `Cylinder_${Date.now()}`;
        cylinder.userData = { type: 'cylinder', createdBy: window.currentUser };
        
        this.scene.add(cylinder);
        this.objects.push(cylinder);
        this.updateObjectList();
        
        if (this.isCollaborative) {
            this.broadcastObjectChange('add', cylinder);
        }
        
        return cylinder;
    }
    
    addLight(position = new THREE.Vector3(0, 5, 0), options = {}) {
        const light = new THREE.PointLight(
            options.color || 0xffffff,
            options.intensity || 1,
            options.distance || 10
        );
        light.position.copy(position);
        light.castShadow = true;
        light.name = `Light_${Date.now()}`;
        light.userData = { type: 'light', createdBy: window.currentUser };
        
        // Add light helper
        const helper = new THREE.PointLightHelper(light, 0.2);
        light.add(helper);
        
        this.scene.add(light);
        this.objects.push(light);
        this.updateObjectList();
        
        if (this.isCollaborative) {
            this.broadcastObjectChange('add', light);
        }
        
        return light;
    }
    
    onMouseClick(event) {
        this.mouse.x = (event.clientX / this.renderer.domElement.clientWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / this.renderer.domElement.clientHeight) * 2 + 1;
        
        this.raycaster.setFromCamera(this.mouse, this.camera);
        
        if (this.isAddingObject) {
            this.handleObjectAddition(event);
        } else {
            this.handleObjectSelection();
        }
    }
    
    handleObjectAddition(event) {
        // Raycast to find intersection with ground plane
        const groundPlane = this.scene.getObjectByName('Ground');
        const intersects = this.raycaster.intersectObject(groundPlane);
        
        if (intersects.length > 0) {
            const position = intersects[0].point;
            position.y += 0.5; // Lift above ground
            
            switch(this.currentTool) {
                case 'cube':
                    this.addCube(position);
                    break;
                case 'sphere':
                    this.addSphere(position);
                    break;
                case 'cylinder':
                    this.addCylinder(position);
                    break;
                case 'light':
                    position.y += 4; // Lights should be higher
                    this.addLight(position);
                    break;
            }
            
            this.isAddingObject = false;
            this.setTool('select');
        }
    }
    
    handleObjectSelection() {
        const intersects = this.raycaster.intersectObjects(this.objects);
        
        if (intersects.length > 0) {
            const selectedObject = intersects[0].object;
            this.selectObject(selectedObject);
        } else {
            this.deselectObject();
        }
    }
    
    selectObject(object) {
        // Deselect previous object
        this.deselectObject();
        
        this.selectedObject = object;
        
        // Add selection indicator
        const box = new THREE.BoxHelper(object, 0xffff00);
        box.name = 'selection_box';
        this.scene.add(box);
        
        // Update properties panel
        this.updatePropertiesPanel();
        
        // Highlight in object list
        this.highlightObjectInList(object);
    }
    
    deselectObject() {
        if (this.selectedObject) {
            // Remove selection indicator
            const selectionBox = this.scene.getObjectByName('selection_box');
            if (selectionBox) {
                this.scene.remove(selectionBox);
            }
            
            this.selectedObject = null;
            this.updatePropertiesPanel();
            this.clearObjectListHighlight();
        }
    }
    
    deleteSelectedObject() {
        if (this.selectedObject && this.selectedObject.name !== 'Ground') {
            this.scene.remove(this.selectedObject);
            const index = this.objects.indexOf(this.selectedObject);
            if (index > -1) {
                this.objects.splice(index, 1);
            }
            
            if (this.isCollaborative) {
                this.broadcastObjectChange('delete', this.selectedObject);
            }
            
            this.deselectObject();
            this.updateObjectList();
        }
    }
    
    onMouseMove(event) {
        this.mouse.x = (event.clientX / this.renderer.domElement.clientWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / this.renderer.domElement.clientHeight) * 2 + 1;
        
        // Handle object dragging if in move mode
        if (this.currentTool === 'move' && this.selectedObject) {
            // Implementation for object dragging
        }
    }
    
    onKeyDown(event) {
        switch(event.key) {
            case 'Delete':
                this.deleteSelectedObject();
                break;
            case 'Escape':
                this.deselectObject();
                this.isAddingObject = false;
                this.setTool('select');
                break;
            case 'r':
                if (event.ctrlKey) {
                    event.preventDefault();
                    this.resetCamera();
                }
                break;
            case 's':
                if (event.ctrlKey) {
                    event.preventDefault();
                    this.saveScene();
                }
                break;
        }
    }
    
    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    updateObjectList() {
        const panel = document.getElementById('objectPanel');
        if (!panel) return;
        
        panel.innerHTML = '<h3>Scene Objects</h3>';
        
        const list = document.createElement('ul');
        list.className = 'object-list';
        
        this.objects.forEach(object => {
            const listItem = document.createElement('li');
            listItem.className = 'object-item';
            listItem.dataset.objectName = object.name;
            listItem.innerHTML = `
                <span class="object-icon">${this.getObjectIcon(object)}</span>
                <span class="object-name">${object.name}</span>
                <button class="delete-object-btn" onclick="canvas3d.deleteObject('${object.name}')">×</button>
            `;
            
            listItem.addEventListener('click', () => {
                this.selectObject(object);
            });
            
            list.appendChild(listItem);
        });
        
        panel.appendChild(list);
    }
    
    updatePropertiesPanel() {
        const panel = document.getElementById('propertiesPanel');
        if (!panel) return;
        
        if (!this.selectedObject) {
            panel.innerHTML = '<h3>Properties</h3><p>No object selected</p>';
            return;
        }
        
        const object = this.selectedObject;
        panel.innerHTML = `
            <h3>Properties</h3>
            <div class="property-group">
                <label>Name:</label>
                <input type="text" value="${object.name}" onchange="canvas3d.updateObjectName('${object.name}', this.value)">
            </div>
            <div class="property-group">
                <label>Position:</label>
                <div class="vector-input">
                    <input type="number" step="0.1" value="${object.position.x.toFixed(2)}" onchange="canvas3d.updateObjectPosition('x', this.value)">
                    <input type="number" step="0.1" value="${object.position.y.toFixed(2)}" onchange="canvas3d.updateObjectPosition('y', this.value)">
                    <input type="number" step="0.1" value="${object.position.z.toFixed(2)}" onchange="canvas3d.updateObjectPosition('z', this.value)">
                </div>
            </div>
            <div class="property-group">
                <label>Rotation:</label>
                <div class="vector-input">
                    <input type="number" step="0.1" value="${(object.rotation.x * 180 / Math.PI).toFixed(1)}" onchange="canvas3d.updateObjectRotation('x', this.value)">
                    <input type="number" step="0.1" value="${(object.rotation.y * 180 / Math.PI).toFixed(1)}" onchange="canvas3d.updateObjectRotation('y', this.value)">
                    <input type="number" step="0.1" value="${(object.rotation.z * 180 / Math.PI).toFixed(1)}" onchange="canvas3d.updateObjectRotation('z', this.value)">
                </div>
            </div>
            <div class="property-group">
                <label>Scale:</label>
                <div class="vector-input">
                    <input type="number" step="0.1" value="${object.scale.x.toFixed(2)}" onchange="canvas3d.updateObjectScale('x', this.value)">
                    <input type="number" step="0.1" value="${object.scale.y.toFixed(2)}" onchange="canvas3d.updateObjectScale('y', this.value)">
                    <input type="number" step="0.1" value="${object.scale.z.toFixed(2)}" onchange="canvas3d.updateObjectScale('z', this.value)">
                </div>
            </div>
        `;
        
        // Add material properties if it's a mesh
        if (object.material) {
            const materialPanel = document.createElement('div');
            materialPanel.innerHTML = `
                <div class="property-group">
                    <label>Color:</label>
                    <input type="color" value="#${object.material.color.getHexString()}" onchange="canvas3d.updateObjectColor(this.value)">
                </div>
                <div class="property-group">
                    <label>Opacity:</label>
                    <input type="range" min="0" max="1" step="0.1" value="${object.material.opacity}" onchange="canvas3d.updateObjectOpacity(this.value)">
                    <span>${object.material.opacity}</span>
                </div>
            `;
            panel.appendChild(materialPanel);
        }
    }
    
    getObjectIcon(object) {
        if (object.userData.type) {
            switch(object.userData.type) {
                case 'cube': return '🟦';
                case 'sphere': return '🔵';
                case 'cylinder': return '🛡️';
                case 'light': return '💡';
                default: return '📦';
            }
        }
        return object.name === 'Ground' ? '🌍' : '📦';
    }
    
    // Object manipulation methods
    updateObjectName(oldName, newName) {
        const object = this.scene.getObjectByName(oldName);
        if (object) {
            object.name = newName;
            this.updateObjectList();
        }
    }
    
    updateObjectPosition(axis, value) {
        if (this.selectedObject) {
            this.selectedObject.position[axis] = parseFloat(value);
            this.broadcastObjectChange('update', this.selectedObject);
        }
    }
    
    updateObjectRotation(axis, value) {
        if (this.selectedObject) {
            this.selectedObject.rotation[axis] = parseFloat(value) * Math.PI / 180;
            this.broadcastObjectChange('update', this.selectedObject);
        }
    }
    
    updateObjectScale(axis, value) {
        if (this.selectedObject) {
            this.selectedObject.scale[axis] = parseFloat(value);
            this.broadcastObjectChange('update', this.selectedObject);
        }
    }
    
    updateObjectColor(colorHex) {
        if (this.selectedObject && this.selectedObject.material) {
            this.selectedObject.material.color.setHex(colorHex.replace('#', '0x'));
            this.broadcastObjectChange('update', this.selectedObject);
        }
    }
    
    updateObjectOpacity(opacity) {
        if (this.selectedObject && this.selectedObject.material) {
            this.selectedObject.material.opacity = parseFloat(opacity);
            this.selectedObject.material.transparent = opacity < 1;
            this.broadcastObjectChange('update', this.selectedObject);
        }
    }
    
    deleteObject(objectName) {
        const object = this.scene.getObjectByName(objectName);
        if (object && object.name !== 'Ground') {
            this.scene.remove(object);
            const index = this.objects.indexOf(object);
            if (index > -1) {
                this.objects.splice(index, 1);
            }
            
            if (this.selectedObject === object) {
                this.deselectObject();
            }
            
            this.updateObjectList();
            
            if (this.isCollaborative) {
                this.broadcastObjectChange('delete', object);
            }
        }
    }
    
    highlightObjectInList(object) {
        document.querySelectorAll('.object-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        const item = document.querySelector(`[data-object-name="${object.name}"]`);
        if (item) {
            item.classList.add('selected');
        }
    }
    
    clearObjectListHighlight() {
        document.querySelectorAll('.object-item').forEach(item => {
            item.classList.remove('selected');
        });
    }
    
    resetCamera() {
        this.camera.position.set(5, 5, 5);
        this.camera.lookAt(0, 0, 0);
        this.controls.reset();
    }
    
    animate() {
        this.animationFrame = requestAnimationFrame(this.animate.bind(this));
        
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
    
    // WebSocket for collaboration
    initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/canvas3d/${this.sessionId}/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            console.log('3D Canvas WebSocket connected');
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleRemoteUpdate(data);
        };
        
        this.socket.onclose = () => {
            console.log('3D Canvas WebSocket disconnected');
        };
    }
    
    broadcastObjectChange(action, object) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            const data = {
                type: '3d_object_change',
                action: action,
                object: this.serializeObject(object),
                user: window.currentUser
            };
            this.socket.send(JSON.stringify(data));
        }
    }
    
    serializeObject(object) {
        return {
            name: object.name,
            type: object.userData.type,
            position: object.position,
            rotation: object.rotation,
            scale: object.scale,
            material: object.material ? {
                color: object.material.color.getHex(),
                opacity: object.material.opacity
            } : null
        };
    }
    
    handleRemoteUpdate(data) {
        if (data.user === window.currentUser) return;
        
        // Handle remote object changes
        switch(data.action) {
            case 'add':
                this.createObjectFromData(data.object);
                break;
            case 'update':
                this.updateObjectFromData(data.object);
                break;
            case 'delete':
                this.deleteObject(data.object.name);
                break;
        }
    }
    
    createObjectFromData(objectData) {
        // Create object based on remote data
        const position = new THREE.Vector3(objectData.position.x, objectData.position.y, objectData.position.z);
        const options = {
            color: objectData.material ? objectData.material.color : 0x3498db
        };
        
        let object;
        switch(objectData.type) {
            case 'cube':
                object = this.addCube(position, options);
                break;
            case 'sphere':
                object = this.addSphere(position, options);
                break;
            case 'cylinder':
                object = this.addCylinder(position, options);
                break;
        }
        
        if (object) {
            object.name = objectData.name;
            object.rotation.set(objectData.rotation.x, objectData.rotation.y, objectData.rotation.z);
            object.scale.set(objectData.scale.x, objectData.scale.y, objectData.scale.z);
        }
    }
    
    updateObjectFromData(objectData) {
        const object = this.scene.getObjectByName(objectData.name);
        if (object) {
            object.position.set(objectData.position.x, objectData.position.y, objectData.position.z);
            object.rotation.set(objectData.rotation.x, objectData.rotation.y, objectData.rotation.z);
            object.scale.set(objectData.scale.x, objectData.scale.y, objectData.scale.z);
            
            if (object.material && objectData.material) {
                object.material.color.setHex(objectData.material.color);
                object.material.opacity = objectData.material.opacity;
            }
        }
    }
    
    saveScene() {
        const sceneData = {
            objects: this.objects.map(obj => this.serializeObject(obj)),
            camera: {
                position: this.camera.position,
                rotation: this.camera.rotation
            },
            timestamp: new Date().toISOString()
        };
        
        fetch('/api/canvas/save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                session_id: this.sessionId,
                canvas_type: '3d',
                canvas_data: sceneData
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.showNotification('3D scene saved successfully!', 'success');
                if (data.session_id) {
                    this.sessionId = data.session_id;
                }
            }
        })
        .catch(error => {
            console.error('Error saving 3D scene:', error);
            this.showNotification('Error saving 3D scene', 'error');
        });
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 24px;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            border-radius: 4px;
            z-index: 1000;
        `;
        
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }
    
    destroy() {
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }
        
        if (this.socket) {
            this.socket.close();
        }
        
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// Initialize 3D Canvas when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('canvas3d-container');
    if (container) {
        const sessionId = container.dataset.sessionId;
        const collaborative = container.dataset.collaborative === 'true';
        
        window.canvas3d = new Canvas3D('canvas3d-container', {
            sessionId: sessionId,
            collaborative: collaborative
        });
    }
});
