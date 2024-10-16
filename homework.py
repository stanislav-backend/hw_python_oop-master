class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration} ч.;'
                f' Дистанция: {self.distance} км;'
                f' средняя скорость: {self.speed} км/ч;'
                f' Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    CH_IN_MIN: int = 60

    """Конструктор класса"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

        self.training_type: str = 'тренировка',
        self.distance: float = 0.0,
        self.speed: float = 0.0,
        self.calories: float = 0.0,

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * Training.LEN_STEP / Training.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    METR_IN_KM: int = 1000
    CH_IN_MIN: int = 60

    """Конструктор класса"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

        self.speed: float = self.get_mean_speed()
        self.training_type: str = 'Running'
        self.LEN_STEP: float = 0.65
        self.distance: float = self.get_distance()
        self.calories: float = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER * self.speed 
        + Running.CALORIES_MEAN_SPEED_SHIFT) * self.weight / 
        Running.METR_IN_KM * (self.duration * Running.CH_IN_MIN))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    Constan1: float = 0.035
    Constan2: float = 0.029
    HOURS_TO_MIS: float = 0.278
    CN_IN_M: int = 100

    """Конструктор класса"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height
        self.speed: float = self.get_mean_speed()
        self.training_type: str = 'SportsWalking'
        self.LEN_STEP: float = 0.65
        self.distance: float = self.get_distance()
        self.calories: float = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((SportsWalking.Constan1 * self.weight + (self.speed * (
                 SportsWalking.HOURS_TO_MIS) ** 2 / self.height / 
                 SportsWalking.CN_IN_M) * SportsWalking.Constan2 * 
                 self.weight) * self.duration * Training.CH_IN_MIN)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""
    Constan3: float = 1.1
    Constan4: int = 2

    """Конструктор класса"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool: int = lenght_pool
        self.count_pool: int = count_pool
        self.speed: float = self.get_mean_speed()
        self.training_type: str = 'Swimming'
        self.LEN_STEP: float = 1.38
        self.distance: float = self.get_distance()
        self.calories: float = self.get_spent_calories()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.lenght_pool * self.count_pool / 
        Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.speed + Swimming.Constan3) * 
        Swimming.Constan4 * self.weight * self.duration)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainigs: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    return trainigs[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
