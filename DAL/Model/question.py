class Question:
    def __init__(self, content, duration, response_rate, random_answer, id_slide, min_points, max_points, threshold):
        self.content = content
        self.duration = duration
        self.response_rate = response_rate
        self.random_answer = random_answer
        self.id_slide = id_slide
        self.min_points = min_points
        self.max_points = max_points
        self.threshold = threshold
