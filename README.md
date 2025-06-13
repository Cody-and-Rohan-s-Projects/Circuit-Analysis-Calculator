# Circuit Analysis Calculator Application

<div align="center">
  <img src="https://github.com/user-attachments/assets/8b3eb796-ddbb-44cc-a87c-1832e1726443" alt="App Screenshot" width="400">
</div>

## About Us

This calculator was created by Cody Carter and Rohan Patel, two computer engineering students with a shared goal: to develop an all-in-one application that simplifies and solves nodal analysis equations using a graphical interface—a lightweight and accessible alternative to MATLAB.

Rohan focused on building the backend and implementing additional UI features, while Cody integrated the backend into an intuitive, user-friendly interface.

We built this tool to help students and engineers quickly solve nodal or mesh analysis problems.



### Connect with Us:

<div align="left">
  <h3>Cody Carter</h3>
  <img src="https://github.com/user-attachments/assets/2808f0ad-6c56-464c-abdd-6ece9a4be026" alt="Cody Carter Profile" width="100" style="border-radius:50%">
  <p>
    <a href="https://github.com/codycarter1763">
      <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
    </a>
    <a href="https://www.linkedin.com/in/cody-carter-a8a747293/">
      <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
    </a>
  </p>
</div>

<div align="left">
  <h3>Rohan Patel</h3>
  <img src="https://github.com/user-attachments/assets/3a4125b1-9be2-477c-8c1a-5b18cee2ed93" alt="Rohan Patel Profile" width="100" style="border-radius:50%">
  <p>
    <a href="https://github.com/immmadeus">
      <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
    </a>
    <a href="https://www.linkedin.com/in/rohan-patel-15a211256/">
      <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
    </a>
  </p>
</div>


## How to Install and Use

1. Download the latest release from the [Releases](https://github.com/Cody-and-Rohan-s-Projects/Circuit-Analyser/releases) tab.
2. Unzip and extract the release into another folder.
3. The application is compatible with 32- or 64-bit versions of Windows 7, 8, 8.1, 10, and 11.
4. Open the .exe file, if it does not open, make sure the "_internal" folder is in the same folder as the .exe file.
5. If Windows shows a "Windows protected your PC" warning, click **"More info"** and then **"Run anyway"**. This is a standard message shown for unsigned applications.
6. A macOS version is coming soon!

<div align="center">
  
![Screenshot 1](https://github.com/user-attachments/assets/80274084-cba3-4ad7-8169-8e9b9ddd5508)

![Screenshot 2](https://github.com/user-attachments/assets/a1edfd12-106a-4a48-bd6f-ae992554d1a4)

</div>

## About the Calculator

The calculator currently supports solving systems of equations with **1 to 4 variables**.  

### How to Use:
- Select the matrix size using the dropdown menu and click **"Set Size."**
- Enter the coefficient and constant values into the respective matrices.
- Click **"Solve"** to view results.

### Features:
- Supports both **real** and **complex** numbers (in rectangular form).
- Displays results in **rectangular** and **polar** form.
- Shows **KVL equations** derived from the solution.
- Toggle **Dark Mode** and **Always on Top** using the respective sliders.

If invalid input is detected, an error message will be shown.

# About The Calculator
## The Goal
For this project, we wanted to create an all-in-one application to simplify and solve nodal analysis linear equations without using MATLAB code. Since it can take time to get MATLAB open, write your program, and execute it, we decided to make an easy to use calculator that can be open at any time while doing circuit analysis problems. 

## How Nodal Analysis Is Calculated
Nodal analysis is a really handy circuit analysis technique that allows you to solve unknown currents and voltages.
### Example

![image](https://github.com/user-attachments/assets/7cf70958-ac26-4d58-a83d-550a72b8d58f)

1. Locate node
![Step 1](https://github.com/user-attachments/assets/82bac9aa-aa20-44e0-99bb-f08987520698)

3. Set current directions
![Screenshot 2025-06-13 105432](https://github.com/user-attachments/assets/939ad2f2-6051-4fb0-9ddc-8d00e495c9cf)

4. Create KVL equations for each branch of the node in terms of ohms law
![equations](https://github.com/user-attachments/assets/a06c1643-5092-4bbc-b3e3-1b3d14302615)

5. Here is where our calculator application comes in handy. Normally, to solve for I1 and I2, you would use solving techniques like Cramers Rule to input the KVL equations into a matrix and solve for I1 and I2. For proof of concept, the steps will be shown in calculation.
![Untitled](https://github.com/user-attachments/assets/bd143e9b-eba4-49e9-9bff-547fdb233763)

6. As you can see, while this was a simple example, it still took a bit of calculation by hand. Especially with three or four unknowns it becomes a lot easier to make errors.

### How Our Circuit Analyzer Calculates 
1. Using the numpy python library, users can enter their constants of their KCL equations into the matrix. Where you enter your constants in this format.
<br/>

![image](https://github.com/user-attachments/assets/998b2028-d892-4e78-aac2-9bcff959ee4f)

![image](https://github.com/user-attachments/assets/07e45435-6115-4944-9634-788291277e7e)

2. The linear system will then be solved using a technique like Cramers Rule from the last example.
  
3. Using the customtkinter library, a gui was designed for a modern and lightweight look and feel. When calculated, your equations will be displayed so you can check your work, and the currents in amps and polar form for AC analysis.

![image](https://github.com/user-attachments/assets/8370c4e5-92ef-4ead-9609-01eb1425318b)

## Releases and Feature Updates

Planned features:
- Support for complex number input in **polar form**.
- Continued UI improvements and bug fixes.

We welcome suggestions and feedback—feel free to open an issue or contact us directly!



## Closing

Thank you for using our program!  
Bug reports or feedback is always appreciated!
