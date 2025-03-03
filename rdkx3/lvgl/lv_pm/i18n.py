import json

class i18n:
    this = None

    def __new__(self, file: str):
        if self.this is None:
            self.this = super(i18n, self).__new__(self)
            with open(file, "rb") as f:
                self.this.json = json.load(f)
            self.this.locale = None
        return self.this

    def get_text(self, msg: str) -> str:
        try:
            return self.json[msg][self.locale] if self.locale else msg
        except:
            return msg

    def set_locale(self, l_name: str | None = None):
        if self.locale != l_name:
            self.locale = l_name
            return True
        return False