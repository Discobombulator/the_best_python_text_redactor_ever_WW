import os


class LargeFileHandler:
    def __init__(self, filename,
                 chunk_size=1024 * 1024 * 1024):  # 1 ГБ по умолчанию
        self.filename = filename
        self.chunk_size = chunk_size
        self.file_size = os.path.getsize(filename)
        self.current_chunk = 0
        self.total_chunks = (
                                    self.file_size + self.chunk_size - 1) // self.chunk_size
        self.loaded_chunks = {}
        self.current_position = 0

    def load_chunk(self, chunk_num, screen_width=None):
        if chunk_num in self.loaded_chunks:
            return self.loaded_chunks[chunk_num]

        with open(self.filename, 'rb') as f:
            f.seek(chunk_num * self.chunk_size)
            data = f.read(self.chunk_size).decode('utf-8', errors='replace')
            if '\n' not in data and data.strip():
                char_per_line = screen_width - 10 if screen_width else 120

                is_homogeneous = len(
                    set(data[:100])) <= 2  # Проверяем, однородны ли данные

                if is_homogeneous:
                    # Получаем первый значимый символ для создания строк
                    first_char = next((c for c in data if c.strip()), '1')
                    # Создаем список строк с одинаковым символом
                    lines = [first_char * char_per_line] * (
                            len(data) // char_per_line)
                    # Добавляем последнюю строку, если есть остаток
                    if len(data) % char_per_line > 0:
                        lines.append(first_char * (len(data) % char_per_line))
                else:
                    # Если данные разнородные, просто разбиваем на строки указанной длины
                    lines = [data[i:i + char_per_line] for i in
                             range(0, len(data), char_per_line)]
            else:
                # Стандартная обработка для файлов с переносами строк
                lines = data.splitlines()
                if not lines and data.strip():
                    lines = [data]

            self.loaded_chunks[chunk_num] = lines

        # Ограничиваем количество загруженных чанков в памяти
        if len(self.loaded_chunks) > 2:
            oldest_chunk = min(
                k for k in self.loaded_chunks.keys() if k != chunk_num)
            del self.loaded_chunks[oldest_chunk]

        return lines

    def get_lines(self, screen_width=None):
        return self.load_chunk(self.current_chunk, screen_width)

    def move_to_chunk(self, chunk_num, screen_width=None):
        if 0 <= chunk_num < self.total_chunks:
            self.current_chunk = chunk_num
            return self.get_lines(screen_width)
        return None

    def get_position_info(self):
        return {
            'current_chunk': self.current_chunk,
            'total_chunks': self.total_chunks,
            'chunk_size': self.chunk_size,
            'file_size': self.file_size
        }