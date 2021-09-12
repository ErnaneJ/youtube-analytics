from controllers.Analytics_controller import *
from models.Analytics import *
from views.Analytics_view import *

if __name__ == "__main__":
  controller = Analytics_Controller()
  model = Analytics()
  view = Analytics_View(controller.root)
  controller.initialize(model, view)
  controller.execute()
  controller.creditos()
