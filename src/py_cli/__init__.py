import httpx
import questionary


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
        user_choice = show_task_menu()

        match user_choice.lower():
            case "a":
                task = input("Todo: ")

                my_todos.append({ "task": task, "pending": False })
            case "vp":
                if len(my_todos) == 0:
                    print("No pending todo's")
                    break

                choices = [
                        {"name": f"[{idx + 1}] {todo['task']}", "value": todo}
                        for idx, todo in enumerate(my_todos)
                        if not todo["pending"]
                        ]

                select_to_update = questionary.select("Select an item", choices = choices).ask()

                while True:
                    print("D: delete, U: update, Q: quit / back")
                    user_choice = input("Select an option: ")
                    item_index = my_todos.index(select_to_update)

                    match user_choice.lower():
                        case "d":
                            my_todos.pop(item_index)
                            print("Task deleted!")
                            break
                        case "u":
                            while True:
                                new_updated_task = input("Enter updated task: ")

                                if len(new_updated_task) == 0:
                                    print("Please enter a valid value.")
                                    continue

                                my_todos[item_index]['task'] = new_updated_task
                                print("Task updated!")
                                break
                        case "q":
                            break

            case "vd":
                choices = [
                        {"name": f"[{idx + 1}] {todo['task']}", "value": todo}
                        for idx, todo in enumerate(my_todos)
                        if todo["pending"]
                        ]

                select_to_update = questionary.select("Select an item", choices = choices).ask()
            case "q":
                break
            case _:
                print("Please pick a valid input.")


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
                print("Please pick a valid input.")


