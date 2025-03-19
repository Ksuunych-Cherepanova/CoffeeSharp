class MonthYearConverter:
    regex = r"(0[1-9]|1[0-2])-[0-9]{4}"  # Формат MM-YYYY

    def to_python(self, value):
        month, year = map(int, value.split('-'))
        return {'month': month, 'year': year}

    def to_url(self, value):
        return f"{value['month']:02d}-{value['year']}"
