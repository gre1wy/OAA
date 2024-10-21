import re # Для обробки регулярних виразів


class Token(object):

    """Клас для представлення токенів"""

    def __init__(self, type, value):

        """Ініціалізація токена

        Args:
            type (str): Тип токена
            value (str): Значення токена
        """

        self.type = type
        self.value = value

    def __str__(self):

        """Повертає рядкове представлення токена"""

        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):

        """Повертає представлення токена"""

        return self.__str__()
    
class Lexer(object):

    """Клас для токенізації тексту

    Використовується для розбиття введеного тексту на токени,
    які потім можуть бути оброблені парсером
    """

    def __init__(self, text):

        """Ініціалізація лексера

        Args:
            text (str): Текст для токенізації
        """

        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception('Помилка в лексері')

    def advance(self):

        """Переміщуємо покажчик `pos` та встановлюємо змінну `current_char`"""

        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # Вказує на кінець введення
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):

        """Пропускаємо пробіли"""

        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_token_type(self, token):

        """Визначаємо тип токена на основі його значення за допомогою регулярних виразів"""
        
        token_patterns = {
            r'CREATE': 'CREATE',
            r'INSERT': 'INSERT',
            r'PRINT_INDEX': 'PRINT_INDEX',
            r'SEARCH': 'SEARCH',
            r'WHERE': 'WHERE',
            r'^[a-zA-Z][a-zA-Z0-9_]*$': 'COLLECTION',
            r'^"[a-zA-Z][a-zA-Z0-9_]*"$': 'WORD', 
            r'^".*"$': 'DOCUMENT',
            r'^-': 'MIN',
            r'^<\d+>$': 'DIST',
            r'^;$': 'EOI'
        }

        # Перевіряємо, якому шаблону відповідає токен
        for pattern, token_type in token_patterns.items():
            if re.match(pattern, token, re.IGNORECASE if token_type in ['CREATE', 'INSERT', 'PRINT_INDEX', 'SEARCH', 'WHERE'] else 0):
                return token_type

        self.error()

    def tokenize_text(self, text):

        """Розбиваємо текст на окремі слова, використовуючи регулярні вирази"""
        
        words = re.findall(r'[a-zA-Z0-9_]+', text)
        return words

    def get_next_token(self):

        """Отримуємо наступний токен з введення, обробляючи рядки в лапках та інші типи токенів"""
        
        while self.current_char is not None:

            # Пропускаємо пробіли
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Кінець команди
            if self.current_char == ';':
                self.advance()
                return Token('EOI', ';')

            # Обробка знаку мінус
            if self.current_char == '-':
                self.advance()
                return Token('MIN', '-')

            # Ініціалізуємо результат для збору символів токена
            result = ''

            # Обробка рядків в лапках (документів або слів)
            if self.current_char == '"':
                self.advance()
                result, contains_space = self._get_quoted_string()
                token_type = 'DOCUMENT' if contains_space else 'WORD'
                result = self.tokenize_text(result)
                return Token(token_type, result)

            # Обробка кутових дужок для <N>
            if self.current_char == '<':
                self.advance()
                result = self._get_angle_bracket_content()
                if result.isdigit():
                    return Token('DIST', int(result))  # Повертаємо як ціле число
                else:
                    self.error()  # Помилка, якщо не число

            # Збираємо звичайні слова/ідентифікатори
            while self.current_char is not None and not self.current_char.isspace() and self.current_char not in [';', '"']:
                result += self.current_char
                self.advance()

            if result:
                token_type = self.get_token_type(result)
                return Token(token_type, result)

        return Token('EOF', None)

    def _get_quoted_string(self):

        """Допоміжний метод для обробки рядків в лапках та визначення, чи містять вони пробіли """
        
        result = ''
        contains_space = False
        while self.current_char is not None and self.current_char != '"':
            if self.current_char.isspace():
                contains_space = True
            result += self.current_char
            self.advance()

        # Якщо досягли кінця тексту без закриваючої лапки, викликаємо помилку
        if self.current_char is None:
            self.error()  # Незакрита лапка

        self.advance()  # Переміщуємося через закриваючу лапку
        return result, contains_space

    def _get_angle_bracket_content(self):

        """Допоміжний метод для збору вмісту в кутових дужках"""
        
        result = ''
        while self.current_char is not None and self.current_char != '>':
            result += self.current_char
            self.advance()

        # Якщо досягли кінця тексту без закриваючої кутової дужки, викликаємо помилку
        if self.current_char is None:
            self.error()  # Незакрита кутова дужка

        self.advance()  # Переміщуємося через закриваючу дужку
        return result



if __name__ == '__main__':
    lexer = Lexer('CrEate "jje"fkfo; <4>')

    token = lexer.get_next_token()
    while token.type != 'EOF':
        print(token)
        token = lexer.get_next_token()
