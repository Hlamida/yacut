def shortlink(self, short):

    return url_for(
        REDIRECT_FUNCTION, short=self.short, _external=True,
    )