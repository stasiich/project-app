class Course:
    _id_counter = 1

    def __init__(self, title, description, creator_email, comments=None):
        self.id = Course._id_counter
        Course._id_counter += 1

        self.title = title
        self.description = description
        self.creator_email = creator_email
        self.comments = comments if comments is not None else []

    def add_review(self, rating, comment):
        self.comments.append((rating, comment))

    def average_rating(self):
        if not self.comments:
            return 0
        total = sum(rating for rating, _ in self.comments)
        return round(total / len(self.comments), 1)
