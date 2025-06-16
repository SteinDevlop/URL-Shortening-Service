from backend.logic.universal_controller_instance import universal_controller as controller
from backend.models.urlacess import UrlacessCreate, UrlacessOut
from backend.models.url import UrlOut
data = controller.get_by_urlid(UrlacessOut,3)
print(list(UrlacessOut.get_fields().keys()))
print(data.to_dict() if hasattr(data, "to_dict") else dict(data))