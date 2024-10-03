-----------------------------------------
User Guide: Running the Interpreter
-----------------------------------------

Function Definitions:

    - Use FUNC for named functions when you plan to reuse them.
    - Use LAMBDA for short, one-off functions or when passing a function as an argument.

Variables:

   - Variables are dynamically typed but currently support integers and functions.
    - Reassigning a variable will overwrite its previous value.

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
   - To exit interactive mode, type exit or press Ctrl + D (EOF) on your keyboard:

-----------------------------------------
            Script Mode
-----------------------------------------
In Script Mode, you can execute a series of commands from a file.
                    -----------------------------
    Example.txt {   |VAR x = 5;                 |
                    |VAR y = x * 2;             |
                    |FUNC square(n) -> n * n;   |
                    |VAR result = square(y);    |
                    -----------------------------
                 }

1. Create a Script File:
    - Write your code in a text file, e.g., program.bas.
    - Separate commands with semicolons (;) if you place multiple commands on the same line.

2. Run the Interpreter with the Script File:
    - Execute the interpreter and pass the script file as an argument:
        python shell.py Example.txt  - for example

3. Interpreter Output:
    - The interpreter will execute each command in the script file.
    - It will display outputs and errors just like in interactive mode.
    - Example Output:
             ____________________________________________
             |   Executing: VAR x = 5                   |
             |   Executing: VAR y = x * 2               |
             |   Executing: FUNC square(n) -> n * n     |
             |   Executing: VAR result = square(y)      |
             ____________________________________________

