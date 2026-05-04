messagebox.showwarning("Предупреждение", "Выберите тренировку для редактирования!")
            return
        
        # Получение данных
        item = self.tree.item(selected[0])
        training_id = item['values'][0]
        training = next((t for t in self.trainings if t["id"] == training_id), None)
        
        if training:
            # Создание окна редактирования
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Редактирование тренировки")
            edit_window.geometry("400x250")
            edit_window.resizable(False, False)
            
            # Поля ввода
            ttk.Label(edit_window, text="Дата (ГГГГ-ММ-ДД):").pack(pady=5)
            date_entry = ttk.Entry(edit_window, width=30)
            date_entry.insert(0, training["date"])
            date_entry.pack(pady=5)
            
            ttk.Label(edit_window, text="Тип тренировки:").pack(pady=5)
            type_combo = ttk.Combobox(edit_window, values=["Бег", "Велосипед", "Плавание", "Силовая", "Йога", "Футбол"], width=27)
            type_combo.set(training["type"])
            type_combo.pack(pady=5)
            
            ttk.Label(edit_window, text="Длительность (мин):").pack(pady=5)
            duration_entry = ttk.Entry(edit_window, width=30)
            duration_entry.insert(0, str(training["duration"]))
            duration_entry.pack(pady=5)
            
            def save_edit():
                # Проверка ввода
                try:
                    datetime.strptime(date_entry.get(), "%Y-%m-%d")
                    duration = float(duration_entry.get())
                    if duration <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат даты или длительности!")
                    return
                
                training["date"] = date_entry.get()
                training["type"] = type_combo.get()
                training["duration"] = duration
                
                self.apply_filters()
                edit_window.destroy()
                messagebox.showinfo("Успех", "Тренировка обновлена!")
                self.update_statistics()
            
            ttk.Button(edit_window, text="Сохранить", command=save_edit).pack(pady=20)
    
    def apply_filters(self):
        """Применение фильтров"""
        filter_type = self.filter_type.get()
        filter_date = self.filter_date.get().strip()
        
        self.filtered_trainings = self.trainings.copy()
        
        # Фильтр по типу
        if filter_type != "Все":
            self.filtered_trainings = [t for t in self.filtered_trainings if t["type"] == filter_type]
        
        # Фильтр по дате
        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                self.filtered_trainings = [t for t in self.filtered_trainings if t["date"] == filter_date]
            except ValueError:
                pass
        
        self.refresh_table()
        self.update_statistics()
    
    def reset_filters(self):
        """Сброс фильтров"""
        self.filter_type.set("Все")
        self.filter_date.delete(0, tk.END)
        self.apply_filters()
    
    def refresh_table(self):
        """Обновление таблицы"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление данных
        for training in self.filtered_trainings:
            self.tree.insert("", tk.END, values=(
                training["id"],
                training["date"],
                training["type"],
                f"{training['duration']:.0f}"
            ))
    
    def update_statistics(self):
        """Обновление статистики"""
        total_trainings = len(self.filtered_trainings)
        total_duration = sum(t["duration"] for t in self.filtered_trainings)
        self.stats_label.config(text=f"📊 Найдено: {tot
