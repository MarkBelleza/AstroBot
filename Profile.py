class Profile:
  def __init__(self, userID):
    self.userId = userID
    self.winCount = 0
    self.inbox = []
    self.gameKey = ""
    self.inGame = False
    self.myTurn = True

  def get_myTurn(self):
    return self.myTurn
  
  def get_gameKey(self):
    return self.gameKey

  def get_inGame(self):
    return self.inGame

  def get_inbox(self):
    return self.inbox

  def add_message(self, message):
    self.inbox.append(message)

  def read_message(self):
    return self.inbox.pop()

  def add_win(self):
    self.winCount += 1

  def set_gameKey(self, key):
    self.gameKey = key

  def set_myTurn(self):
    self.myTurn = not self.myTurn

  def reset_myTurn(self):
    self.myTurn = True