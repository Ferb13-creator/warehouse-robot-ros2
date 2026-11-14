# 🤖 ROS 2 Warehouse Robot

A modular warehouse robot project developed using **ROS 2 and Python**. This project demonstrates communication between robot nodes using custom Messages, Services, and Actions.

## 📌 Project Overview

The project demonstrates how a warehouse robot can publish its status, receive package-loading requests, and manage package deliveries using ROS 2 communication mechanisms.

## 🛠️ Technologies Used

- Ubuntu 24.04
- ROS 2
- Python
- CMake
- Colcon

## 📂 Project Structure

```text
warehouse-robot-ros2/
│
├── src/
│   ├── warehouse_interfaces/
│   │   ├── msg/
│   │   │   └── DeliveryStatus.msg
│   │   ├── srv/
│   │   │   └── LoadPackage.srv
│   │   ├── action/
│   │   │   └── Deliver.action
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   │
│   └── warehouse_nodes/
│       ├── warehouse_nodes/
│       │   ├── warehouse_publisher.py
│       │   ├── warehouse_subscriber.py
│       │   ├── deliver_server.py
│       │   └── deliver_client.py
│       ├── setup.py
│       └── package.xml
│
└── README.md
```

## ⚙️ ROS 2 Nodes

| Node | Responsibility |
|---|---|
| `warehouse_publisher` | Publishes robot status and handles package-loading service requests |
| `warehouse_subscriber` | Receives and displays robot status |
| `deliver_server` | Manages delivery goals, feedback, and cancellation |
| `deliver_client` | Sends delivery requests and receives results |

## 🔗 Custom ROS 2 Interfaces

### 1. Message – DeliveryStatus

Publishes:
- Robot ID
- Package count
- Battery percentage
- Robot state

### 2. Service – LoadPackage

Handles package-loading requests.

Conditions:
- Package weight must not exceed 10 kg.
- Maximum package count is 5.
- Returns acceptance status and a response message.

### 3. Action – Deliver

Manages delivery requests using:
- Destination
- Distance
- Speed
- Remaining distance feedback
- Delivery completion percentage
- Final delivery result

## 🚀 Installation and Build

Clone the repository:

```bash
git clone https://github.com/Ferb13-creator/warehouse-robot-ros2.git
```

Navigate to the workspace:

```bash
cd warehouse-robot-ros2
```

Build the packages:

```bash
colcon build
```

Source the workspace:

```bash
source install/setup.bash
```

## ▶️ Running the Project

Open separate terminals and source the workspace in each one.

**Terminal 1 – Warehouse Publisher**

```bash
ros2 run warehouse_nodes warehouse_publisher
```

**Terminal 2 – Warehouse Subscriber**

```bash
ros2 run warehouse_nodes warehouse_subscriber
```

**Terminal 3 – Delivery Server**

```bash
ros2 run warehouse_nodes deliver_server
```

**Terminal 4 – Delivery Client**

```bash
ros2 run warehouse_nodes deliver_client Warehouse_B 10.0 2.0
```

## 🧪 Testing Package Loading

```bash
ros2 service call /load_package warehouse_interfaces/srv/LoadPackage "{package_id: 'PKG101', weight: 5.5}"
```

## 🎯 Project Objectives

- Understand ROS 2 node architecture.
- Implement Publisher and Subscriber communication.
- Create custom ROS 2 Messages, Services, and Actions.
- Implement asynchronous delivery feedback.
- Develop modular and reusable robot software.

## 👨‍💻 Author

**Fernando**

GitHub: [Ferb13-creator](https://github.com/Ferb13-creator)

---

⭐ If you find this project interesting, feel free to explore the repository!
