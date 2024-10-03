import sys
import basic

def execute_command(text):
    result, error = basic.run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result is not None:
        print(result)

def interactive_mode():
    print("Interactive mode. Type 'exit' to quit.")
    while True:
        try:
            text = input('basic > ')
            if text.strip().lower() == 'exit':
                break
            if text.strip() == '':
                continue
            execute_command(text)
            print()
        except EOFError:
            break

def program_mode(filename):
    with open(filename, 'r') as file:
        program = file.read()

    commands = program.split(';')
    for command in commands:
        command = command.strip()
        if command:
            print(f"Executing: {command}")
            execute_command(command)
            print()

def main():
    if len(sys.argv) > 1:
        # Program mode
        program_mode(sys.argv[1])
    else:
        # Interactive mode
        interactive_mode()

if __name__ == '__main__':
    main()
