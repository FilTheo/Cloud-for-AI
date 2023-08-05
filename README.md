# Cloud-for-AI

### Course Introduction 

Welcome to the repository for the course Cloud for AI. During the course, you will go through the process of deploying an already trained Machine Learning Model. 


As a general note, the commands in the course are meant to be run within a terminal. To begin you need **clone this repo in your local filesystem and `cd` to the Cloud for AI directory**

To clone the repo use this command:
```bash
git clone link.git
```

or for cloning via SSH use:
```bash
git clone git@github.com:link.git
```

If you are unsure which method to use for cloning, use the first one.

The `cd` command allows you to change directories. Assuming you are at the directory where you issued the cloning command, type the following on your terminal.
```bash
cd Cloud-for-AI/...rest
```
This will bring you to the `week 1` directory. The `ls` command allows you to list the files and directories.
Type `ls` and let's take a quick look at the content inside `week1-ungraded-lab` directory:

(Update what they will see there)
 
```
.
└── week1-ungraded-lab (this directory)
    ├── images (includes some images from ImageNet)
    ├── server.ipynb (Part 1 of the ungraded lab)
    ├── client.ipynb (Part 2 of the ungraded lab)
    └── requirements.txt (python dependencies)
```

#### 1. Create a virtual Environment

Now I assume you have successfully installed Visual Studio Code. The first step is to create a new developing environment. Python virtual environments' role is to create an isolated python environment for each project so that there are no dependency issues etc. from conflicting project requirements (e.g. Project A need pandas 1.0 and Project B needs pandas 1.1). 


Lets set a new environment with python with this command:

`python -m venv .venv`

After succesfully creating the environment, you need to activate it each time you work on this project using the following command:

`source .venv/bin/activate`

At this point, you will do all your libraries installation and work in this environment. So, whenever working on this lab, check the .venv environment is active.

#### 2. Installing dependencies using PIP 
 
Before proceeding, double check that you are currently on the `....` directory, which includes the `requirements.txt` file. This file lists all the required dependencies and their respective versions. 

Now use the following command to install the required dependencies:
 
```bash
pip install -r requirements.txt
```
This command can take a while to run depending on the speed of your internet connection. Once this step completes you should be ready to spin up jupyter lab and begin working on the lab.
 
Jupyter lab was installed during the previous step so you can launch it with this command:

```bash
jupyter lab
```
After execution, you will see some information printed on the terminal. Usually you will need to authenticate to use Jupyter lab. For this, copy the token that appears on your terminal, head over to [http://localhost:8888/lab](http://localhost:8888/lab) and paste it there. Your terminal's output should look very similar to the next image, in which the token has been highlighted for reference:


![Token in terminal](./assets/token.png)


#### 4. Running the notebook
 
Within Jupyter lab you should be in the same directory where you used the `jupyter lab` command.
 
Look for the `server.ipynb` file and open it to begin the ungraded lab.

To stop jupyter lab once you are done with the lab just press `Ctrl + C` twice.
 
#### And... that's it! Have fun deploying a Machine Learning model! :)

# 
#
#
# Method 2: Docker

