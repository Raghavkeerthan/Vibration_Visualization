## Download & Installation

The compiled Windows executable is available in the GitHub **Releases** section.

**[Download Vibration Simulator →](../../releases/latest)**

Download the `.exe` file from the latest release and run it on Windows

VIBRATION SIMULATOR - USER GUIDE

============================================================
1. IMPORTANT NOTE: FIRST LAUNCH BEHAVIOR (WINDOWS DEFENDER)
============================================================

This simulator is packaged as a standalone executable that includes the complete Python runtime and required scientific libraries (NumPy, SciPy, and Matplotlib).

First Run:

Windows Defender may temporarily pause the extraction process while scanning the application. This may result in the following error message:

"Failed to start embedded Python interpreter"

Solution:

Simply click OK and launch the .exe file again. Once the initial security scan is complete, the simulator will start normally and launch instantly on all subsequent runs.

============================================================
2. USING THE SIMULATOR
============================================================

Using the simulator is straightforward:

1. Select one of the predefined vibration cases.
2. Press the Play button.
3. The simulator will generate a live displacement-versus-time plot of the mass response.

PRECONFIGURED VIBRATION CASES

The simulator includes eight standard vibration scenarios with preset parameters:

1. Free Spring-Mass Vibration
2. Free Spring-Mass Critically Damped Vibration
3. Free Spring-Mass Underdamped Vibration
4. Free Spring-Mass Overdamped Vibration
5. Forced Spring-Mass Vibration Below Natural Frequency(< wn)
6. Forced Spring-Mass Vibration Above Natural Frequency(>wn)
7. Forced Spring-Mass Damped Vibration Below Natural Frequency(< wn)
8. Forced Spring-Mass Damped Vibration Above Natural Frequency(>wn)

CUSTOM SIMULATION MODE

A ninth case is available for complete customization.

Users can specify their own values for:

- Mass (m)
- Spring Stiffness (k)
- Damping Coefficient (c)
- Force Amplitude (F0)
- Force Frequency(Hz)
- Initial Displacement
- Initial Velocity
- Simulation Duration (t_end)

and other simulation parameters as required.

============================================================
3. SYSTEM PROPERTIES AND END-STATE ANALYSIS
============================================================

The System Properties and End State panels are located in the bottom-left section of the application.

As parameters are entered or modified, the simulator automatically computes and displays the following:

SYSTEM PROPERTIES

- Natural Frequency
- Critical Damping Coefficient
- Damping Ratio
- System Classification
  (Undamped, Underdamped, Critically Damped, or Overdamped)

END-STATE RESULTS

For the specified simulation end time (t_end), the simulator calculates:

- Final Displacement
- Final Velocity
- Final Acceleration

All values are updated in real time as input parameters are changed.

