Python3 port of [Berkeley AI Pacman Search](http://ai.berkeley.edu) by jspacco (https://github.com/jspacco/pac3man). This read me is also from him, you should give it a look for more info and more exercises!

Project 1: Search
-----------------

Version 1.001. Last Updated: 08/26/2014.

* * *

### Table of Contents

*   [Introduction](#Introduction)
*   [Welcome](#Welcome)

* * *

> ![](http://ai.berkeley.edu/projects/release/search/v1/001/maze.png)
> 
> All those colored walls,  
> Mazes give Pacman the blues,  
> So teach him to search.

### Introduction

In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

`python autograder.py`

The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore.

**Files you'll edit and submit:**

[`search.py`](search.py)  Where all of your search algorithms will reside.

[`searchAgents.py`](searchAgents.py)   Where all of your search-based agents will reside.

**Helpful file for running code (might edit, won't submit):**

[`run.py`](run.py)   Use this file to run any commands in this readme. Look at the examples and make modifications as necessary. This file is helpful if you are not running from the command line, but you need to pass command line arguments to the code.

**Files you might want to look at:**

[`pacman.py`](pacman.py)   The main file that runs Pacman games. This file describes a Pacman GameState type, which you use in this project.

[`game.py`](game.py)   The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.

[`util.py`](util.py)   Useful data structures for implementing search algorithms.

**Supporting files you can ignore:**

[`graphicsDisplay.py`](graphicsDisplay.py)   Graphics for Pacman

[`graphicsUtils.py`](graphicsUtils.py)   Support for Pacman graphics

[`textDisplay.py`](textDisplay.py)   ASCII graphics for Pacman

[`ghostAgents.py`](ghostAgents.py)   Agents to control ghosts

[`keyboardAgents.py`](keyboardAgents.py)   Keyboard interfaces to control Pacman

[`layout.py`](layout.py)   Code for reading layout files and storing their contents

[`autograder.py`](autograder.py)   Project autograder

[`testParser.py`](testParser.py)   Parses autograder test and solution files

[`testClasses.py`](testClasses.py)   General autograding test classes

[`test_cases/`](test_cases)   Directory containing the test cases for each question

[`searchTestClasses.py`](searchTestClasses.py)   Project 1 specific autograding test classes

**Getting Help:** You are not alone! If you find yourself stuck on something, contact the course staff for help. Office hours, open lab, Red Room, and the discussion Google Group forum are there for your support; please use them. If you can't make our office hours, let us know and we will schedule more. We want these projects to be rewarding and instructional, not frustrating and demoralizing. But, we don't know when or how to help unless you ask.

**Discussion:** Please be careful not to post spoilers! If you fork this repo,
*make the repo private*.

* * *

### <a name="Welcome"></a> Welcome to Pacman 

After downloading or cloning the code, you should be able to play a game of Pacman by typing the following at the command line:

`python pacman.py`

Give it a try to this command and get familiar to how to play the game. You first need to know how pacman lives to make it so smart that it can go through all the levels with any effort.

The simplest agent in `searchAgents.py` is called the `GoWestAgent`, which always goes West (a trivial reflex agent). This agent can win... in some specific cases, like:

`python pacman.py --layout testMaze --pacman GoWestAgent`

But, things get ugly for this agent when turning is required!

`python pacman.py --layout tinyMaze --pacman GoWestAgent`

If Pacman gets stuck, you can exit the game by typing CTRL-c into your terminal.

Soon, your agent will solve not only `tinyMaze`, but any maze you want even `originalClassic`.

Note that `pacman.py` supports a number of options that can each be expressed in a long way (e.g., `--layout`) or a short way (e.g., `-l`). You can see the list of all options and their default values via:

`python pacman.py -h`

Also, all of the commands that appear in this project also appear in `commands.txt`, for easy copying and pasting. In UNIX/Mac OS X, you can even run all these commands in order with `bash commands.txt`.

Note: if you get error messages regarding Tkinter, see [this page](http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter).

* * *

* * *

### Submission

You're not done yet! Follow your instructor's guidelines to receive credit on your project!
