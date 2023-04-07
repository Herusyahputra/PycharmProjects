## How to install ?

This guidance is tested on ubuntu 20.04 with python 3.8

### 1. Clone this repository

   Use the git clone command to download the code from the repository to your local machine.
   ```
   git clone https://github.com/McutOIL/moilapp.git --branch=develop
   ```
### 2. Change working directory
   
   After successfully cloning the repository,change working directory by using the command line below.
   ```
   cd moilapp
   ```

### 3. Set up Virtual Environment 
  - To build a new virtual environment, use the python command. You can define the Python version to use by giving the location of the Python executable.
    ```
    python3.8 -m venv env
    ```
    *note: you can change the python version ex: *python3.8, python3.9, python3.10*


   - To start using the virtual environment, you need to activate it. You can do this by running the activate script located in the `bin` directory of your virtual environment. On Linux or macOS, use the following command:
     ```
     source venv/bin/activate
     ```
     
   - With the environment activated, you can install all required packages. The packages will be installed in the virtual environment and will not affect the global Python installation.
     ```
     pip install -r requirements.txt
     ```
  
### 4. Run the Program

After all ready, run the main program in `src` directory, on your terminal you can type this command to run the project

  ```
  $ cd src
  $ python3 main.py
  ```

