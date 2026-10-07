# Vibration Simulator

An interactive **Single Degree of Freedom (SDOF) Vibration Simulator** designed to help students understand and visualize mechanical vibration responses under different operating conditions.

The simulator provides real-time displacement-versus-time visualization and allows users to study free, forced, damped, and custom vibration systems.

---

## 🚀 Download

The compiled Windows executable (`.exe`) is available in the **Releases** section.

👉 **[Download Vibration Simulator](../../releases/latest)**

Download the latest `.exe` file from the release and run it on Windows.

> **Note:** Windows Defender may temporarily scan the application during the first launch. See the [First Launch](#-first-launch--windows-defender) section below if the simulator does not start immediately.

---

## ✨ Features

- Interactive SDOF vibration simulation
- Real-time displacement-versus-time visualization
- Preconfigured vibration scenarios
- Custom simulation mode
- Automatic calculation of system properties
- End-state analysis
- Support for free and forced vibration
- Support for different damping conditions
- Built using Python and scientific computing libraries

---

## 📊 Preconfigured Vibration Cases

The simulator includes **eight predefined vibration scenarios**:

1. Free Spring-Mass Vibration
2. Free Spring-Mass Critically Damped Vibration
3. Free Spring-Mass Underdamped Vibration
4. Free Spring-Mass Overdamped Vibration
5. Forced Spring-Mass Vibration Below Natural Frequency (`ω < ωₙ`)
6. Forced Spring-Mass Vibration Above Natural Frequency (`ω > ωₙ`)
7. Forced Spring-Mass Damped Vibration Below Natural Frequency (`ω < ωₙ`)
8. Forced Spring-Mass Damped Vibration Above Natural Frequency (`ω > ωₙ`)

---

## 🛠️ Custom Simulation Mode

A ninth simulation case allows users to define their own system parameters.

Users can specify:

- Mass (`m`)
- Spring stiffness (`k`)
- Damping coefficient (`c`)
- Force amplitude (`F₀`)
- Force frequency
- Initial displacement
- Initial velocity
- Simulation duration (`t_end`)
- Other simulation parameters

This allows users to investigate the vibration response of their own SDOF systems.

---

## 📐 System Properties

The simulator automatically calculates the following system properties as parameters are entered or modified:

- **Natural frequency**
- **Critical damping coefficient**
- **Damping ratio**
- **System classification**

The system is classified as:

- Undamped
- Underdamped
- Critically damped
- Overdamped

---

## 📈 End-State Analysis

At the specified simulation end time (`t_end`), the simulator calculates:

- Final displacement
- Final velocity
- Final acceleration

These values are automatically updated when the simulation parameters are changed.

---

## ▶️ How to Use

1. Launch the simulator.
2. Select one of the predefined vibration cases or choose **Custom Simulation**.
3. Enter or review the required parameters.
4. Press the **Play** button.
5. Observe the live displacement-versus-time response.
6. Modify the parameters to study how the system response changes.

---

## ⚠️ First Launch — Windows Defender

The simulator is packaged as a standalone Windows executable containing the required Python runtime and scientific libraries, including:

- NumPy
- SciPy
- Matplotlib

During the **first launch**, Windows Defender may temporarily scan or pause the extraction of the embedded Python environment.

This may result in an error such as:

> `Failed to start embedded Python interpreter`

### Solution

If this occurs:

1. Click **OK** on the error message.
2. Wait a few seconds for Windows Defender to complete its initial scan.
3. Launch the `.exe` again.

The simulator should start normally on subsequent launches.

---

## 💻 Source Code

The complete Python source code is included in this repository:

`Source_Code.py`

The executable version is provided through the **GitHub Releases** section.

---

## 🧰 Technologies Used

- **Python**
- **NumPy**
- **SciPy**
- **Matplotlib**

---

## 🎯 Purpose

This simulator was developed as an educational tool for understanding fundamental concepts in mechanical vibrations.

It can be used to visualize how changes in mass, stiffness, damping, forcing frequency, and initial conditions affect the dynamic response of an SDOF system.

---

## 👨‍💻 Author

**N. RaghavaKeerthan Reddy**

M.Tech — Mechanical Engineering

---

## 📄 License

This project is intended primarily for educational and academic purposes.
