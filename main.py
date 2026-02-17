from db import main_db
import flet as ft

def main(page: ft.Page):
    tasks_column = ft.Column()

    def create_task_row(task_id, task_value, task_date):
        def delete_from_db(id):
            main_db.delete_task(id)

        def edit_db(task_id, new_value):
            main_db.edit_task(task_id, new_value)
            print(f"Задача с ID: {task_id} обновлена на: {new_value}")

        def edit(e):
            task_text.read_only = True
            edit_db(task_id, task_text.value)
            page.update()

        def delete(e):
            tasks_column.controls.remove(task_row)
            delete_from_db(task_id)
            page.update()

        def edit_task(e):
            if task_text.read_only:
                task_text.read_only = False
            else:
                task_text.read_only = True
            page.update()

        task_text = ft.TextField(value=task_value, expand=True, read_only=True, on_submit=edit)
        task_date_text = ft.Text(value=task_date, size=12)
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=edit_task)
        submit_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=edit)
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete)
        task_row = ft.Row([task_text, task_date_text, edit_button, submit_button, delete_button])

        return task_row

    def add_new_task(e):
        if user_input.value:
            task_id, task_date = main_db.add_task(user_input.value)
            print(f"Добавлена новая задача: {user_input.value} ID: {task_id}")
            task_row = create_task_row(task_id, user_input.value, task_date)
            user_input.value = ""
            tasks_column.controls.insert(0, task_row)
            page.update()

    user_input = ft.TextField(label='Enter', expand=True, on_submit=add_new_task)
    enter_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_new_task)

    main_row = ft.Row([user_input, enter_button])

    page.add(main_row, tasks_column)


if __name__ == "__main__":
    main_db.create_tables()
    ft.run(main)
