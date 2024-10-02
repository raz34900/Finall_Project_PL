
User Guide: Running the Interpreter


The interpreter for this custom programming language can be run in two different modes: **Interactive Mode** and **Script Mode**. This guide provides instructions on how to use both modes effectively.
-----------------------------------------
            Interactive Mode
-----------------------------------------
In **Interactive Mode**, users can enter commands one at a time, and the interpreter will execute them immediately, providing an output for each command. This mode is helpful for testing individual lines of code or experimenting with language features.

        -----------------------------------------
             Steps to Run in Interactive Mode:
        -----------------------------------------
1. **Start the Interpreter:**
   - To start the interpreter in interactive mode, open your terminal or command prompt.
   - Navigate to the directory containing the interpreter file.
   - Run the interpreter using the command:

     python shell.py

2. **Enter Commands:**
   - Once the interpreter starts, you will see a prompt (`>>>`) indicating that the interpreter is ready to accept input.
   - You can now enter commands one at a time. For example:
     ```
     >>> VAR x = 10
     >>> VAR y = x + 5
     >>> FUNC add(a, b) -> a + b
     >>> add(x, y)
     ```
   - The interpreter will evaluate each command and display the result.

3. **Exit the Interpreter:**
   - To exit the interactive mode, press `Ctrl + C` or `Ctrl + D` on your keyboard.
