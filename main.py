import flet as ft
from db import main_db


def main(page: ft.Page):
    tasks_column = ft.Column()

    def add_to_db(name):
        task_id, task_date = main_db.add_task(name)
        print(f"Добавлена новая задача: {name} ID: {task_id}")
        return task_id, task_date

    def edit_db(task_id, new_value):
        main_db.edit_task(task_id, new_value)
        print(f"Задача с ID: {task_id} обновлена на: {new_value}")

    def delete_from_db(task_id):
        main_db.delete_task(task_id)

    def add_task(task_id, task, task_date):
        def edit(e):
            edit_db(task_id, task_text.value)
            task_text.read_only = True
            page.update()

        def delete(e):
            delete_from_db(task_id)
            tasks_column.controls.remove(task_row)
            page.update()

        def to_edit(e):
            if task_text.read_only:
                task_text.read_only = False
            else:
                task_text.read_only = True
            page.update()

        task_text = ft.TextField(value=task, expand=True, read_only=True, on_submit=edit)
        task_date_text = ft.Text(value=task_date, size=12)
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=to_edit)
        submit_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=edit)
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete)
        task_row = ft.Row([task_text, task_date_text, edit_button, submit_button, delete_button])

        return task_row

    def add_new_task(e):
        if user_input.value:
            task_value = user_input.value
            task_id, task_date = add_to_db(task_value)
            task_row = add_task(task_id, task_value, task_date)
            user_input.value = ""
        
            tasks_column.controls.append(task_row)
            page.update()

    def load_from_db():
        tasks_column.controls.clear()
        results = main_db.get_all_tasks()
        if results:
            for task_id, task, task_date, completed in results:
                result = add_task(task_id, task, task_date)
                tasks_column.controls.append(result)
        page.update()

    def filter_by(completed):
        tasks_column.controls.clear()
        results = main_db.get_tasks_by_filters(completed)
        if results:
            for task_id, task, task_date, task_completed in results:
                result = add_task(task_id, task, task_date)
                tasks_column.controls.append(result)
        page.update()

    def clear_completed(e):
        main_db.clear_completed_tasks()
        load_from_db()

    user_input = ft.TextField(label="Новая задача", expand=True, on_submit=add_new_task)
    enter_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_new_task)

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: load_from_db()),
        ft.ElevatedButton("Выполненные", on_click=lambda e: filter_by(1)),
        ft.ElevatedButton("Невыполненные", on_click=lambda e: filter_by(0)),
        ft.ElevatedButton("Очистить выполненные", on_click=clear_completed),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )
    main_row = ft.Row([user_input, enter_button])

    page.add(main_row, tasks_column, filter_buttons)
    load_from_db()

if __name__ == "__main__":
    main_db.create_tables()
    ft.run(main, view=ft.AppView.WEB_BROWSER)
