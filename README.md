# Circuit Analysis Calculator Application
  
## About Us

This calculator was created by Cody Carter and Rohan Patel, two computer engineering students with a shared goal: to develop an all-in-one application that simplifies and solves nodal analysis equations using a graphical interface—a lightweight and accessible alternative to MATLAB.

Together we built a working backend and intuitive, user-friendly interface to work on Windows, Mac, Linux, iOS, and Android. We then split development for mobile, where 
Rohan focused on the Android version using Kotlin, while Cody focused on iOS using Swift.

We built this tool to help students and engineers quickly solve nodal or mesh analysis problems.

<!--suppress ALL -->
<div align="center">
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

## About the Calculator

The calculator currently supports solving systems of equations with **1 to 4 variables**.  

### Features:
- Supports both **real** and **complex** numbers (in rectangular form).
- Change the amount of decimal precision and number of equations to be solved using the dropdown menu.
- Displays results in **rectangular** and **polar** form.
- Shows **KVL equations** along with the solution.
- Desktop: Toggle **Dark Mode** and **Always on Top** using the respective sliders.

### How to Use:
- Select the matrix size using the dropdown menu and click **"Set Size."**
- Change the decimal precision of the answer and equations if needed.
- Enter the coefficient and constant values into the respective matrices.
- The values can be rectangular, complex or real.
- If invalid input is detected, an error message will be shown.
- Click or tap **"Solve"** to view results.
- Click or tap **"Reset"** or **"Clear"** to reset the inputs and outputs to start over.
- Click or tap **"Copy to Clipboard"** to copy the output to your clipboard for use in another app.

## How to Install and Use

1. Download the latest release from the [Releases](https://github.com/Cody-and-Rohan-s-Projects/Circuit-Analyser/releases) tab. Included inside are different installers dependent on what Linux distro you are running, only one needs to be ran.


### Linux:
<ol>
  <li> Select the appropriate package for your distro. ".rpm" for Red Hat systems (such as Fedora), ".deb" for Debian based systems (such as Ubuntu or Linux Mint), and ".tar.gz" for Arch.</li>
  <li> Double click your installer and install for your specific distro once downloaded.</li>
    <br>
  <div align="center">
    <img width="545" height="443" alt="image" src="https://github.com/user-attachments/assets/7a3f3325-2f4c-4a36-91d9-2a31839b43df" />
  </div>
    <br>
  <li> Once package is installed, open your applications and you should see Circuit Analysis ready to use.</li>
    <br>
  <div align="center">
    <img width="544" height="449" alt="image" src="https://github.com/user-attachments/assets/4fe51b39-c9f0-48d7-b3a5-0683c8a156f5" />
    <img width="515" height="247" alt="image" src="https://github.com/user-attachments/assets/76fe68b6-1bb6-4edd-9f4d-de96d97d43b6" />
  </div>
</ol> 



## Screenshots:

### *Desktop Versions:*
<figure>
  <div align="center">
    <img src="https://github.com/user-attachments/assets/d4a9eba3-85ae-470d-b1c4-74c24c14dfff" width="600" height="1200" alt="Windows Screenshot">
  </div>
</figure>

# Calculator Background

### *The Goal:*
For this project, we wanted to create an all-in-one application to simplify and solve nodal analysis linear equations without using MATLAB code. Since it can take time to get MATLAB open, write your program, and execute it, we decided to make an easy-to-use calculator that can be open at any time while doing circuit analysis problems. 

### *How Nodal Analysis Is Calculated:*
Nodal analysis is a handy circuit analysis technique that allows you to solve unknown currents and voltages.


![image](https://github.com/user-attachments/assets/7cf70958-ac26-4d58-a83d-550a72b8d58f)

Step 1: Locate node or nodes.

![Step 1](https://github.com/user-attachments/assets/82bac9aa-aa20-44e0-99bb-f08987520698)

Step 2: Pick current directions.

![Screenshot 2025-06-13 105432](https://github.com/user-attachments/assets/939ad2f2-6051-4fb0-9ddc-8d00e495c9cf)

Step 3. Create KVL equations for each branch of the node in terms of Ohm's law.

![equations](https://github.com/user-attachments/assets/a06c1643-5092-4bbc-b3e3-1b3d14302615)

Step 4: Here is where our calculator application comes in handy. Normally, to solve for I1 and I2, you would use solving techniques such as Cramer's Rule to input the KVL equations into a matrix and solve for I1 and I2. For this example, the steps will be shown in calculation.

![Untitled](https://github.com/user-attachments/assets/bd143e9b-eba4-49e9-9bff-547fdb233763)

As you can see, while this is a simple example, it still took a bit of calculation by hand. Especially with three or four unknowns, it becomes a lot easier to make errors.

### How Our Circuit Analyzer Calculates 
<ol>
  <li>
    Using the Python library NumPy, users can enter their constants of their KCL equations into the matrix. Where you enter your constants in this format. Due to language differences, an equivalent implementation to NumPy is used for compatibility with iOS and Android versions.
    <div align="center">
      <br>
      <img width="340" height="315" alt="image" src="https://github.com/user-attachments/assets/6adc539e-e6e4-457b-b419-a4cd3e11b4d4" />
      <br>
      <img width="582" height="174" alt="image" src="https://github.com/user-attachments/assets/b9d1b5c2-1986-4645-bef9-bf27a0c0d775" />
      <br>
    </div>
  </li>

  <li>
    The linear system will then be solved using a technique like Cramer's Rule from the last example.
  </li>
  <br>
  <li>
    When calculated, your equations will be displayed so you can check your work. All numbers will have their proper units, and will be shown in both rectangular and polar forms for AC analysis.
    <div align="center">
      <br>
      <img width="636" height="275" alt="image" src="https://github.com/user-attachments/assets/86fe8b5f-96bf-40af-9c11-b207c7a44e8a" />
      <br>
    </div>
  </li>
</ol>

## Releases and Feature Updates

Planned features:
- Support for complex number input in **polar form**.
- Continued UI improvements and bug fixes.

We welcome suggestions and feedback—feel free to let us know of an issue or contact us directly!



## Closing

Thank you for using our program!  
Bug reports or feedback is always appreciated!
