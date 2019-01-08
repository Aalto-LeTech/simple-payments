from wtforms import Form as WtForm

class Form(WtForm):
    @property
    def errors_as_string(self):
        out = []
        for key, values in self.errors.items():
            out.append("%s:" % (key,))
            for value in values:
                out.append("  - %s" % (value,))
        return "\n".join(out)
