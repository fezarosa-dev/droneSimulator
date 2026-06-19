# droneSimulator
A ROS 2-based simulation environment for autonomous drone navigation, designed for robotics researchers and students to test obstacle avoidance algorithms in a controlled virtual space.

## 🧭 At a Glance
- **What it is:** A ROS 2 (Robot Operating System) package providing a simulated drone platform.
- **What problem it solves:** Eliminates the need for physical hardware during the initial development and testing of drone flight controllers and obstacle avoidance logic.
- **Who uses it:** Robotics engineers and students learning ROS 2 and autonomous navigation.
- **Complexity level:** Intermediate (requires familiarity with ROS 2 concepts).
- **Best way to explore:** Start with `droneSimulator/main.py` to see the entry point, then inspect `droneSimulator/autopilot.py` to understand the control logic.

## 💡 Why This Exists
Developing flight software on physical drones is expensive, dangerous, and slow due to battery constraints and hardware repair cycles. Developers need a way to iterate on control loops and pathfinding algorithms without risking equipment.

This project provides a "digital twin" approach. By leveraging the ROS 2 ecosystem, it allows developers to write code that interacts with a simulated drone using the same message-passing interfaces they would use on real hardware.

It fits into the broader robotics ecosystem as a lightweight simulation node, bridging the gap between theoretical algorithm design and real-world deployment.

## ✨ Key Features
- **ROS 2 Node Integration** — Uses standard ROS 2 node architecture to ensure compatibility with the wider robotics ecosystem.
- **Obstacle Generation** — Procedural world generation via `world/world_generator.py` to test spatial awareness.
- **Autopilot Logic** — Encapsulated control loops in `autopilot.py` for testing navigation behaviors.
- **Modular Drone Model** — Separation of concerns between the drone physics/state and the simulation environment.
- **Launch System** — Standardized `launch/drone_simulator.launch.py` file for repeatable simulation startup.

## 🏗️ Core Architecture
- **System Design Pattern**: ROS 2 Node-based Architecture (a distributed system where independent processes communicate via topics and services).
- **Data Flow**: `world_generator.py` defines the environment → `drone.py` tracks state → `autopilot.py` processes state to calculate velocity vectors → `drone_simulator_node.py` publishes commands to the ROS 2 graph.
- **Key Abstractions**: `Drone` (state container), `Autopilot` (decision engine), and `World` (spatial constraints).
- **Boundaries & Seams**: The system interfaces with the ROS 2 middleware (DDS) for external communication, allowing it to be controlled by external nodes.

## 🛠️ Tech Stack
- **Languages & Frameworks:** Python 3, ROS 2 (Robot Operating System).
- **Build & Tooling:** `colcon` (standard ROS build tool), `flake8` (linting), `pytest` (via `test/` directory).
- **Infrastructure:** Local ROS 2 environment.
- **External Runtime Requirements:** ROS 2 (Humble or Foxy recommended), `colcon` build system.

## 📦 Critical Dependencies
- `rclpy` — The ROS 2 Python client library; essential for node communication.
- `geometry_msgs` — Standard ROS message types for position and velocity; required for drone movement.
- `std_msgs` — Basic ROS primitive types for system status reporting.

## 🗂️ Project Structure
```text
/droneSimulator       → Core package logic, containing drone, autopilot, and world modules
/launch               → ROS 2 launch files for orchestrating the simulation
/resource             → Package-specific resource markers for ROS 2 indexer
/test                 → Unit and style tests (copyright, flake8, pep257)
/package.xml          → ROS 2 package manifest and dependency declarations
/setup.py             → Python package installation script
/setup.cfg            → Configuration for package installation
/fis.txt              → Likely a project-specific configuration or data reference
```
*Mental Map: To understand this project, think of it as a specialized ROS 2 node that acts as a virtual flight controller.*

## 🔍 Where to Start Reading
**For engineers:**
- `droneSimulator/drone_simulator_node.py` — *The main entry point that manages the ROS 2 lifecycle.*
- `droneSimulator/autopilot.py` — *The core logic for drone decision-making.*
- `droneSimulator/drone/drone.py` — *The data model representing the drone's physical state.*

**For learners:**
- `droneSimulator/main.py` — *Shows how the application is initialized.*
- `launch/drone_simulator.launch.py` — *Teaches how ROS 2 nodes are orchestrated.*
- `droneSimulator/world/obstacle.py` — *A simple class demonstrating basic object-oriented design in the simulation.*

## 🚀 Getting Started

### Prerequisites
- ROS 2 installed (e.g., Humble Hawksbill).
- `colcon` build tool.
- Python 3.8+.

### Setup
```bash
# Clone the repository
git clone https://github.com/fezarosa-dev/droneSimulator
# Build the package
colcon build --packages-select droneSimulator
# Source the environment
source install/setup.bash
```

### Verify It's Working
```bash
ros2 launch droneSimulator drone_simulator.launch.py
# You should see the simulation node initializing and publishing status messages.
```

## 🤝 How to Contribute
1. **What contributions are most welcome?** Documentation, unit test coverage, and new obstacle types.
2. **Which folder is lowest-risk to edit?** `droneSimulator/world/` is isolated and ideal for adding new environment features.
3. **What does a good PR look like?** Includes updated `package.xml` if dependencies change and passes all `test/` scripts.

**Testing & linting before you push:**
```bash
colcon test --packages-select droneSimulator
```

## 📚 What You'll Learn
- **ROS 2 Lifecycle:** How to structure a robotics application as a set of nodes.
- **Simulation Design:** How to model physical systems in a virtual environment.
- **Python Packaging:** Best practices for structuring ROS 2 Python packages.
- **Automated Testing:** How to enforce code quality in robotics projects using `flake8` and `pep257`.

## 🤖 Machine-Readable Metadata [AI-READABLE]
```yaml
repo: fezarosa-dev/droneSimulator
description: "ROS 2 drone simulation environment"
stars: 1
forks: 0
open_issues: 0
language: "Python"
license: "none"
architecture_pattern: "ROS 2 Node-based"
entry_point: "droneSimulator/drone_simulator_node.py"
external_dependencies_required: true
test_command: "colcon test"
ci_present: false
```

## 📊 Quick Stats [AI-READABLE]
| Metric | Value |
|--------|-------|
| ⭐ Stars | 1 |
| 🍴 Forks | 0 |
| 🐛 Open Issues & PRs | 0 |
| 💬 Primary Language | Python |
| ⚖️ License | N/A |