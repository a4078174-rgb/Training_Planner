# Настройка колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип тренировки", text="Тип тренировки")
        self.tree.heading("Длительность (мин)", text="Длительность (мин)")
        
        self.tree.column("ID", width=50)
        self.tree.column("Дата", width=120)
        self.tree.column("Тип тренировки", width=150)
        self.tree.column("Длительность (мин)", width=120)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка удаления
        delete_btn = tk.Button(self.root, text="Удалить выбранную тренировку", command=self.delete_training, bg="#f44336", fg="white")
        delete_btn.pack(pady=5)
    
    def validate_input(self, date_str, duration_str):
        """Проверка корректности ввода"""
        # Проверка даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return False
        
        # Проверка длительности
        try:
            duration = float(duration_str)
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом!")
            return False
        
        return True
    
    def add_training(self):
        """Добавление новой тренировки"""
        date = self.date_entry.get().strip()
        training_type = self.type_var.get()
        duration = self.duration_entry.get().strip()
        
        if not all([date, training_type, duration]):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        if self.validate_input(date, duration):
            # Генерация ID
            new_id = max([t["id"] for t in self.trainings], default=0) + 1
            
            training = {
                "id": new_id,
                "date": date,
                "type": training_type,
                "duration": float(duration)
            }
            
            self.trainings.append(training)
            self.save_data()
            self.refresh_table()
            
            # Очистка поля длительности
            self.duration_entry.delete(0, tk.END)
            
            messagebox.showinfo("Успех", "Тренировка добавлена!")
    
    def delete_training(self):
        """Удаление выбранной тренировки"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите тренировку для удаления!")
            return
        
        # Получение ID из выбранной строки
        item = self.tree.item(selected[0])
        training_id = item['values'][0]
        
        # Удаление из списка
        self.trainings = [t for t in self.trainings if t["id"] != training_id]
        self.save_data()
        self.refresh_table()
        
        messagebox.showinfo("Успех", "Тренировка удалена!")
    
    def refresh_table(self):
        """Обновление таблицы с учетом фильтров"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Применение фильтров
        filtered_trainings = self.trainings.copy()
        
        # Фильтр по типу
        filter_type = self.filter_type_var.get()
        if filter_type != "Все":
            filtered_trainings = [t for t in filtered_trainings if t["type"] == filter_type]
                    # Фильтр по дате
        filter_date = self.filter_date_entry.get().strip()
        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                filtered_trainings = [t for t in filtered_trainings if t["date"] == filter_date]
            except ValueError:
                if filter_date:
                    messagebox.showerror("Ошибка", "Неверный формат даты в фильтре!")
                    return
        
        # Сортировка по дате
        filtered_trainings.sort(key=lambda x: x["date"])
        
        # Заполнение таблицы
        for training in filtered_trainings:
            self.tree.insert("", "end", values=(
                training["id"],
                training["date"],
                training["type"],
                training["duration"]
            ))
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_type_var.set("Все")
        self.filter_date_entry.delete(0, tk.END)
        self.refresh_table()
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

if name == "main":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
