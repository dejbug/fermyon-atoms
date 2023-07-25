def stringify(cls):
	setattr(cls, "__str__", lambda self: self.__class__.__name__ + str(self.__dict__))
	return cls
