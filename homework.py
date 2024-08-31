class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINS_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

        # В классаж наследниках переопределить эти переменные объекта
        self.trainig_type: str = 'тренировка'
        self.LEN_STEP: float = 0.65

        self.distance: float = 0.0
        self.speed: float = 0.0
        self.calories: float = 0.0

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / Training.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # преодолённая_дистанция_за_тренировку / время_тренировки
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0.0

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.trainig_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        # переопределить переменные объекта - хараетерные
        # для коонкретного типа тренировки
        self.trainig_type: str = 'Running'
        self.LEN_STEP: float = 0.65
        self.distance: float = self.get_distance()
        self.speed: float = self.get_mean_speed()
        self.calories: float = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + Running.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / Training.M_IN_KM * (self.duration * Training.MINS_IN_HOUR))

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    HOURS_TO_MIS: float = 0.278
    CN_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height
        # переопределить переменные объекта - хараетерные
        # для коонкретного типа тренировки
        self.trainig_type: str = 'SportsWalking'
        self.LEN_STEP: float = 0.65
        self.distance: float = self.get_distance()
        self.speed: float = self.get_mean_speed()
        self.calories: float = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        mean_speed_ms = self.get_mean_speed() * SportsWalking.HOURS_TO_MIS
        height_m = self.height / SportsWalking.CN_IN_M
        duration_mins = self.duration * Training.MINS_IN_HOUR
        return ((SportsWalking.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (mean_speed_ms**2 / (height_m))
                * SportsWalking.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                * duration_mins)

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SPENT_CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    SPENT_CALORIES_WEGHT_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool
        # переопределить переменные объекта - хараетерные для
        # коонкретного типа тренировки
        self.trainig_type: str = 'Swimming'
        self.LEN_STEP: float = 1.38
        self.distance: float = self.get_distance()
        self.speed: float = self.get_mean_speed()
        self.calories: float = self.get_spent_calories()

    def get_mean_speed(self) -> float:
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        return (self.length_pool * self.count_pool
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + Swimming.SPENT_CALORIES_MEAN_SPEED_SHIFT)
                * Swimming.SPENT_CALORIES_WEGHT_MULTIPLIER
                * self.weight * self.duration)

    def show_training_info(self) -> InfoMessage:
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
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('RUN', [15000, 1, 75]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
