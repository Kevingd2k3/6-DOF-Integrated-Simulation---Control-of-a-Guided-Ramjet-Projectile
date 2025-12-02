import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import interp1d

# 1. CONFIGURATION & CONSTANTS
class Config:
    # Simulation Parameters
    dt = 0.01           # Time step (seconds)
    max_time = 100.0    # Max flight time
    g = 9.81            # Gravity (m/s^2)
    
    # Projectile Properties (155mm Shell M549)
    mass = 43.5         # kg
    diameter = 0.155    # m
    area = np.pi * (diameter/2)**2
    
    # Target (We are aiming for this)
    target_pos = np.array([15000.0, 500.0, 0.0]) # 15km downrange



# 2. AERODYNAMIC DATABASE
class AeroDatabase:
    def __init__(self, filepath='aerodynamics.csv'):
        # Columns: Mach(0), Alpha(1), Cd(2), Cl_Slope(3)
        try:
            data = np.genfromtxt(filepath, delimiter=',', skip_header=1)
            
            # Create Interpolation Functions
            # This creates a "lookup curve" from your data points
            self.cd_curve = interp1d(data[:, 0], data[:, 2], kind='linear', fill_value="extrapolate")
            self.cl_curve = interp1d(data[:, 0], data[:, 3], kind='linear', fill_value="extrapolate")
            print(f"Successfully loaded Aerodynamic Database from {filepath}")
            
        except Exception as e:
            print(f"Error loading database: {e}")
            print("Falling back to hardcoded estimates.")
            self.cd_curve = lambda m: 0.67 # Fallback
            self.cl_curve = lambda m: 2.0  # Fallback

    def get_cd(self, mach):
        # Look up drag from the loaded CSV curve
        return float(self.cd_curve(mach))

    def get_cl_alpha(self, mach):
        # Look up lift slope from the loaded CSV curve
        return float(self.cl_curve(mach))

# 3. THE PHYSICS ENGINE (6-DOF KINEMATICS)
class Projectile:
    def __init__(self):
        # State Vector: [x, y, z, vx, vy, vz] (Inertial Frame)
        self.pos = np.array([0.0, 2000.0, 0.0])  # Start at 2km altitude
        self.vel = np.array([680.0, 0.0, 0.0])   # Start at Mach 2 (680 m/s)
        
        # Orientation: Quaternion [x, y, z, w]
        # Initially aligned with X-axis
        self.quat = R.from_euler('xyz', [0, 0, 0]).as_quat()
        
        self.aero = AeroDatabase()

    def update(self, dt, target_pos):
        # A. ATMOSPHERE MODEL
        # Simple exponential atmosphere
        h = self.pos[1] # Altitude (y)
        rho = 1.225 * np.exp(-h / 8500.0)
        speed = np.linalg.norm(self.vel)
        mach = speed / 340.0 # Assuming constant speed of sound for simplicity
        
        if h < 0: return False # Crashed

        # B. GUIDANCE (The "GNC" Requirement)
        # Proportional Navigation (Simple version)
        # Calculate Vector to Target
        r_tm = target_pos - self.pos
        los_angle = np.arctan2(r_tm[1], r_tm[0]) # Line of Sight angle
        
        # Velocity Angle (Flight Path Angle)
        vel_angle = np.arctan2(self.vel[1], self.vel[0])
        
        # Desired Angle of Attack to steer
        # Gain * (Error between LOS and Velocity)
        N = 3.0 # Navigation Constant
        alpha_cmd = N * (los_angle - vel_angle)
        
        # Limit Alpha (Structural limit)
        alpha_cmd = np.clip(alpha_cmd, -np.radians(10), np.radians(10))

        # C. FORCES IN BODY FRAME
        # 1. Get Coefficients
        Cd = self.aero.get_cd(mach)
        Cl_slope = self.aero.get_cl_alpha(mach)
        Cl = Cl_slope * alpha_cmd

        # 2. Calculate Dynamic Pressure
        q = 0.5 * rho * speed**2 * Config.area

        # 3. Aerodynamic Forces (Body Frame)
        # Drag is always opposite to velocity vector
        # Lift is perpendicular to velocity vector
        F_drag = q * Cd
        F_lift = q * Cl

        # D. TRANSFORMATIONS (The "Reference Frame" Requirement) 
        # Create rotation from Velocity Vector (Wind Frame) to Inertial Frame
        # Simple 2D rotation for this demo (Pitch)
        gamma = np.arctan2(self.vel[1], self.vel[0]) # Flight path angle
        
        # Forces in Inertial Frame (resolving Lift and Drag)
        # Drag acts opposite to velocity (gamma + 180)
        # Lift acts perpendicular (gamma + 90)
        
        fx_aero = -F_drag * np.cos(gamma) - F_lift * np.sin(gamma)
        fy_aero = -F_drag * np.sin(gamma) + F_lift * np.cos(gamma)
        
        # E. INTEGRATION (Equation of Motion) 
        # F = ma => a = F/m
        ax = fx_aero / Config.mass
        ay = (fy_aero / Config.mass) - Config.g # Gravity acts down on Y

        # Euler Integration
        self.vel[0] += ax * dt
        self.vel[1] += ay * dt
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        
        return True # Still flying

# 4. RUN SIMULATION
def run_simulation():
    missile = Projectile()
    config = Config()
    
    # History for plotting
    history = {'x': [], 'y': [], 'mach': []}
    
    t = 0
    while t < config.max_time:
        flying = missile.update(config.dt, config.target_pos)
        if not flying:
            print(f"Impact at t={t:.2f}s")
            break
            
        # Record Data
        history['x'].append(missile.pos[0])
        history['y'].append(missile.pos[1])
        speed = np.linalg.norm(missile.vel)
        history['mach'].append(speed/340.0)
        
        t += config.dt

    return history

# 5. VISUALIZATION
if __name__ == "__main__":
    data = run_simulation()
    
    plt.figure(figsize=(10, 6))
    
    # Trajectory
    plt.subplot(2, 1, 1)
    plt.plot(data['x'], data['y'], label='Ramjet Trajectory', color='b', linewidth=2)
    plt.plot(Config.target_pos[0], Config.target_pos[1], 'rx', markersize=10, label='Target')
    plt.title(f'Ramjet Project: Guided Trajectory (Cd={AeroDatabase().get_cd(2.0):.2f})')
    plt.xlabel('Downrange (m)')
    plt.ylabel('Altitude (m)')
    plt.grid(True)
    plt.legend()
    
    # Mach Number
    plt.subplot(2, 1, 2)
    plt.plot(data['x'], data['mach'], color='r')
    plt.title('Mach Number Profile')
    plt.xlabel('Downrange (m)')
    plt.ylabel('Mach')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()