cascade="all, delete, delete-orphan",
        backref="user"
    )
    reviews = relationships(
        "Review",
        cascade="all, delete, delete-orphan",
        backref="user"
    )
  else:
    email =""
    password = ""
    first_name = ""
    last_name = ""

  def_init_(self, args, *kwargs):
    """initializes user"""
    super()._init_(args, *kwargs)

  def_setattr_(self, _name: str, _value) -> None:
    '''Sets an attribute of this class to a given value'''
    if _name == 'password'
        if type(_value) is str:
            m = hashlib.md5(bytes(_value, 'utf-8'))
            super()._setattr_(_name, m.hexdigest())
        else:
            super()._setattr_(_name, _value)
