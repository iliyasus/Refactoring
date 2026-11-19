import random
import sys
import time


def type_print(text, delay=0.015, end="\n"):
    """Эффект плавной печати текста для улучшения атмосферы игры."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(end, end="")


def run_quiz():
    # Наша база данных вопросов (можно расширять сколько угодно)
    question_pool = [
        {
            "question": "Как в Python обозначается возведение в степень?",
            "options": ["^", "**", "pow()"],
            "correct_index": 1,
        },
        {
            "question": "Какой тип данных используется для хранения целых чисел?",
            "options": ["float", "str", "int"],
            "correct_index": 2,
        },
        {
            "question": "Какая функция выводит текст на экран?",
            "options": ["print()", "input()", "output()"],
            "correct_index": 0,
        },
        {
            "question": "Что вернет выражение 3 * 'A'?",
            "options": ["'AAA'", "'3A'", "Ошибку"],
            "correct_index": 0,
        },
        {
            "question": "Как правильно создать пустой список?",
            "options": ["list = {}", "list = []", "list = ()"],
            "correct_index": 1,
        },
        {
            "question": "Какой логический оператор используется для проверки условия 'И'?",
            "options": ["or", "and", "not"],
            "correct_index": 1,
        },
        {
            "question": "Как получить длину строки или списка в Python?",
            "options": ["count()", "size()", "len()"],
            "correct_index": 2,
        },
        {
            "question": "Какой метод используется для добавления элемента в конец списка?",
            "options": ["append()", "add()", "push()"],
            "correct_index": 0,
        },
        {
            "question": "Какое ключевое слово используется для создания функции?",
            "options": ["func", "function", "def"],
            "correct_index": 2,
        },
        {
            "question": "Какое из этих выражений преобразует строку '5' в число?",
            "options": ["int('5')", "str(5)", "float('5.0')"],
            "correct_index": 0,
        },
    ]

    # Игровые метрики
    lives = 5
    question_number = 1
    correct_answers = 0
    total_score = 0
    current_streak = 0
    max_streak = 0

    # Создаем рабочий список вопросов, который будем опустошать
    active_pool = question_pool.copy()
    random.shuffle(active_pool)

    # Красивое приветствие
    print("=" * 60)
    type_print(" 💀  PYTHON QUIZ: РЕЖИМ ВЫЖИВАНИЯ (SURVIVAL)  💀 ")
    print("=" * 60)
    type_print(
        " Игра идет до тех пор, пока вы не потеряете все 5 жизней. Удачи!"
    )
    print("=" * 60 + "\n")
    time.sleep(0.5)

    # Главный игровой цикл (пока живы)
    while lives > 0:
        # Если вопросы в пуле закончились, копируем их заново и перемешиваем
        if not active_pool:
            active_pool = question_pool.copy()
            random.shuffle(active_pool)

        # Достаем один вопрос
        q = active_pool.pop()

        # Отображение статуса
        heart_display = "❤️ " * lives
        print(f"🔷 ВОПРОС №{question_number}")
        print(f"Жизни: {heart_display} ({lives}/5)")
        if current_streak > 1:
            print(f"🔥 СЕРИЯ ОТВЕТОВ: {current_streak}x МНОЖИТЕЛЬ!")

        print("-" * 40)
        type_print(f"👉 {q['question']}\n")

        # Перемешивание вариантов ответов
        indexed_options = list(enumerate(q["options"]))
        random.shuffle(indexed_options)

        correct_input_number = None
        for display_num, (original_idx, text) in enumerate(
            indexed_options, start=1
        ):
            print(f"  [{display_num}] {text}")
            if original_idx == q["correct_index"]:
                correct_input_number = display_num

        # Валидация ввода
        valid_choices = [str(i) for i in range(1, len(q["options"]) + 1)]
        while True:
            user_input = input("\n⌨️ Ваш выбор: ").strip()
            if user_input in valid_choices:
                user_answer = int(user_input)
                break
            print(f"❌ Ошибка! Введите число от 1 до {len(valid_choices)}.")

        # Проверка ответа и логика жизней/очков
        print("-" * 40)
        if user_answer == correct_input_number:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
            correct_answers += 1

            points_earned = 100 * current_streak
            total_score += points_earned

            print(f"🎉 ПРАВИЛЬНО! ✅ (+{points_earned} очков)")
        else:
            lives -= 1
            current_streak = 0  # Сброс комбо
            correct_text = q["options"][q["correct_index"]]

            print(f"💥 ОШИБКА! Потеряна 1 жизнь. ❌")
            print(f"💡 Правильный ответ: {correct_text}")

        print(f"💰 Всего очков: {total_score}")
        print("=" * 60 + "\n")

        question_number += 1
        time.sleep(0.8)

    # Финальный экран (когда жизней не осталось)
    print("\n" + "═" * 60)
    print(" 🪦  GAME OVER — ВЫ ПОТЕРЯЛИ ВСЕ ЖИЗНИ  🪦 ")
    print("═" * 60)
    time.sleep(0.5)

    type_print(f"📊 Всего вопросов пройдено: {question_number - 1}")
    type_print(f"📈 Успешных ответов:      {correct_answers}")
    type_print(f"🏆 Финальный счет:         {total_score} очков")
    type_print(f"🔥 Максимальное комбо:     {max_streak}")
    print("-" * 60)

    # Оценка на основе набранных очков
    if total_score >= 2000:
        type_print("👑 ЛЕГЕНДА! Вы продержались невероятно долго! Пул пробит. 👑")
    elif total_score >= 1000:
        type_print("⚡ Отличный результат! Настоящий хардкорный кодер. 👍")
    elif total_score >= 4000:
        type_print("📈 Хорошая попытка, но база взяла своё. Практикуйтесь дальше! 📚")
    else:
        type_print("🧙 Быстрое поражение. Стоит подтянуть синтаксис! 🔄")
    print("═" * 60)


if __name__ == "__main__":
    run_quiz()
