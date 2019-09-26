# OpenSight: the powerful, easy-to-use vision suite

## Want to get it?
Get the latest <a href="https://github.com/opensight-cv/opsi-gen/releases">release</a>!
## About

### What is this?
OpenSight is an FRC-focused, free and open source computer vision system for ARM based systems, such as the Raspberry Pi. Our goal is to make it easy for people not familar with vision systems to be able to make complex pipelines, while also have great functionality for power users. 

### Why?
Originally, this project was targeted at making a more accessible version of the Limelight for FRC. This vision still partially holds true, as OpenSight allows FRC teams to create vision pipelines for low monetary cost while still allowing collaboration and learning. We want to make vision more accessible to those who don't have much experience with vision, while also providing the tools for power users and inviting contributors to add their own piece to the project.

### Want to help development?
Join the discord server actively creating OpenSight: https://discord.gg/sMUJF2u

## How it works
The main components of the OpenSight Vision framework are the **modules** and the **manager**. 
In short, vision **modules** are connected to each other to form a vision pipeline used to detect and track vision targets. The software that binds them together in the backend is called the **manager**, while the raw footage from the camera comes from the **Camera Server**.

### Modules
The modules determine what the vision pipeline tracks and to what extent. OpenSight Modules take after cv image operations, allowing the user to have much greater control over the vision pipeline

A common pipeline will be: **Camera Server**->**Blur** -> **HSV/Color Mask** -> **Find Contours** -> **Select Largest Contour**

One unique advantage of OpenSight is its extendability. You can create your own module and with a simple pull request, make it available to all teams!

### Manager
The manager is the backbone of OpenSight. It controls the pipeline and manages the code. Once you create your own pipeline, it generates the python code for you to use on your robot!
