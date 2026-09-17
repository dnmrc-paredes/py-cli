import httpx
import questionary

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def show_menu():
    print("What would you like to do?")
    choices = ["A: Get a Random joke", "B: Manage ToDo's", "Q: Quit / Back"]

    for choice in choices:
        print(choice)

    choice = input("Selection: ")
    return choice


def get_random_joke():
    req = httpx.get('https://official-joke-api.appspot.com/random_joke')
    data = req.json()

    print(f"'{data['setup']}'... {data['punchline']}.")


def show_task_menu():
    print("a: add, vp: view pending, vd: view done todos, q: quit / back")
    user_choice = input("Selection: ")
    return user_choice


def manage_todo():
    my_todos = []

    while True:
        user_choice = show_task_menu().lower().strip()

        match user_choice:
            case "a":
                task = input("Todo: ")

                my_todos.append({ "task": task, "pending": False })
                print(f"{GREEN}Task added!{RESET}")
            case "vp":
                choices = [
                        {"name": f"[{idx + 1}] {todo['task']}", "value": todo}
                        for idx, todo in enumerate(my_todos)
                        if not todo["pending"]
                        ] 

                if len(choices) == 0:
                    print(f"{YELLOW}No pending todo's{RESET}")
                    break

                select_to_update = questionary.select("Select an item", choices = choices).ask()

                while True:
                    print("D: delete, U: update, S: toggle status, Q: quit / back")
                    user_choice = input("Select an option: ")
                    item_index = my_todos.index(select_to_update)

                    match user_choice.lower():
                        case "d":
                            my_todos.pop(item_index)
                            print(f"{RED}Task deleted!{RESET}")
                            break
                        case "u":
                            while True:
                                new_updated_task = input("Enter updated task: ")

                                if len(new_updated_task) == 0:
                                    print(f"{RED}Please enter a valid value.{RESET}")
                                    continue

                                my_todos[item_index]['task'] = new_updated_task
                                print(f"{YELLOW}Task updated!{RESET}")
                                break
                        case "s":
                            my_todos[item_index]['pending'] = not my_todos[item_index]['pending']
                            print(f"Status: {f"{GREEN}Done{RESET}" if my_todos[item_index]['pending'] else f"{YELLOW}Pending{RESET}"}")
                            break
                        case "q":
                            break
            case "vd":
                choices = [
                        {"name": f"[{idx + 1}] {todo['task']}", "value": todo}
                        for idx, todo in enumerate(my_todos)
                        if todo["pending"]
                        ]

                if len(choices) == 0:
                    print(f"{YELLOW}No done todo's{RESET}")
                    break

                select_to_update = questionary.select("Select an item", choices = choices).ask()

                while True:
                    print("D: delete, S: toggle status, Q: quit / back")
                    user_choice = input("Select an option: ")
                    item_index = my_todos.index(select_to_update)

                    match user_choice.lower():
                        case "d":
                            my_todos.pop(item_index)
                            print(f"{RED}Task deleted!${RESET}")
                            break
                        case "s":
                            my_todos[item_index]['pending'] = not my_todos[item_index]['pending']
                            print(f"Status: {f"{GREEN}Done{RESET}" if my_todos[item_index]['pending'] else f"{YELLOW}Pending{RESET}"}")
                            break
                        case "q":
                            break
            case "q":
                break
            case _:
                print(f"{RED}Please pick a valid input.{RESET}")


def main():
    while True:
        user_choice = show_menu().lower().strip()

        match user_choice:
            case "a":
                get_random_joke()
            case "b":
                manage_todo()
            case "q":
                print("Thank you")
                break
            case _:
                print(f"{RED}Please pick a valid input.{RESET}")


